"""
Basic Usage Example for KOO Sentiment Analysis
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from src.scraper.koo_scraper import KooScraper
from src.sentiment.analyzer import SentimentAnalyzer
from src.utils.config_loader import load_config


def main():
    """Basic usage example"""

    print("KOO Sentiment Analysis - Basic Example")
    print("=" * 50)
    print()

    # 1. Create sample data
    print("Step 1: Creating sample posts...")
    scraper = KooScraper()
    posts = scraper.create_sample_data(num_posts=20)
    print(f"Created {len(posts)} sample posts")
    print()

    # 2. Initialize analyzer
    print("Step 2: Initializing sentiment analyzer...")
    config = load_config()
    analyzer = SentimentAnalyzer(config.get('sentiment', {}))
    print("Analyzer ready")
    print()

    # 3. Analyze posts
    print("Step 3: Analyzing sentiment...")
    results = analyzer.analyze_posts(posts, show_progress=True)
    print(f"Analyzed {len(results)} posts")
    print()

    # 4. Display some results
    print("Step 4: Sample Results")
    print("-" * 50)
    for i, result in enumerate(results[:5], 1):
        print(f"\nPost {i}:")
        print(f"  Text: {result['text'][:60]}...")
        print(f"  Language: {result['language']}")
        print(f"  Sentiment: {result['sentiment']}")
        print(f"  Confidence: {result['confidence']:.2%}")
        print(f"  Score: {result['sentiment_score']:.3f}")

    print()
    print("-" * 50)

    # 5. Get statistics
    print("\nStep 5: Overall Statistics")
    print("-" * 50)
    stats = analyzer.get_statistics()

    print(f"Total Posts: {stats['total_posts']}")
    print(f"Average Sentiment Score: {stats['average_sentiment_score']:.3f}")
    print()

    print("Sentiment Distribution:")
    for sentiment, count in stats['sentiment_distribution'].items():
        print(f"  {sentiment}: {count}")

    print()
    print("=" * 50)
    print("Example complete!")


if __name__ == "__main__":
    main()
