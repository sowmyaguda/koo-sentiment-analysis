"""
Language Detection Utility
"""

from langdetect import detect, detect_langs, LangDetectException
from typing import Optional, List, Dict
import re


class LanguageDetector:
    """
    Detect language of text with support for Indian languages
    """

    # Mapping of langdetect codes to full language names
    LANGUAGE_NAMES = {
        'en': 'English',
        'hi': 'Hindi',
        'ta': 'Tamil',
        'te': 'Telugu',
        'bn': 'Bengali',
        'mr': 'Marathi',
        'kn': 'Kannada',
        'gu': 'Gujarati',
        'ml': 'Malayalam',
        'pa': 'Punjabi',
        'or': 'Oriya',
        'ur': 'Urdu',
        'ne': 'Nepali',
        'sa': 'Sanskrit'
    }

    # Unicode ranges for Indian scripts
    SCRIPT_RANGES = {
        'Devanagari': (0x0900, 0x097F),  # Hindi, Marathi, Nepali, Sanskrit
        'Bengali': (0x0980, 0x09FF),      # Bengali, Assamese
        'Gurmukhi': (0x0A00, 0x0A7F),     # Punjabi
        'Gujarati': (0x0A80, 0x0AFF),     # Gujarati
        'Oriya': (0x0B00, 0x0B7F),        # Oriya
        'Tamil': (0x0B80, 0x0BFF),        # Tamil
        'Telugu': (0x0C00, 0x0C7F),       # Telugu
        'Kannada': (0x0C80, 0x0CFF),      # Kannada
        'Malayalam': (0x0D00, 0x0D7F),    # Malayalam
    }

    def __init__(self):
        """Initialize language detector"""
        pass

    def detect(self, text: str) -> Optional[str]:
        """
        Detect the primary language of text

        Args:
            text: Input text

        Returns:
            Language code (e.g., 'en', 'hi', 'ta') or None if detection fails
        """
        if not text or not text.strip():
            return None

        # Clean text
        text = self._clean_text(text)

        # Try script-based detection first for better accuracy with Indian languages
        script = self._detect_script(text)
        if script:
            script_to_lang = {
                'Devanagari': 'hi',
                'Bengali': 'bn',
                'Gurmukhi': 'pa',
                'Gujarati': 'gu',
                'Oriya': 'or',
                'Tamil': 'ta',
                'Telugu': 'te',
                'Kannada': 'kn',
                'Malayalam': 'ml'
            }
            if script in script_to_lang:
                return script_to_lang[script]

        # Fall back to langdetect
        try:
            lang_code = detect(text)
            return lang_code
        except LangDetectException:
            return None

    def detect_with_confidence(self, text: str) -> List[Dict[str, float]]:
        """
        Detect languages with confidence scores

        Args:
            text: Input text

        Returns:
            List of dictionaries with 'lang' and 'prob' keys
        """
        if not text or not text.strip():
            return []

        text = self._clean_text(text)

        try:
            langs = detect_langs(text)
            return [{'lang': str(lang).split(':')[0], 'prob': lang.prob} for lang in langs]
        except LangDetectException:
            return []

    def _detect_script(self, text: str) -> Optional[str]:
        """
        Detect the script used in text based on Unicode ranges

        Args:
            text: Input text

        Returns:
            Script name or None
        """
        script_counts = {script: 0 for script in self.SCRIPT_RANGES}

        for char in text:
            code_point = ord(char)
            for script, (start, end) in self.SCRIPT_RANGES.items():
                if start <= code_point <= end:
                    script_counts[script] += 1
                    break

        # Find the most common script
        max_script = max(script_counts.items(), key=lambda x: x[1])
        if max_script[1] > 0:
            return max_script[0]

        return None

    def _clean_text(self, text: str) -> str:
        """
        Clean text for better language detection

        Args:
            text: Input text

        Returns:
            Cleaned text
        """
        # Remove URLs
        text = re.sub(r'http\S+|www\S+', '', text)
        # Remove mentions
        text = re.sub(r'@\w+', '', text)
        # Remove hashtags (keep the text)
        text = re.sub(r'#', '', text)
        # Remove extra whitespace
        text = ' '.join(text.split())

        return text

    def get_language_name(self, lang_code: str) -> str:
        """
        Get full language name from code

        Args:
            lang_code: Language code (e.g., 'en', 'hi')

        Returns:
            Full language name
        """
        return self.LANGUAGE_NAMES.get(lang_code, lang_code.upper())

    def is_multilingual(self, text: str, threshold: float = 0.3) -> bool:
        """
        Check if text contains multiple languages

        Args:
            text: Input text
            threshold: Minimum probability threshold for secondary language

        Returns:
            True if text is multilingual
        """
        langs = self.detect_with_confidence(text)

        if len(langs) > 1:
            # Check if second language has significant presence
            return langs[1]['prob'] >= threshold

        return False

    def detect_batch(self, texts: List[str]) -> List[Optional[str]]:
        """
        Detect languages for multiple texts

        Args:
            texts: List of texts

        Returns:
            List of language codes
        """
        return [self.detect(text) for text in texts]
