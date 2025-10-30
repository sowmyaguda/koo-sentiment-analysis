"""
Quick Demo of KOO Sentiment Analysis
"""

import sys
from pathlib import Path
from datetime import datetime

sys.path.append(str(Path(__file__).parent))

from src.scraper.koo_scraper import KooScraper
from src.sentiment.analyzer import SentimentAnalyzer
from src.utils.config_loader import load_config

print("=" * 70)
print("KOO MULTILINGUAL SENTIMENT ANALYSIS - DEMO")
print("=" * 70)
print()

# Step 1: Create sample data
print("[1/3] Creating sample posts...")
scraper = KooScraper()
posts = scraper.create_sample_data(num_posts=20)
print(f"✓ Created {len(posts)} sample posts in English, Hindi, and Tamil")
print()

# Show some samples
print("Sample Posts:")
for i, post in enumerate(posts[:3], 1):
    print(f"{i}. [{post.language}] {post.text[:60]}...")
print()

# Step 2: Initialize analyzer
print("[2/3] Initializing sentiment analyzer...")
print("Loading transformer model (this may take a moment on first run)...")
config = load_config()
analyzer = SentimentAnalyzer(config.get('sentiment', {}))
print("✓ Analyzer ready!")
print()

# Step 3: Analyze sentiment
print("[3/3] Analyzing sentiment...")
results = analyzer.analyze_posts(posts, show_progress=True)
print()

# Display results
print("=" * 70)
print("ANALYSIS RESULTS")
print("=" * 70)
print()

print("Sample Results:")
print("-" * 70)
for i, result in enumerate(results[:5], 1):
    text = result['text'][:50] + "..." if len(result['text']) > 50 else result['text']
    print(f"\nPost {i}:")
    print(f"  Text: {text}")
    print(f"  Language: {result['language'].upper()}")
    print(f"  Sentiment: {result['sentiment'].upper()}")
    print(f"  Confidence: {result['confidence']*100:.1f}%")
    print(f"  Score: {result['sentiment_score']:.3f}")

print()
print("=" * 70)
print("OVERALL STATISTICS")
print("=" * 70)

stats = analyzer.get_statistics()
print(f"\nTotal Posts Analyzed: {stats['total_posts']}")
print(f"Average Sentiment Score: {stats['average_sentiment_score']:.3f}")
print(f"Average Confidence: {stats['average_confidence']*100:.1f}%")
print()

print("Sentiment Distribution:")
for sentiment, count in sorted(stats['sentiment_distribution'].items()):
    percentage = (count / stats['total_posts']) * 100
    bar = "█" * int(percentage / 5)
    print(f"  {sentiment:15s}: {count:2d} ({percentage:5.1f}%) {bar}")

print()
print("=" * 70)
print("DEMO COMPLETE!")
print("=" * 70)
print()
print("Next steps:")
print("  • Run full analysis: python main.py --mode sample --num-posts 100 --visualize")
print("  • Launch dashboard: streamlit run src/dashboard/app.py")
print("  • Check the documentation: README.md")
