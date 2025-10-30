"""
Word Cloud Generator for Sentiment Analysis
"""

from wordcloud import WordCloud
import matplotlib.pyplot as plt
from typing import List, Dict
from collections import Counter
from pathlib import Path
import pandas as pd


class WordCloudGenerator:
    """
    Generate word clouds from text data
    """

    def __init__(self, results: List[Dict] = None):
        """
        Initialize word cloud generator

        Args:
            results: List of sentiment analysis results
        """
        self.results = results or []
        self.df = pd.DataFrame(results) if results else None

    def generate_overall_wordcloud(self, save_path: str = None, max_words: int = 100):
        """
        Generate word cloud from all texts

        Args:
            save_path: Path to save the word cloud
            max_words: Maximum number of words to include
        """
        if not self.results:
            print("No data to generate word cloud")
            return

        # Combine all texts
        all_text = ' '.join([result['text'] for result in self.results])

        # Generate word cloud
        wordcloud = WordCloud(
            width=1200,
            height=600,
            background_color='white',
            max_words=max_words,
            colormap='viridis',
            relative_scaling=0.5,
            min_font_size=10
        ).generate(all_text)

        # Plot
        plt.figure(figsize=(14, 7))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('Overall Word Cloud', fontsize=20, fontweight='bold', pad=20)

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Word cloud saved to {save_path}")
        else:
            plt.show()
        plt.close()

    def generate_sentiment_wordclouds(self, save_dir: str = None, max_words: int = 100):
        """
        Generate separate word clouds for each sentiment

        Args:
            save_dir: Directory to save word clouds
            max_words: Maximum number of words per cloud
        """
        if self.df is None or self.df.empty:
            print("No data to generate word clouds")
            return

        sentiments = self.df['sentiment'].unique()
        n_sentiments = len(sentiments)

        fig, axes = plt.subplots(1, n_sentiments, figsize=(7 * n_sentiments, 6))
        if n_sentiments == 1:
            axes = [axes]

        # Color maps for different sentiments
        color_maps = {
            'very negative': 'Reds',
            'negative': 'OrRd',
            'neutral': 'Greys',
            'positive': 'YlGn',
            'very positive': 'Greens'
        }

        for idx, sentiment in enumerate(sentiments):
            # Get texts for this sentiment
            texts = self.df[self.df['sentiment'] == sentiment]['text'].tolist()
            combined_text = ' '.join(texts)

            # Generate word cloud
            colormap = color_maps.get(sentiment, 'viridis')
            wordcloud = WordCloud(
                width=800,
                height=600,
                background_color='white',
                max_words=max_words,
                colormap=colormap,
                relative_scaling=0.5,
                min_font_size=10
            ).generate(combined_text)

            # Plot
            axes[idx].imshow(wordcloud, interpolation='bilinear')
            axes[idx].axis('off')
            axes[idx].set_title(f'{sentiment.capitalize()}', fontsize=16, fontweight='bold')

        plt.tight_layout()

        if save_dir:
            save_path = Path(save_dir)
            save_path.mkdir(parents=True, exist_ok=True)
            output_file = save_path / 'sentiment_wordclouds.png'
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            print(f"Sentiment word clouds saved to {output_file}")
        else:
            plt.show()
        plt.close()

    def generate_hashtag_wordcloud(self, save_path: str = None, max_words: int = 50):
        """
        Generate word cloud from hashtags

        Args:
            save_path: Path to save the word cloud
            max_words: Maximum number of hashtags to include
        """
        if not self.results:
            print("No data to generate word cloud")
            return

        # Collect all hashtags
        all_hashtags = []
        for result in self.results:
            all_hashtags.extend(result.get('hashtags', []))

        if not all_hashtags:
            print("No hashtags found")
            return

        # Count hashtag frequencies
        hashtag_counts = Counter(all_hashtags)

        # Create word cloud from frequencies
        wordcloud = WordCloud(
            width=1200,
            height=600,
            background_color='white',
            max_words=max_words,
            colormap='plasma',
            relative_scaling=0.5,
            min_font_size=12
        ).generate_from_frequencies(hashtag_counts)

        # Plot
        plt.figure(figsize=(14, 7))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('Hashtag Word Cloud', fontsize=20, fontweight='bold', pad=20)

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Hashtag word cloud saved to {save_path}")
        else:
            plt.show()
        plt.close()

    def generate_language_wordclouds(self, save_dir: str = None, max_words: int = 100):
        """
        Generate word clouds for each language

        Args:
            save_dir: Directory to save word clouds
            max_words: Maximum number of words per cloud
        """
        if self.df is None or self.df.empty:
            print("No data to generate word clouds")
            return

        languages = self.df['language'].unique()

        for lang in languages:
            # Get texts for this language
            texts = self.df[self.df['language'] == lang]['text'].tolist()
            combined_text = ' '.join(texts)

            # Generate word cloud
            wordcloud = WordCloud(
                width=1200,
                height=600,
                background_color='white',
                max_words=max_words,
                colormap='tab20',
                relative_scaling=0.5,
                min_font_size=10
            ).generate(combined_text)

            # Plot
            plt.figure(figsize=(14, 7))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            plt.title(f'Word Cloud - {lang.upper()}', fontsize=20, fontweight='bold', pad=20)

            if save_dir:
                save_path = Path(save_dir)
                save_path.mkdir(parents=True, exist_ok=True)
                output_file = save_path / f'wordcloud_{lang}.png'
                plt.savefig(output_file, dpi=300, bbox_inches='tight')
                print(f"Word cloud for {lang} saved to {output_file}")
            else:
                plt.show()
            plt.close()
