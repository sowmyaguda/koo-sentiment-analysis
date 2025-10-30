"""
Charts and Visualizations for Sentiment Analysis
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import List, Dict
from pathlib import Path
import json


class SentimentCharts:
    """
    Create various charts and visualizations for sentiment analysis results
    """

    def __init__(self, results: List[Dict] = None, style: str = 'seaborn-v0_8-darkgrid'):
        """
        Initialize chart generator

        Args:
            results: List of sentiment analysis results
            style: Matplotlib style
        """
        self.results = results or []
        self.df = pd.DataFrame(results) if results else None

        # Set style
        try:
            plt.style.use(style)
        except:
            pass  # Use default if style not available

        sns.set_palette("husl")

    def load_results(self, file_path: str):
        """Load results from JSON file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            self.results = json.load(f)
        self.df = pd.DataFrame(self.results)

    def plot_sentiment_distribution(self, save_path: str = None, use_plotly: bool = False):
        """
        Plot sentiment distribution pie chart

        Args:
            save_path: Path to save the figure
            use_plotly: Use plotly for interactive chart
        """
        if self.df is None or self.df.empty:
            print("No data to visualize")
            return

        sentiment_counts = self.df['sentiment'].value_counts()

        if use_plotly:
            fig = px.pie(
                values=sentiment_counts.values,
                names=sentiment_counts.index,
                title='Sentiment Distribution',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')

            if save_path:
                fig.write_html(save_path)
            else:
                fig.show()
        else:
            plt.figure(figsize=(10, 6))
            colors = sns.color_palette('pastel')
            plt.pie(sentiment_counts.values, labels=sentiment_counts.index,
                   autopct='%1.1f%%', startangle=90, colors=colors)
            plt.title('Sentiment Distribution', fontsize=16, fontweight='bold')

            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
            else:
                plt.show()
            plt.close()

    def plot_sentiment_by_language(self, save_path: str = None, use_plotly: bool = False):
        """
        Plot sentiment distribution by language

        Args:
            save_path: Path to save the figure
            use_plotly: Use plotly for interactive chart
        """
        if self.df is None or self.df.empty:
            print("No data to visualize")
            return

        # Create cross-tabulation
        lang_sentiment = pd.crosstab(self.df['language'], self.df['sentiment'])

        if use_plotly:
            fig = px.bar(
                lang_sentiment,
                barmode='group',
                title='Sentiment Distribution by Language',
                labels={'value': 'Count', 'language': 'Language'},
                color_discrete_sequence=px.colors.qualitative.Pastel
            )

            if save_path:
                fig.write_html(save_path)
            else:
                fig.show()
        else:
            fig, ax = plt.subplots(figsize=(12, 6))
            lang_sentiment.plot(kind='bar', ax=ax, width=0.8)
            plt.title('Sentiment Distribution by Language', fontsize=16, fontweight='bold')
            plt.xlabel('Language', fontsize=12)
            plt.ylabel('Count', fontsize=12)
            plt.legend(title='Sentiment', bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()

            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
            else:
                plt.show()
            plt.close()

    def plot_sentiment_timeline(self, save_path: str = None, use_plotly: bool = False):
        """
        Plot sentiment over time

        Args:
            save_path: Path to save the figure
            use_plotly: Use plotly for interactive chart
        """
        if self.df is None or self.df.empty:
            print("No data to visualize")
            return

        # Convert timestamp to datetime
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
        self.df['date'] = self.df['timestamp'].dt.date

        # Group by date and sentiment
        timeline_data = self.df.groupby(['date', 'sentiment']).size().unstack(fill_value=0)

        if use_plotly:
            fig = go.Figure()
            for sentiment in timeline_data.columns:
                fig.add_trace(go.Scatter(
                    x=timeline_data.index,
                    y=timeline_data[sentiment],
                    name=sentiment,
                    mode='lines+markers'
                ))

            fig.update_layout(
                title='Sentiment Timeline',
                xaxis_title='Date',
                yaxis_title='Number of Posts',
                hovermode='x unified'
            )

            if save_path:
                fig.write_html(save_path)
            else:
                fig.show()
        else:
            fig, ax = plt.subplots(figsize=(14, 6))
            timeline_data.plot(ax=ax, marker='o')
            plt.title('Sentiment Timeline', fontsize=16, fontweight='bold')
            plt.xlabel('Date', fontsize=12)
            plt.ylabel('Number of Posts', fontsize=12)
            plt.legend(title='Sentiment')
            plt.xticks(rotation=45, ha='right')
            plt.grid(True, alpha=0.3)
            plt.tight_layout()

            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
            else:
                plt.show()
            plt.close()

    def plot_engagement_by_sentiment(self, save_path: str = None, use_plotly: bool = False):
        """
        Plot engagement metrics by sentiment

        Args:
            save_path: Path to save the figure
            use_plotly: Use plotly for interactive chart
        """
        if self.df is None or self.df.empty:
            print("No data to visualize")
            return

        engagement = self.df.groupby('sentiment')[['likes', 'reposts', 'comments']].mean()

        if use_plotly:
            fig = go.Figure()
            for metric in ['likes', 'reposts', 'comments']:
                fig.add_trace(go.Bar(
                    name=metric.capitalize(),
                    x=engagement.index,
                    y=engagement[metric]
                ))

            fig.update_layout(
                title='Average Engagement by Sentiment',
                xaxis_title='Sentiment',
                yaxis_title='Average Count',
                barmode='group'
            )

            if save_path:
                fig.write_html(save_path)
            else:
                fig.show()
        else:
            fig, ax = plt.subplots(figsize=(10, 6))
            engagement.plot(kind='bar', ax=ax, width=0.8)
            plt.title('Average Engagement by Sentiment', fontsize=16, fontweight='bold')
            plt.xlabel('Sentiment', fontsize=12)
            plt.ylabel('Average Count', fontsize=12)
            plt.legend(title='Metric')
            plt.xticks(rotation=0)
            plt.tight_layout()

            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
            else:
                plt.show()
            plt.close()

    def plot_top_hashtags(self, top_n: int = 20, save_path: str = None, use_plotly: bool = False):
        """
        Plot top hashtags with sentiment breakdown

        Args:
            top_n: Number of top hashtags to show
            save_path: Path to save the figure
            use_plotly: Use plotly for interactive chart
        """
        if self.df is None or self.df.empty:
            print("No data to visualize")
            return

        # Explode hashtags
        hashtag_data = []
        for _, row in self.df.iterrows():
            for hashtag in row['hashtags']:
                hashtag_data.append({
                    'hashtag': hashtag,
                    'sentiment': row['sentiment']
                })

        if not hashtag_data:
            print("No hashtags found")
            return

        hashtag_df = pd.DataFrame(hashtag_data)
        top_hashtags = hashtag_df['hashtag'].value_counts().head(top_n).index

        # Filter and create cross-tab
        filtered = hashtag_df[hashtag_df['hashtag'].isin(top_hashtags)]
        hashtag_sentiment = pd.crosstab(filtered['hashtag'], filtered['sentiment'])

        if use_plotly:
            fig = px.bar(
                hashtag_sentiment.reset_index(),
                x='hashtag',
                y=hashtag_sentiment.columns.tolist(),
                title=f'Top {top_n} Hashtags by Sentiment',
                labels={'value': 'Count', 'hashtag': 'Hashtag'},
                barmode='stack'
            )

            if save_path:
                fig.write_html(save_path)
            else:
                fig.show()
        else:
            fig, ax = plt.subplots(figsize=(14, 6))
            hashtag_sentiment.plot(kind='barh', stacked=True, ax=ax)
            plt.title(f'Top {top_n} Hashtags by Sentiment', fontsize=16, fontweight='bold')
            plt.xlabel('Count', fontsize=12)
            plt.ylabel('Hashtag', fontsize=12)
            plt.legend(title='Sentiment', bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.tight_layout()

            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
            else:
                plt.show()
            plt.close()

    def plot_sentiment_score_distribution(self, save_path: str = None):
        """
        Plot distribution of sentiment scores

        Args:
            save_path: Path to save the figure
        """
        if self.df is None or self.df.empty:
            print("No data to visualize")
            return

        fig, axes = plt.subplots(1, 2, figsize=(14, 5))

        # Histogram
        axes[0].hist(self.df['sentiment_score'], bins=30, color='skyblue', edgecolor='black')
        axes[0].set_title('Sentiment Score Distribution', fontsize=14, fontweight='bold')
        axes[0].set_xlabel('Sentiment Score', fontsize=12)
        axes[0].set_ylabel('Frequency', fontsize=12)
        axes[0].axvline(x=0, color='red', linestyle='--', label='Neutral')
        axes[0].legend()

        # Box plot by sentiment category
        sentiment_order = ['very negative', 'negative', 'neutral', 'positive', 'very positive']
        available_sentiments = [s for s in sentiment_order if s in self.df['sentiment'].unique()]

        sns.boxplot(data=self.df, x='sentiment', y='sentiment_score',
                   order=available_sentiments, ax=axes[1])
        axes[1].set_title('Sentiment Scores by Category', fontsize=14, fontweight='bold')
        axes[1].set_xlabel('Sentiment Category', fontsize=12)
        axes[1].set_ylabel('Sentiment Score', fontsize=12)
        axes[1].tick_params(axis='x', rotation=45)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()
        plt.close()

    def create_dashboard(self, output_dir: str):
        """
        Create a complete dashboard with all visualizations

        Args:
            output_dir: Directory to save all visualizations
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        print("Generating sentiment analysis dashboard...")

        # Generate all plots
        self.plot_sentiment_distribution(
            save_path=str(output_path / 'sentiment_distribution.png')
        )
        print("✓ Sentiment distribution")

        self.plot_sentiment_by_language(
            save_path=str(output_path / 'sentiment_by_language.png')
        )
        print("✓ Sentiment by language")

        self.plot_sentiment_timeline(
            save_path=str(output_path / 'sentiment_timeline.png')
        )
        print("✓ Sentiment timeline")

        self.plot_engagement_by_sentiment(
            save_path=str(output_path / 'engagement_by_sentiment.png')
        )
        print("✓ Engagement by sentiment")

        self.plot_top_hashtags(
            save_path=str(output_path / 'top_hashtags.png')
        )
        print("✓ Top hashtags")

        self.plot_sentiment_score_distribution(
            save_path=str(output_path / 'sentiment_score_distribution.png')
        )
        print("✓ Sentiment score distribution")

        print(f"\nDashboard created successfully in: {output_dir}")
