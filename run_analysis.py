"""
Direct Terminal Demo - Sentiment Analysis
No web browser needed - runs directly in terminal!
"""

import sys
from pathlib import Path
from datetime import datetime

sys.path.append(str(Path(__file__).parent))

print("\n" + "="*70)
print("KOO SENTIMENT ANALYSIS - TERMINAL DEMO")
print("="*70 + "\n")

# Step 1: Generate Data
print("[1/3] Generating Sample Data...")
print("-"*70)

from src.scraper.koo_scraper import KooScraper

scraper = KooScraper()
posts = scraper.create_sample_data(num_posts=10)

print(f"[SUCCESS] Created {len(posts)} multilingual posts\n")

# Show samples
print("Sample Posts:\n")
for i, post in enumerate(posts[:5], 1):
    lang_name = {"en": "English", "hi": "Hindi", "ta": "Tamil"}.get(post.language, post.language)
    print(f"{i}. [{lang_name}]")
    print(f"   {post.text}")
    print(f"   Likes: {post.likes}\n")

# Step 2: Analyze Sentiment
print("\n" + "="*70)
print("[2/3] Running AI Sentiment Analysis...")
print("-"*70)
print("Loading BERT model (may take 1-2 min on first run)...")

from src.sentiment.analyzer import SentimentAnalyzer
from src.utils.config_loader import load_config

config = load_config()
analyzer = SentimentAnalyzer(config.get('sentiment', {}))

print("Analyzing sentiment...")
results = analyzer.analyze_posts(posts, show_progress=True)

print("\n[SUCCESS] Analysis Complete!\n")

# Step 3: Show Results
print("="*70)
print("[3/3] SENTIMENT ANALYSIS RESULTS")
print("="*70 + "\n")

for i, result in enumerate(results, 1):
    text = result['text'][:60] + "..." if len(result['text']) > 60 else result['text']

    print(f"{i}. {text}")
    print(f"   Language: {result['language'].upper()}")
    print(f"   Sentiment: {result['sentiment'].upper()}")
    print(f"   Confidence: {result['confidence']*100:.1f}%")
    print(f"   Score: {result['sentiment_score']:+.3f}")
    print()

# Statistics
print("="*70)
print("STATISTICS")
print("="*70 + "\n")

stats = analyzer.get_statistics()

print(f"Total Posts: {stats['total_posts']}")
print(f"Avg Sentiment Score: {stats['average_sentiment_score']:+.3f}")
print(f"Avg Confidence: {stats['average_confidence']*100:.1f}%\n")

print("Sentiment Distribution:")
for sentiment, count in sorted(stats['sentiment_distribution'].items()):
    percentage = (count / stats['total_posts']) * 100
    bar = "█" * int(percentage / 5)
    print(f"  {sentiment:15s}: {count:2d} ({percentage:5.1f}%) {bar}")

print("\n" + "="*70)
print("[SUCCESS] DEMO COMPLETE!")
print("="*70 + "\n")

print("Results saved to: outputs/reports/")
analyzer.save_results("outputs/reports/terminal_demo_results.json", format='json')
print("\n[SUCCESS] Your sentiment analysis system is working perfectly!\n")
