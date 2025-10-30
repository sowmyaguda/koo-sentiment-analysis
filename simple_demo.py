"""
Simple Demo - Shows data generation and preprocessing (no model download)
"""

import sys
from pathlib import Path
from datetime import datetime

sys.path.append(str(Path(__file__).parent))

print("\n" + "="*70)
print("KOO SENTIMENT ANALYSIS - QUICK PREVIEW")
print("="*70 + "\n")

# Step 1: Generate sample data
print("STEP 1: Generating Sample Posts")
print("-"*70)

from src.scraper.koo_scraper import KooScraper

scraper = KooScraper()
posts = scraper.create_sample_data(num_posts=20)

print(f"[SUCCESS] Generated {len(posts)} sample posts in multiple languages\n")

# Show all posts with details
print("SAMPLE POSTS:\n")

lang_names = {"en": "English", "hi": "Hindi", "ta": "Tamil"}

for i, post in enumerate(posts, 1):
    lang = lang_names.get(post.language, post.language.upper())

    print(f"{i}. {lang}")
    print(f"   Text: {post.text}")
    print(f"   Author: {post.author}")
    print(f"   Likes: {post.likes} | Reposts: {post.reposts} | Comments: {post.comments}")

    if post.hashtags:
        print(f"   Hashtags: {', '.join(['#' + h for h in post.hashtags])}")
    print()

# Step 2: Language Detection
print("="*70)
print("STEP 2: Language Detection")
print("-"*70 + "\n")

from src.utils.language_detector import LanguageDetector

detector = LanguageDetector()

lang_count = {}
for post in posts:
    lang = detector.detect(post.text)
    lang_name = detector.get_language_name(lang)
    lang_count[lang_name] = lang_count.get(lang_name, 0) + 1

print("Language Distribution:")
for lang, count in sorted(lang_count.items(), key=lambda x: x[1], reverse=True):
    percentage = (count / len(posts)) * 100
    bar = "█" * int(percentage / 5)
    print(f"  {lang:15s}: {count:2d} posts ({percentage:5.1f}%) {bar}")

# Step 3: Text Preprocessing
print("\n" + "="*70)
print("STEP 3: Text Preprocessing")
print("-"*70 + "\n")

from src.utils.text_preprocessor import TextPreprocessor

preprocessor = TextPreprocessor()

all_hashtags = []
all_mentions = []

for post in posts:
    hashtags = preprocessor.extract_hashtags(post.text)
    mentions = preprocessor.extract_mentions(post.text)
    all_hashtags.extend(hashtags)
    all_mentions.extend(mentions)

from collections import Counter

print("Top Hashtags:")
hashtag_counts = Counter(all_hashtags)
for hashtag, count in hashtag_counts.most_common(10):
    print(f"  #{hashtag:20s}: {count} times")

if all_mentions:
    print("\nMentioned Users:")
    mention_counts = Counter(all_mentions)
    for mention, count in mention_counts.most_common(5):
        print(f"  @{mention:15s}: {count} times")

# Step 4: Statistics
print("\n" + "="*70)
print("STEP 4: Engagement Statistics")
print("-"*70 + "\n")

total_likes = sum(p.likes for p in posts)
total_reposts = sum(p.reposts for p in posts)
total_comments = sum(p.comments for p in posts)

print(f"Total Engagement:")
print(f"   Likes: {total_likes}")
print(f"   Reposts: {total_reposts}")
print(f"   Comments: {total_comments}")
print(f"   Total: {total_likes + total_reposts + total_comments}\n")

print(f"Average per Post:")
print(f"   Avg Likes: {total_likes/len(posts):.1f}")
print(f"   Avg Reposts: {total_reposts/len(posts):.1f}")
print(f"   Avg Comments: {total_comments/len(posts):.1f}")

# Most engaged post
most_engaged = max(posts, key=lambda p: p.likes + p.reposts + p.comments)
print(f"\nMost Engaged Post:")
print(f"   {most_engaged.text[:70]}...")
print(f"   Total engagement: {most_engaged.likes + most_engaged.reposts + most_engaged.comments}")

# Save to file
print("\n" + "="*70)
print("SAVING DATA")
print("-"*70 + "\n")

scraper.posts = posts
scraper.save_posts("data/raw/sample_posts.json", format='json')
scraper.save_posts("data/raw/sample_posts.csv", format='csv')

print("[SUCCESS] Data saved to:")
print("   - data/raw/sample_posts.json")
print("   - data/raw/sample_posts.csv")

print("\n" + "="*70)
print("[SUCCESS] PREVIEW COMPLETE!")
print("="*70 + "\n")

print("WHAT YOU'VE SEEN:\n")
print("  [OK] Sample data generation in 3 languages (EN, HI, TA)")
print("  [OK] Automatic language detection")
print("  [OK] Text preprocessing (hashtags, mentions)")
print("  [OK] Engagement statistics")
print("  [OK] Data export (JSON/CSV)\n")

print("NEXT: Run Sentiment Analysis\n")
print("  The sentiment analysis uses BERT AI models that need to")
print("  download on first run (~500MB, takes 2-5 minutes).\n")
print("  After download, analysis is very fast!\n")
print("  Run: python quick_demo.py")
print("   or: python main.py --mode sample --num-posts 50\n")

print("  Or launch the web dashboard:")
print("  Run: streamlit run src/dashboard/app.py\n")

print("="*70 + "\n")
