# Usage Guide

This guide provides detailed instructions on how to use the KOO Multilingual Sentiment Analysis tool.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Data Collection](#data-collection)
3. [Sentiment Analysis](#sentiment-analysis)
4. [Visualizations](#visualizations)
5. [Web Dashboard](#web-dashboard)
6. [Advanced Usage](#advanced-usage)

## Getting Started

### Installation

```bash
# Clone repository
git clone <repository-url>
cd Analysis

# Install dependencies
pip install -r requirements.txt
```

### Quick Test

Run a quick test to ensure everything is working:

```bash
python examples/basic_usage.py
```

## Data Collection

### Method 1: Sample Data

Generate sample data for testing:

```python
from src.scraper.koo_scraper import KooScraper

scraper = KooScraper()
posts = scraper.create_sample_data(num_posts=100)
```

### Method 2: Load from File

Load posts from a JSON file:

```python
scraper = KooScraper()
posts = scraper.load_from_file('path/to/posts.json')
```

Expected JSON format:

```json
[
  {
    "id": "post_1",
    "text": "Your post text here",
    "author": "username",
    "timestamp": "2024-01-01T12:00:00",
    "language": "en",
    "likes": 100,
    "reposts": 20,
    "comments": 15
  }
]
```

### Method 3: Custom Scraping

Adapt the scraper for your needs:

```python
from src.scraper.data_models import KooPost
from datetime import datetime

# Create posts manually
post = KooPost(
    post_id="custom_1",
    text="Your text here",
    author="username",
    timestamp=datetime.now(),
    language="en"
)
```

## Sentiment Analysis

### Basic Analysis

```python
from src.sentiment.analyzer import SentimentAnalyzer
from src.utils.config_loader import load_config

# Initialize
config = load_config()
analyzer = SentimentAnalyzer(config.get('sentiment', {}))

# Analyze posts
results = analyzer.analyze_posts(posts)

# View results
for result in results[:5]:
    print(f"Text: {result['text']}")
    print(f"Sentiment: {result['sentiment']}")
    print(f"Confidence: {result['confidence']:.2%}")
    print()
```

### Single Post Analysis

```python
post = KooPost(
    post_id="1",
    text="This is amazing!",
    author="user",
    timestamp=datetime.now()
)

result = analyzer.analyze_post(post)
print(result)
```

### Batch Analysis with Progress

```python
results = analyzer.analyze_posts(posts, show_progress=True)
```

### Get Statistics

```python
stats = analyzer.get_statistics()

print(f"Total Posts: {stats['total_posts']}")
print(f"Avg Sentiment: {stats['average_sentiment_score']}")
print(f"Distribution: {stats['sentiment_distribution']}")
```

### Hashtag Analysis

```python
hashtag_stats = analyzer.analyze_hashtags()

for hashtag, data in hashtag_stats.items():
    print(f"#{hashtag}: {data['count']} posts")
    print(f"  Avg sentiment: {data['average_sentiment_score']:.3f}")
```

### Save Results

```python
# Save as JSON
analyzer.save_results('outputs/results.json', format='json')

# Save as CSV
analyzer.save_results('outputs/results.csv', format='csv')

# Save summary report
analyzer.export_summary_report('outputs/summary.json')
```

## Visualizations

### Sentiment Distribution

```python
from src.visualization.charts import SentimentCharts

charts = SentimentCharts(results)

# Static plot
charts.plot_sentiment_distribution(save_path='sentiment_dist.png')

# Interactive plot
charts.plot_sentiment_distribution(save_path='sentiment_dist.html', use_plotly=True)
```

### Sentiment by Language

```python
charts.plot_sentiment_by_language(save_path='by_language.png')
```

### Sentiment Timeline

```python
charts.plot_sentiment_timeline(save_path='timeline.png')
```

### Engagement Analysis

```python
charts.plot_engagement_by_sentiment(save_path='engagement.png')
```

### Top Hashtags

```python
charts.plot_top_hashtags(top_n=20, save_path='hashtags.png')
```

### Complete Dashboard

Generate all visualizations at once:

```python
charts.create_dashboard('outputs/visualizations')
```

### Word Clouds

```python
from src.visualization.wordcloud_generator import WordCloudGenerator

wc_gen = WordCloudGenerator(results)

# Overall word cloud
wc_gen.generate_overall_wordcloud(save_path='wordcloud.png')

# Word clouds by sentiment
wc_gen.generate_sentiment_wordclouds(save_dir='wordclouds/')

# Hashtag word cloud
wc_gen.generate_hashtag_wordcloud(save_path='hashtag_cloud.png')

# Word clouds by language
wc_gen.generate_language_wordclouds(save_dir='language_clouds/')
```

## Web Dashboard

### Launch Dashboard

```bash
streamlit run src/dashboard/app.py
```

Or with custom port:

```bash
streamlit run src/dashboard/app.py --server.port 8080
```

### Dashboard Features

1. **Home Page**
   - Overview of the tool
   - Feature descriptions

2. **Data Analysis**
   - View analyzed data
   - Filter by sentiment and language
   - Sample data display

3. **Visualizations**
   - Interactive charts
   - Generate word clouds on demand

4. **Live Analysis**
   - Enter custom text
   - Get real-time sentiment analysis
   - Support for all languages

5. **Statistics**
   - Overall statistics
   - Language-wise breakdown
   - Top posts

### Dashboard Data Loading

The dashboard supports three data loading methods:

1. **Upload File**: Upload JSON results file
2. **Load Sample Data**: Generate sample data on the fly
3. **Use Existing Results**: Load from `data/processed/` directory

## Advanced Usage

### Custom Model Configuration

```python
# Use a different model
custom_config = {
    'model_name': 'cardiffnlp/twitter-xlm-roberta-base-sentiment',
    'device': 'cuda',  # Use GPU
    'batch_size': 32
}

analyzer = SentimentAnalyzer(custom_config)
```

### Language Detection

```python
from src.utils.language_detector import LanguageDetector

detector = LanguageDetector()

# Detect language
lang = detector.detect("Your text here")
print(f"Language: {lang}")

# Get language with confidence
langs = detector.detect_with_confidence("Your text here")
for lang_info in langs:
    print(f"{lang_info['lang']}: {lang_info['prob']:.2%}")

# Check if multilingual
is_multi = detector.is_multilingual("Text with multiple languages")
```

### Text Preprocessing

```python
from src.utils.text_preprocessor import TextPreprocessor

preprocessor = TextPreprocessor()

# Clean text
clean = preprocessor.clean_text(
    text,
    remove_urls=True,
    remove_mentions=True,
    remove_emojis=False
)

# Extract features
hashtags = preprocessor.extract_hashtags(text)
mentions = preprocessor.extract_mentions(text)
urls = preprocessor.extract_urls(text)
```

### Filtering Results

```python
import pandas as pd

df = pd.DataFrame(results)

# Filter by sentiment
positive_posts = df[df['sentiment'] == 'positive']

# Filter by language
hindi_posts = df[df['language'] == 'hi']

# Filter by confidence
high_confidence = df[df['confidence'] > 0.8]

# Multiple filters
filtered = df[
    (df['sentiment'] == 'positive') &
    (df['language'] == 'en') &
    (df['confidence'] > 0.7)
]
```

### Exporting Specific Data

```python
# Export only positive sentiments
positive_results = [r for r in results if r['sentiment'] == 'positive']

import json
with open('positive_only.json', 'w') as f:
    json.dump(positive_results, f, indent=2)
```

### Programmatic Dashboard Access

```python
import subprocess

# Launch dashboard programmatically
process = subprocess.Popen([
    'streamlit', 'run',
    'src/dashboard/app.py',
    '--server.port', '8501'
])

# Stop dashboard later
process.terminate()
```

## Command Line Usage

### Using main.py

```bash
# Sample data with visualizations
python main.py --mode sample --num-posts 200 --visualize

# Analyze file
python main.py --mode file --input data.json --visualize

# Custom output directory
python main.py --mode sample --output-dir my_results

# Launch dashboard after analysis
python main.py --mode sample --dashboard
```

### Using Makefile

```bash
# Install dependencies
make install

# Run basic analysis
make run

# Launch dashboard
make dashboard

# Generate visualizations
make visualize

# Run tests
make test

# Clean cache
make clean
```

## Tips and Best Practices

1. **Always use virtual environment** to avoid dependency conflicts

2. **Start with sample data** to test your workflow

3. **Use GPU if available** for faster processing (set `device: "cuda"`)

4. **Monitor memory usage** when processing large datasets

5. **Save intermediate results** to avoid reprocessing

6. **Use appropriate batch size** based on your hardware

7. **Verify language detection** for mixed-language content

8. **Check confidence scores** to filter unreliable predictions

9. **Use visualizations** to quickly understand patterns

10. **Export results regularly** to preserve your analysis

## Troubleshooting

### Common Issues

**Issue**: Slow model loading
- **Solution**: Models download on first use; subsequent runs are faster

**Issue**: Memory error
- **Solution**: Reduce batch_size or use smaller model

**Issue**: Incorrect language detection
- **Solution**: Manually specify language in post object

**Issue**: Dashboard won't start
- **Solution**: Check if port 8501 is available

**Issue**: Poor sentiment accuracy
- **Solution**: Try different models or ensure text is clean

## Next Steps

- Explore the examples in `examples/` directory
- Modify `config/config.yaml` for your needs
- Check the main README for more information
- Join the community for support

---

Happy Analyzing!
