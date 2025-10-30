"""
Quick Demo - Shows sentiment analysis in action
"""

import sys
from pathlib import Path
from datetime import datetime

sys.path.append(str(Path(__file__).parent))

print("\n" + "="*70)
print("KOO MULTILINGUAL SENTIMENT ANALYSIS - LIVE DEMO")
print("="*70 + "\n")

# Step 1: Generate sample data
print("[STEP 1/4] Generating sample posts...")
print("-"*70)

from src.scraper.koo_scraper import KooScraper

scraper = KooScraper()
posts = scraper.create_sample_data(num_posts=15)

print(f"[SUCCESS] Generated {len(posts)} sample posts\n")

# Show sample posts
print("Sample Posts:")
for i, post in enumerate(posts[:5], 1):
    lang_name = {"en": "English", "hi": "Hindi", "ta": "Tamil"}.get(post.language, post.language)
    print(f"\n  {i}. [{lang_name}]")
    print(f"     {post.text}")
    print(f"     Author: {post.author} | Likes: {post.likes} | Reposts: {post.reposts}")

print("\n" + "="*70)
print("[STEP 2/4] Initializing AI Model...")
print("-"*70)
print("Loading BERT multilingual sentiment model...")
print("(This may take 1-2 minutes on first run to download ~500MB model)")

from src.sentiment.analyzer import SentimentAnalyzer
from src.utils.config_loader import load_config

config = load_config()
analyzer = SentimentAnalyzer(config.get('sentiment', {}))

print("[SUCCESS] Model loaded and ready!\n")

print("="*70)
print("[STEP 3/4] Analyzing Sentiment...")
print("-"*70)

results = analyzer.analyze_posts(posts, show_progress=True)

print("\n[SUCCESS] Analysis complete!\n")

print("="*70)
print("[STEP 4/4] RESULTS")
print("="*70 + "\n")

# Show detailed results
print("DETAILED ANALYSIS RESULTS:")
print("-"*70)

for i, result in enumerate(results[:10], 1):
    text = result['text'][:60] + "..." if len(result['text']) > 60 else result['text']

    # Color sentiment score
    score = result['sentiment_score']
    score_bar = "█" * int(abs(score) * 10)

    print(f"\n{i}. Text: {text}")
    print(f"   Language: {result['language'].upper()}")
    print(f"   Sentiment: {result['sentiment'].upper()}")
    print(f"   Confidence: {result['confidence']*100:.1f}%")
    print(f"   Score: {score:+.3f} {score_bar}")

print("\n" + "="*70)
print("OVERALL STATISTICS")
print("="*70 + "\n")

stats = analyzer.get_statistics()

print(f"Total Posts Analyzed: {stats['total_posts']}")
print(f"Average Sentiment Score: {stats['average_sentiment_score']:+.3f}")
print(f"Average Confidence: {stats['average_confidence']*100:.1f}%\n")

print("Sentiment Distribution:")
print("-"*70)
for sentiment, count in sorted(stats['sentiment_distribution'].items()):
    percentage = (count / stats['total_posts']) * 100
    bar = "█" * int(percentage / 3)
    print(f"  {sentiment:15s}: {count:2d} posts ({percentage:5.1f}%) {bar}")

print("\n" + "="*70)
print("TOP POSTS")
print("="*70 + "\n")

print("MOST POSITIVE POST:")
print(f"   {stats['most_positive_post']['text']}")
print(f"   Score: {stats['most_positive_post']['sentiment_score']:+.3f}\n")

print("MOST NEGATIVE POST:")
print(f"   {stats['most_negative_post']['text']}")
print(f"   Score: {stats['most_negative_post']['sentiment_score']:+.3f}\n")

# Hashtag analysis
print("="*70)
print("HASHTAG ANALYSIS")
print("="*70 + "\n")

hashtag_stats = analyzer.analyze_hashtags()
top_hashtags = sorted(hashtag_stats.items(), key=lambda x: x[1]['count'], reverse=True)[:5]

if top_hashtags:
    print("Top 5 Hashtags:")
    for hashtag, data in top_hashtags:
        avg_score = data['average_sentiment_score']
        sentiment = "Positive" if avg_score > 0.2 else "Negative" if avg_score < -0.2 else "Neutral"
        print(f"  #{hashtag:20s}: {data['count']} posts | {sentiment} ({avg_score:+.3f})")
else:
    print("  No hashtags found in sample data")

print("\n" + "="*70)
print("[SUCCESS] DEMO COMPLETE!")
print("="*70 + "\n")

# Save results
output_file = "outputs/reports/demo_results.json"
analyzer.save_results(output_file, format='json')
print(f"Results saved to: {output_file}\n")

print("WHAT'S NEXT?\n")
print("  1. Run full analysis:")
print("     python main.py --mode sample --num-posts 100 --visualize\n")
print("  2. Launch web dashboard:")
print("     streamlit run src/dashboard/app.py\n")
print("  3. Analyze your own text:")
print("     python examples/analyze_custom_text.py\n")
print("="*70 + "\n")
