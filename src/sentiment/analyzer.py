"""
Main Sentiment Analyzer for KOO posts
"""

import pandas as pd
from typing import List, Dict, Optional
from pathlib import Path
import json
from tqdm import tqdm

from .multilingual_model import MultilingualSentimentModel
from ..scraper.data_models import KooPost
from ..utils.language_detector import LanguageDetector


class SentimentAnalyzer:
    """
    Main sentiment analyzer for KOO posts with multilingual support
    """

    def __init__(self, config: Dict = None):
        """
        Initialize the sentiment analyzer

        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        model_name = self.config.get('model_name', 'bert-multilingual-sentiment')
        device = self.config.get('device', 'cpu')
        self.batch_size = self.config.get('batch_size', 16)

        print("Initializing Sentiment Analyzer...")
        self.model = MultilingualSentimentModel(model_name=model_name, device=device)
        self.language_detector = LanguageDetector()

        self.results = []

    def analyze_post(self, post: KooPost) -> Dict:
        """
        Analyze sentiment of a single post

        Args:
            post: KooPost object

        Returns:
            Dictionary with analysis results
        """
        # Detect language if not provided
        if not post.language:
            post.language = self.language_detector.detect(post.text)

        # Get sentiment prediction
        sentiment_result = self.model.predict(post.text)

        # Get normalized sentiment score
        sentiment_score = self.model.get_sentiment_score(post.text)

        result = {
            'post_id': post.post_id,
            'text': post.text,
            'author': post.author,
            'timestamp': post.timestamp.isoformat(),
            'language': post.language,
            'sentiment': sentiment_result['sentiment'],
            'sentiment_score': sentiment_score,
            'confidence': sentiment_result['confidence'],
            'sentiment_scores': sentiment_result['scores'],
            'likes': post.likes,
            'reposts': post.reposts,
            'comments': post.comments,
            'hashtags': post.hashtags,
            'mentions': post.mentions
        }

        return result

    def analyze_posts(self, posts: List[KooPost], show_progress: bool = True) -> List[Dict]:
        """
        Analyze sentiment of multiple posts

        Args:
            posts: List of KooPost objects
            show_progress: Whether to show progress bar

        Returns:
            List of analysis results
        """
        results = []

        # Detect languages for all posts
        for post in posts:
            if not post.language:
                post.language = self.language_detector.detect(post.text)

        # Extract texts for batch processing
        texts = [post.text for post in posts]

        # Batch sentiment analysis
        print(f"Analyzing {len(posts)} posts...")
        sentiment_results = self.model.predict_batch(texts, batch_size=self.batch_size)

        # Combine results
        iterator = zip(posts, sentiment_results)
        if show_progress:
            iterator = tqdm(list(iterator), desc="Processing results")

        for post, sentiment_result in iterator:
            sentiment_score = self._calculate_sentiment_score(sentiment_result)

            result = {
                'post_id': post.post_id,
                'text': post.text,
                'author': post.author,
                'timestamp': post.timestamp.isoformat(),
                'language': post.language,
                'sentiment': sentiment_result['sentiment'],
                'sentiment_score': sentiment_score,
                'confidence': sentiment_result['confidence'],
                'sentiment_scores': sentiment_result['scores'],
                'likes': post.likes,
                'reposts': post.reposts,
                'comments': post.comments,
                'hashtags': post.hashtags,
                'mentions': post.mentions
            }

            results.append(result)

        self.results = results
        print(f"Analysis complete! Processed {len(results)} posts.")
        return results

    def _calculate_sentiment_score(self, sentiment_result: Dict) -> float:
        """Calculate normalized sentiment score from prediction"""
        scores = sentiment_result['scores']

        if len(scores) == 5:
            # 5-class model
            class_idx = sentiment_result['predicted_class']
            return (class_idx - 2) / 2.0
        elif len(scores) == 3:
            # 3-class model
            if 'positive' in scores and 'negative' in scores:
                return scores['positive'] - scores['negative']
            else:
                class_idx = sentiment_result['predicted_class']
                return (class_idx - 1)

        return 0.0

    def get_statistics(self) -> Dict:
        """
        Get statistical summary of sentiment analysis

        Returns:
            Dictionary with statistics
        """
        if not self.results:
            return {}

        df = pd.DataFrame(self.results)

        stats = {
            'total_posts': len(self.results),
            'sentiment_distribution': df['sentiment'].value_counts().to_dict(),
            'average_sentiment_score': float(df['sentiment_score'].mean()),
            'sentiment_by_language': df.groupby('language')['sentiment'].value_counts().to_dict(),
            'average_confidence': float(df['confidence'].mean()),
            'most_positive_post': self._get_extreme_post(df, 'max'),
            'most_negative_post': self._get_extreme_post(df, 'min'),
            'engagement_by_sentiment': {
                'likes': df.groupby('sentiment')['likes'].mean().to_dict(),
                'reposts': df.groupby('sentiment')['reposts'].mean().to_dict(),
                'comments': df.groupby('sentiment')['comments'].mean().to_dict()
            }
        }

        return stats

    def _get_extreme_post(self, df: pd.DataFrame, extreme_type: str) -> Dict:
        """Get the most positive or negative post"""
        if extreme_type == 'max':
            idx = df['sentiment_score'].idxmax()
        else:
            idx = df['sentiment_score'].idxmin()

        post = df.loc[idx]
        return {
            'post_id': post['post_id'],
            'text': post['text'][:100] + '...' if len(post['text']) > 100 else post['text'],
            'sentiment_score': float(post['sentiment_score']),
            'sentiment': post['sentiment']
        }

    def analyze_hashtags(self) -> Dict:
        """
        Analyze sentiment by hashtags

        Returns:
            Dictionary with hashtag sentiment analysis
        """
        hashtag_sentiments = {}

        for result in self.results:
            for hashtag in result['hashtags']:
                if hashtag not in hashtag_sentiments:
                    hashtag_sentiments[hashtag] = {
                        'count': 0,
                        'sentiments': [],
                        'scores': []
                    }

                hashtag_sentiments[hashtag]['count'] += 1
                hashtag_sentiments[hashtag]['sentiments'].append(result['sentiment'])
                hashtag_sentiments[hashtag]['scores'].append(result['sentiment_score'])

        # Calculate statistics for each hashtag
        hashtag_stats = {}
        for hashtag, data in hashtag_sentiments.items():
            hashtag_stats[hashtag] = {
                'count': data['count'],
                'average_sentiment_score': sum(data['scores']) / len(data['scores']),
                'sentiment_distribution': pd.Series(data['sentiments']).value_counts().to_dict()
            }

        return hashtag_stats

    def save_results(self, output_path: str, format: str = 'json'):
        """
        Save analysis results to file

        Args:
            output_path: Path to save file
            format: Output format ('json' or 'csv')
        """
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        if format == 'json':
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, indent=2, ensure_ascii=False)
        elif format == 'csv':
            df = pd.DataFrame(self.results)
            # Flatten nested dictionaries
            df['sentiment_scores'] = df['sentiment_scores'].apply(json.dumps)
            df['hashtags'] = df['hashtags'].apply(lambda x: ','.join(x) if x else '')
            df['mentions'] = df['mentions'].apply(lambda x: ','.join(x) if x else '')
            df.to_csv(path, index=False, encoding='utf-8')

        print(f"Results saved to {output_path}")

    def export_summary_report(self, output_path: str):
        """
        Export a summary report

        Args:
            output_path: Path to save the report
        """
        stats = self.get_statistics()
        hashtag_stats = self.analyze_hashtags()

        report = {
            'summary': stats,
            'top_hashtags': dict(sorted(
                hashtag_stats.items(),
                key=lambda x: x[1]['count'],
                reverse=True
            )[:20])
        }

        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        print(f"Summary report saved to {output_path}")
