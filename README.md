# KOO Multilingual Sentiment Analysis

A comprehensive sentiment analysis tool for analyzing social media posts from the KOO platform with support for multiple Indian languages. This project uses state-of-the-art transformer-based models (BERT) to perform accurate multilingual sentiment analysis.

## Features

- **Multilingual Support**: Analyze posts in 10+ languages including English, Hindi, Tamil, Telugu, Bengali, Marathi, Kannada, Gujarati, Malayalam, and Punjabi
- **Advanced NLP**: Uses transformer-based models (mBERT, XLM-RoBERTa) for high-accuracy sentiment detection
- **Rich Visualizations**: Generate beautiful charts, graphs, and word clouds
- **Interactive Dashboard**: Web-based dashboard built with Streamlit for real-time analysis
- **Statistical Reports**: Comprehensive statistical analysis and reports
- **Flexible Data Input**: Support for sample data, file uploads, and custom text analysis
- **Export Capabilities**: Export results in JSON and CSV formats

## Project Structure

```
Analysis/
├── config/                 # Configuration files
│   └── config.yaml        # Main configuration
├── data/                  # Data directory
│   ├── raw/              # Raw scraped data
│   └── processed/        # Processed analysis results
├── src/                   # Source code
│   ├── scraper/          # Data scraping module
│   ├── sentiment/        # Sentiment analysis module
│   ├── visualization/    # Visualization module
│   ├── dashboard/        # Web dashboard
│   └── utils/            # Utility functions
├── models/               # Trained models cache
├── outputs/              # Output directory
│   ├── reports/         # Analysis reports
│   └── visualizations/  # Generated charts and graphs
├── examples/            # Example scripts
├── main.py              # Main execution script
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- (Optional) CUDA-compatible GPU for faster processing

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd Analysis
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

Or use the Makefile:
```bash
make install
```

4. (Optional) Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Quick Start

### 1. Basic Usage

Run the main script with sample data:

```bash
python main.py --mode sample --num-posts 100 --visualize
```

This will:
- Generate 100 sample posts
- Analyze their sentiment
- Generate visualizations
- Save results to `outputs/`

### 2. Launch Web Dashboard

```bash
streamlit run src/dashboard/app.py
```

Or use the Makefile:
```bash
make dashboard
```

The dashboard will open at `http://localhost:8501`

### 3. Run Example Scripts

Basic usage example:
```bash
python examples/basic_usage.py
```

Analyze custom text:
```bash
python examples/analyze_custom_text.py
```

## Usage Examples

### Analyze Sample Data

```python
from src.scraper.koo_scraper import KooScraper
from src.sentiment.analyzer import SentimentAnalyzer
from src.utils.config_loader import load_config

# Create sample data
scraper = KooScraper()
posts = scraper.create_sample_data(num_posts=50)

# Analyze sentiment
config = load_config()
analyzer = SentimentAnalyzer(config.get('sentiment', {}))
results = analyzer.analyze_posts(posts)

# Get statistics
stats = analyzer.get_statistics()
print(stats)
```

### Analyze Custom Text

```python
from src.sentiment.analyzer import SentimentAnalyzer
from src.scraper.data_models import KooPost
from datetime import datetime

# Initialize analyzer
analyzer = SentimentAnalyzer()

# Create a post
post = KooPost(
    post_id="1",
    text="This is an amazing product! I love it!",
    author="user1",
    timestamp=datetime.now()
)

# Analyze
result = analyzer.analyze_post(post)
print(f"Sentiment: {result['sentiment']}")
print(f"Confidence: {result['confidence']:.2%}")
```

### Generate Visualizations

```python
from src.visualization.charts import SentimentCharts
from src.visualization.wordcloud_generator import WordCloudGenerator

# Create charts
charts = SentimentCharts(results)
charts.plot_sentiment_distribution(save_path='sentiment_dist.png')
charts.plot_sentiment_by_language(save_path='sentiment_by_lang.png')

# Generate word clouds
wc_gen = WordCloudGenerator(results)
wc_gen.generate_overall_wordcloud(save_path='wordcloud.png')
```

### Load and Analyze Data from File

```python
from src.scraper.koo_scraper import KooScraper

# Load posts from JSON file
scraper = KooScraper()
posts = scraper.load_from_file('path/to/data.json')

# Analyze as usual
analyzer = SentimentAnalyzer()
results = analyzer.analyze_posts(posts)
```

## Command Line Interface

### Main Script Options

```bash
python main.py [OPTIONS]

Options:
  --mode {sample,file,scrape}  Data source mode (default: sample)
  --input PATH                 Input file path (for file mode)
  --output-dir PATH            Output directory (default: outputs)
  --num-posts N                Number of sample posts (default: 100)
  --visualize                  Generate visualizations
  --dashboard                  Launch web dashboard
```

