"""
Main script for KOO Multilingual Sentiment Analysis

This script demonstrates the complete workflow:
1. Data collection (sample data or from file)
2. Sentiment analysis
3. Visualization generation
4. Report generation
"""

import argparse
from pathlib import Path
from datetime import datetime

from src.scraper.koo_scraper import KooScraper
from src.sentiment.analyzer import SentimentAnalyzer
from src.visualization.charts import SentimentCharts
from src.visualization.wordcloud_generator import WordCloudGenerator
from src.utils.config_loader import load_config


def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(
        description="KOO Multilingual Sentiment Analysis"
    )

    parser.add_argument(
        '--mode',
        choices=['sample', 'file', 'scrape'],
        default='sample',
        help='Data source mode'
    )

    parser.add_argument(
        '--input',
        type=str,
        help='Input file path (for file mode)'
    )

    parser.add_argument(
        '--output-dir',
        type=str,
        default='outputs',
        help='Output directory for results'
    )

    parser.add_argument(
        '--num-posts',
        type=int,
        default=100,
        help='Number of sample posts to generate (for sample mode)'
    )

    parser.add_argument(
        '--visualize',
        action='store_true',
        help='Generate visualizations'
    )

    parser.add_argument(
        '--dashboard',
        action='store_true',
        help='Launch web dashboard'
    )

    args = parser.parse_args()

    print("=" * 70)
    print("KOO MULTILINGUAL SENTIMENT ANALYSIS")
    print("=" * 70)
    print()

    # Load configuration
    config = load_config()

    # Step 1: Data Collection
    print("[1/4] Data Collection")
    print("-" * 70)

    scraper = KooScraper(config.get('scraping', {}))
    posts = []

    if args.mode == 'sample':
        print(f"Generating {args.num_posts} sample posts...")
        posts = scraper.create_sample_data(num_posts=args.num_posts)

    elif args.mode == 'file':
        if not args.input:
            print("Error: --input required for file mode")
            return

        print(f"Loading posts from: {args.input}")
        posts = scraper.load_from_file(args.input)

    elif args.mode == 'scrape':
        print("Note: KOO platform is no longer active.")
        print("Using sample data instead...")
        posts = scraper.create_sample_data(num_posts=args.num_posts)

    print(f"✓ Loaded {len(posts)} posts")
    print()

    # Step 2: Sentiment Analysis
    print("[2/4] Sentiment Analysis")
    print("-" * 70)

    analyzer = SentimentAnalyzer(config.get('sentiment', {}))
    results = analyzer.analyze_posts(posts)

    print(f"✓ Analyzed {len(results)} posts")
    print()

    # Step 3: Save Results
    print("[3/4] Saving Results")
    print("-" * 70)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Create timestamp for filenames
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Save raw results
    results_file = output_dir / 'reports' / f'sentiment_results_{timestamp}.json'
    analyzer.save_results(results_file, format='json')

    # Save CSV
    csv_file = output_dir / 'reports' / f'sentiment_results_{timestamp}.csv'
    analyzer.save_results(csv_file, format='csv')

    # Save summary report
    summary_file = output_dir / 'reports' / f'summary_report_{timestamp}.json'
    analyzer.export_summary_report(summary_file)

    print(f"✓ Results saved to {output_dir / 'reports'}")
    print()

    # Step 4: Statistics
    print("[4/4] Statistical Summary")
    print("-" * 70)

    stats = analyzer.get_statistics()

    print(f"Total Posts: {stats['total_posts']}")
    print(f"Average Sentiment Score: {stats['average_sentiment_score']:.3f}")
    print(f"Average Confidence: {stats['average_confidence']:.2%}")
    print()

    print("Sentiment Distribution:")
    for sentiment, count in stats['sentiment_distribution'].items():
        percentage = (count / stats['total_posts']) * 100
        print(f"  {sentiment:15s}: {count:4d} ({percentage:5.1f}%)")
    print()

    print("Most Positive Post:")
    print(f"  {stats['most_positive_post']['text']}")
    print(f"  Score: {stats['most_positive_post']['sentiment_score']:.3f}")
    print()

    print("Most Negative Post:")
    print(f"  {stats['most_negative_post']['text']}")
    print(f"  Score: {stats['most_negative_post']['sentiment_score']:.3f}")
    print()

    # Generate Visualizations
    if args.visualize:
        print("Generating Visualizations...")
        print("-" * 70)

        viz_dir = output_dir / 'visualizations' / timestamp
        charts = SentimentCharts(results)
        charts.create_dashboard(str(viz_dir))

        # Word clouds
        wc_gen = WordCloudGenerator(results)
        wc_gen.generate_overall_wordcloud(
            save_path=str(viz_dir / 'wordcloud_overall.png')
        )
        wc_gen.generate_sentiment_wordclouds(save_dir=str(viz_dir))
        wc_gen.generate_hashtag_wordcloud(
            save_path=str(viz_dir / 'wordcloud_hashtags.png')
        )

        print(f"✓ Visualizations saved to {viz_dir}")
        print()

    # Launch Dashboard
    if args.dashboard:
        print("Launching Web Dashboard...")
        print("-" * 70)
        print("Dashboard will open in your browser at http://localhost:8501")
        print("Press Ctrl+C to stop the dashboard")
        print()

        import subprocess
        subprocess.run([
            'streamlit', 'run',
            'src/dashboard/app.py',
            '--server.port', str(config.get('dashboard', {}).get('port', 8501))
        ])

    print("=" * 70)
    print("Analysis Complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
