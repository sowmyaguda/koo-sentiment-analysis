# Quick Start Guide

Get started with KOO Sentiment Analysis in 5 minutes!

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Run Your First Analysis

### Option 1: Command Line (Easiest)

```bash
# Analyze 100 sample posts and generate visualizations
python main.py --mode sample --num-posts 100 --visualize
```

Results will be saved in `outputs/` directory.

### Option 2: Web Dashboard (Interactive)

```bash
# Launch the dashboard
streamlit run src/dashboard/app.py
```

Then:
1. Open your browser to `http://localhost:8501`
2. Click "Load Sample Data" in the sidebar
3. Click "Generate Sample Data"
4. Explore the visualizations and statistics!

### Option 3: Python Script (Programmatic)

```python
from src.scraper.koo_scraper import KooScraper
from src.sentiment.analyzer import SentimentAnalyzer
from src.utils.config_loader import load_config

# Generate sample data
scraper = KooScraper()
posts = scraper.create_sample_data(num_posts=50)

# Analyze sentiment
config = load_config()
analyzer = SentimentAnalyzer(config.get('sentiment', {}))
results = analyzer.analyze_posts(posts)

# Print results
for result in results[:5]:
    print(f"Text: {result['text'][:50]}...")
    print(f"Sentiment: {result['sentiment']} ({result['confidence']:.1%})")
    print()
```

## Analyze Your Own Text

```python
from src.sentiment.analyzer import SentimentAnalyzer
from src.scraper.data_models import KooPost
from datetime import datetime

# Initialize
analyzer = SentimentAnalyzer()

# Create a post
post = KooPost(
    post_id="1",
    text="This is an amazing product! I absolutely love it!",
    author="user",
    timestamp=datetime.now()
)

# Analyze
result = analyzer.analyze_post(post)

print(f"Sentiment: {result['sentiment']}")
print(f"Confidence: {result['confidence']:.2%}")
```

## Generate Visualizations

```python
from src.visualization.charts import SentimentCharts

# Create charts from your results
charts = SentimentCharts(results)

# Generate all visualizations
charts.create_dashboard('outputs/visualizations')

print("Visualizations saved to outputs/visualizations/")
```

## What's Next?

- Read the full [README.md](README.md) for detailed information
- Check out [USAGE_GUIDE.md](USAGE_GUIDE.md) for advanced usage
- Explore examples in the `examples/` directory
- Customize settings in `config/config.yaml`

## Common Commands

```bash
# Run with sample data
python main.py --mode sample --num-posts 100

# Run with visualizations
python main.py --mode sample --visualize

# Launch dashboard
streamlit run src/dashboard/app.py

# Run examples
python examples/basic_usage.py
python examples/analyze_custom_text.py

# Clean cache
make clean
```

## Need Help?

- Check [README.md](README.md) for full documentation
- See [USAGE_GUIDE.md](USAGE_GUIDE.md) for detailed usage examples
- Open an issue on GitHub for bugs or questions

Happy analyzing!