### Examples

Generate and analyze 200 sample posts with visualizations:
```bash
python main.py --mode sample --num-posts 200 --visualize
```

Analyze data from a file:
```bash
python main.py --mode file --input data/my_posts.json --visualize
```

Launch dashboard after analysis:
```bash
python main.py --mode sample --num-posts 100 --dashboard
```

## Configuration

Edit `config/config.yaml` to customize:

- **Scraping settings**: max posts, timeout, delays
- **Model selection**: Choose from different transformer models
- **Language support**: Enable/disable specific languages
- **Output formats**: JSON, CSV, etc.
- **Dashboard settings**: Port, theme, refresh interval

Example configuration:

```yaml
sentiment:
  model_name: "nlptown/bert-base-multilingual-uncased-sentiment"
  batch_size: 16
  device: "cpu"  # Use "cuda" for GPU

languages:
  - en  # English
  - hi  # Hindi
  - ta  # Tamil
  - te  # Telugu
  # ... more languages
```

## Supported Models

1. **nlptown/bert-base-multilingual-uncased-sentiment** (Default)
   - 5-class sentiment (very negative to very positive)
   - Best for detailed sentiment analysis

2. **cardiffnlp/twitter-xlm-roberta-base-sentiment**
   - 3-class sentiment (negative, neutral, positive)
   - Optimized for social media text

3. **ai4bharat/indic-bert**
   - Specialized for Indian languages
   - Good for Hindi, Tamil, Telugu, etc.

## Supported Languages

- English (en)
- Hindi (hi)
- Tamil (ta)
- Telugu (te)
- Bengali (bn)
- Marathi (mr)
- Kannada (kn)
- Gujarati (gu)
- Malayalam (ml)
- Punjabi (pa)

## Output Files

After running the analysis, you'll find:

### Reports (`outputs/reports/`)
- `sentiment_results_YYYYMMDD_HHMMSS.json` - Complete results in JSON
- `sentiment_results_YYYYMMDD_HHMMSS.csv` - Results in CSV format
- `summary_report_YYYYMMDD_HHMMSS.json` - Statistical summary

### Visualizations (`outputs/visualizations/`)
- `sentiment_distribution.png` - Pie chart of sentiment distribution
- `sentiment_by_language.png` - Sentiment breakdown by language
- `sentiment_timeline.png` - Sentiment trends over time
- `engagement_by_sentiment.png` - Engagement metrics by sentiment
- `top_hashtags.png` - Most popular hashtags with sentiment
- `wordcloud_*.png` - Various word clouds

## Web Dashboard Features

The Streamlit dashboard provides:

- **Home**: Overview and introduction
- **Data Analysis**: View and filter analyzed data
- **Visualizations**: Interactive charts and graphs
- **Live Analysis**: Analyze custom text in real-time
- **Statistics**: Detailed statistical reports

Access at `http://localhost:8501` after running:
```bash
streamlit run src/dashboard/app.py
```

## Performance Tips

1. **Use GPU**: Set `device: "cuda"` in config for 10-20x speedup
2. **Batch Size**: Increase batch_size for faster processing (if memory allows)
3. **Model Selection**: Smaller models are faster but may be less accurate
4. **Caching**: Models are cached after first download

## Troubleshooting

### Issue: Model download is slow
**Solution**: Models are downloaded from HuggingFace on first use. Be patient or download manually.

### Issue: Out of memory error
**Solution**: Reduce batch_size in config or use CPU instead of GPU.

### Issue: Language detection is incorrect
**Solution**: Manually specify language when creating posts instead of auto-detection.

### Issue: Dashboard not loading
**Solution**: Ensure Streamlit is installed and port 8501 is not in use.

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- HuggingFace for transformer models
- Streamlit for the dashboard framework
- The open-source NLP community

## Citation

If you use this project in your research, please cite:

```bibtex
@software{koo_sentiment_analysis,
  title={KOO Multilingual Sentiment Analysis},
  author={Sowmya Guda},
  year={2025},
  url={https://github.com/sowmyaguda/koo-sentiment-analysis}
}
```

## Contact

For questions, issues, or suggestions:
- Email: gkvsowmya08@gmail.com
- GitHub Issues: [Create an issue](https://github.com/sowmyaguda/koo-sentiment-analysis/issues)

## Roadmap

- [ ] Add more Indian languages
- [ ] Implement aspect-based sentiment analysis
- [ ] Add emotion detection
- [ ] Support for real-time streaming analysis
- [ ] API endpoint for sentiment analysis
- [ ] Docker containerization
- [ ] Cloud deployment guide

---

Made with ❤️ for multilingual NLP analysis
