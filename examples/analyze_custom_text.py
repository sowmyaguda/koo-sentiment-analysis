"""
Example: Analyze Custom Text
"""

import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from src.sentiment.analyzer import SentimentAnalyzer
from src.scraper.data_models import KooPost
from src.utils.config_loader import load_config


def analyze_text(text: str, language: str = None):
    """
    Analyze sentiment of custom text

    Args:
        text: Text to analyze
        language: Language code (optional, will be auto-detected)
    """
    # Initialize analyzer
    config = load_config()
    analyzer = SentimentAnalyzer(config.get('sentiment', {}))

    # Create a post object
    post = KooPost(
        post_id="custom_1",
        text=text,
        author="user",
        timestamp=datetime.now(),
        language=language
    )

    # Analyze
    result = analyzer.analyze_post(post)

    # Display results
    print(f"\nText: {text}")
    print(f"Language: {result['language']}")
    print(f"Sentiment: {result['sentiment']}")
    print(f"Confidence: {result['confidence']:.2%}")
    print(f"Sentiment Score: {result['sentiment_score']:.3f}")
    print("\nDetailed Scores:")
    for sentiment, score in result['sentiment_scores'].items():
        print(f"  {sentiment}: {score:.4f}")


def main():
    """Main function with example texts"""

    print("Custom Text Sentiment Analysis")
    print("=" * 70)

    # Example texts in different languages
    examples = [
        ("This is an amazing product! I love it!", "en"),
        ("बहुत अच्छा है! मुझे यह पसंद है।", "hi"),
        ("இது மிகவும் நன்றாக உள்ளது!", "ta"),
        ("This is terrible. Very disappointed.", "en"),
        ("यह बहुत खराब है। निराशाजनक।", "hi"),
    ]

    for text, lang in examples:
        print("\n" + "-" * 70)
        analyze_text(text, lang)

    print("\n" + "=" * 70)
    print("\nYou can modify this script to analyze your own custom text!")


if __name__ == "__main__":
    main()
