"""
Text Preprocessing Utilities
"""

import re
from typing import List, Optional
import unicodedata


class TextPreprocessor:
    """
    Text preprocessing for sentiment analysis
    """

    def __init__(self):
        """Initialize preprocessor"""
        pass

    def clean_text(self, text: str, remove_urls: bool = True,
                   remove_mentions: bool = False,
                   remove_hashtags: bool = False,
                   remove_emojis: bool = False) -> str:
        """
        Clean text with various options

        Args:
            text: Input text
            remove_urls: Remove URLs
            remove_mentions: Remove @mentions
            remove_hashtags: Remove hashtags
            remove_emojis: Remove emojis

        Returns:
            Cleaned text
        """
        if not text:
            return ""

        # Remove URLs
        if remove_urls:
            text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)

        # Remove mentions
        if remove_mentions:
            text = re.sub(r'@\w+', '', text)

        # Remove hashtags (symbol only, keep text)
        if remove_hashtags:
            text = re.sub(r'#', '', text)

        # Remove emojis
        if remove_emojis:
            text = self._remove_emojis(text)

        # Remove extra whitespace
        text = ' '.join(text.split())

        return text.strip()

    def _remove_emojis(self, text: str) -> str:
        """Remove emojis from text"""
        emoji_pattern = re.compile(
            "["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
            u"\U00002500-\U00002BEF"  # chinese char
            u"\U00002702-\U000027B0"
            u"\U00002702-\U000027B0"
            u"\U000024C2-\U0001F251"
            u"\U0001f926-\U0001f937"
            u"\U00010000-\U0010ffff"
            u"\u2640-\u2642"
            u"\u2600-\u2B55"
            u"\u200d"
            u"\u23cf"
            u"\u23e9"
            u"\u231a"
            u"\ufe0f"  # dingbats
            u"\u3030"
            "]+",
            re.UNICODE
        )
        return emoji_pattern.sub(r'', text)

    def normalize_text(self, text: str) -> str:
        """
        Normalize text (lowercase, unicode normalization)

        Args:
            text: Input text

        Returns:
            Normalized text
        """
        if not text:
            return ""

        # Unicode normalization
        text = unicodedata.normalize('NFKC', text)

        # Lowercase (be careful with non-English text)
        # text = text.lower()

        return text

    def extract_hashtags(self, text: str) -> List[str]:
        """
        Extract hashtags from text

        Args:
            text: Input text

        Returns:
            List of hashtags (without # symbol)
        """
        return re.findall(r'#(\w+)', text)

    def extract_mentions(self, text: str) -> List[str]:
        """
        Extract mentions from text

        Args:
            text: Input text

        Returns:
            List of mentions (without @ symbol)
        """
        return re.findall(r'@(\w+)', text)

    def extract_urls(self, text: str) -> List[str]:
        """
        Extract URLs from text

        Args:
            text: Input text

        Returns:
            List of URLs
        """
        return re.findall(r'http\S+|www\S+|https\S+', text)

    def tokenize_simple(self, text: str) -> List[str]:
        """
        Simple word tokenization

        Args:
            text: Input text

        Returns:
            List of tokens
        """
        # Remove punctuation
        text = re.sub(r'[^\w\s]', ' ', text)
        # Split on whitespace
        tokens = text.split()
        return [t for t in tokens if t]

    def remove_punctuation(self, text: str) -> str:
        """
        Remove punctuation from text

        Args:
            text: Input text

        Returns:
            Text without punctuation
        """
        return re.sub(r'[^\w\s]', ' ', text)

    def preprocess_for_sentiment(self, text: str) -> str:
        """
        Preprocess text for sentiment analysis

        Args:
            text: Input text

        Returns:
            Preprocessed text
        """
        # Clean but preserve emojis and some punctuation (important for sentiment)
        text = self.clean_text(
            text,
            remove_urls=True,
            remove_mentions=False,
            remove_hashtags=False,
            remove_emojis=False
        )

        # Normalize
        text = self.normalize_text(text)

        return text
