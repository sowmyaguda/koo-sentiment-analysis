"""
Multilingual Sentiment Model using Transformers
"""

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from typing import List, Dict, Tuple
import numpy as np


class MultilingualSentimentModel:
    """
    Wrapper for multilingual sentiment analysis models using HuggingFace Transformers
    """

    SUPPORTED_MODELS = {
        'bert-multilingual-sentiment': 'nlptown/bert-base-multilingual-uncased-sentiment',
        'xlm-roberta-sentiment': 'cardiffnlp/twitter-xlm-roberta-base-sentiment',
        'indic-bert': 'ai4bharat/indic-bert',
    }

    def __init__(self, model_name: str = 'bert-multilingual-sentiment', device: str = 'cpu'):
        """
        Initialize the multilingual sentiment model

        Args:
            model_name: Name of the model to use
            device: Device to run the model on ('cpu' or 'cuda')
        """
        self.device = device
        self.model_name = model_name

        # Get the actual model identifier
        if model_name in self.SUPPORTED_MODELS:
            model_id = self.SUPPORTED_MODELS[model_name]
        else:
            model_id = model_name  # Allow custom model names

        print(f"Loading model: {model_id}")
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_id)
        self.model.to(self.device)
        self.model.eval()

        # Determine the sentiment mapping based on the model
        self._setup_sentiment_mapping(model_id)

        print(f"Model loaded successfully on {self.device}")

    def _setup_sentiment_mapping(self, model_id: str):
        """Set up sentiment label mapping based on model type"""
        if 'nlptown' in model_id:
            # 5-star rating model (1-5)
            self.labels = ['very negative', 'negative', 'neutral', 'positive', 'very positive']
            self.sentiment_map = {
                0: 'very negative',
                1: 'negative',
                2: 'neutral',
                3: 'positive',
                4: 'very positive'
            }
        elif 'cardiffnlp' in model_id or 'twitter' in model_id:
            # 3-class sentiment
            self.labels = ['negative', 'neutral', 'positive']
            self.sentiment_map = {
                0: 'negative',
                1: 'neutral',
                2: 'positive'
            }
        else:
            # Default 3-class
            self.labels = ['negative', 'neutral', 'positive']
            self.sentiment_map = {
                0: 'negative',
                1: 'neutral',
                2: 'positive'
            }

    def predict(self, text: str) -> Dict:
        """
        Predict sentiment for a single text

        Args:
            text: Input text

        Returns:
            Dictionary with sentiment prediction and scores
        """
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=512,
            padding=True
        ).to(self.device)

        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            probs = torch.nn.functional.softmax(logits, dim=-1)

        scores = probs[0].cpu().numpy()
        predicted_class = int(torch.argmax(probs, dim=-1).cpu().numpy()[0])
        sentiment = self.sentiment_map[predicted_class]

        # Create score dictionary
        score_dict = {label: float(score) for label, score in zip(self.labels, scores)}

        return {
            'sentiment': sentiment,
            'confidence': float(scores[predicted_class]),
            'scores': score_dict,
            'predicted_class': predicted_class
        }

    def predict_batch(self, texts: List[str], batch_size: int = 16) -> List[Dict]:
        """
        Predict sentiments for multiple texts

        Args:
            texts: List of input texts
            batch_size: Batch size for processing

        Returns:
            List of prediction dictionaries
        """
        results = []

        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i + batch_size]

            inputs = self.tokenizer(
                batch_texts,
                return_tensors="pt",
                truncation=True,
                max_length=512,
                padding=True
            ).to(self.device)

            with torch.no_grad():
                outputs = self.model(**inputs)
                logits = outputs.logits
                probs = torch.nn.functional.softmax(logits, dim=-1)

            batch_results = []
            for j in range(len(batch_texts)):
                scores = probs[j].cpu().numpy()
                predicted_class = int(torch.argmax(probs[j]).cpu().numpy())
                sentiment = self.sentiment_map[predicted_class]

                score_dict = {label: float(score) for label, score in zip(self.labels, scores)}

                batch_results.append({
                    'sentiment': sentiment,
                    'confidence': float(scores[predicted_class]),
                    'scores': score_dict,
                    'predicted_class': predicted_class
                })

            results.extend(batch_results)

        return results

    def get_sentiment_score(self, text: str) -> float:
        """
        Get a normalized sentiment score [-1, 1]

        Args:
            text: Input text

        Returns:
            Sentiment score (-1 = negative, 0 = neutral, 1 = positive)
        """
        result = self.predict(text)

        if len(self.labels) == 5:
            # For 5-class model, map to [-1, 1]
            class_idx = result['predicted_class']
            return (class_idx - 2) / 2.0  # Maps 0->-1, 2->0, 4->1
        elif len(self.labels) == 3:
            # For 3-class model
            scores = result['scores']
            if 'positive' in scores and 'negative' in scores:
                return scores['positive'] - scores['negative']
            else:
                class_idx = result['predicted_class']
                return (class_idx - 1)  # Maps 0->-1, 1->0, 2->1

        return 0.0

    def analyze_emotions(self, text: str) -> Dict:
        """
        Analyze emotional content (wrapper around sentiment)

        Args:
            text: Input text

        Returns:
            Dictionary with emotion analysis
        """
        result = self.predict(text)

        # Map sentiment to emotions
        emotion_map = {
            'very negative': ['angry', 'disgusted', 'sad'],
            'negative': ['sad', 'fearful'],
            'neutral': ['neutral'],
            'positive': ['happy', 'surprised'],
            'very positive': ['happy', 'excited']
        }

        primary_emotion = emotion_map.get(result['sentiment'], ['neutral'])[0]

        return {
            'primary_emotion': primary_emotion,
            'sentiment': result['sentiment'],
            'confidence': result['confidence'],
            'all_emotions': emotion_map.get(result['sentiment'], ['neutral'])
        }
