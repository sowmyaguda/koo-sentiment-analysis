"""
KOO Website Scraper

Note: As of 2023, KOO has been shut down. This scraper is designed as a template
and can be adapted for similar social media platforms or used with archived KOO data.
"""

import time
import json
import re
from datetime import datetime
from typing import List, Optional, Dict
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from .data_models import KooPost


class KooScraper:
    """Scraper for KOO social media platform"""

    def __init__(self, config: Dict = None):
        """
        Initialize KOO scraper

        Args:
            config: Configuration dictionary with scraping parameters
        """
        self.config = config or {}
        self.max_posts = self.config.get('max_posts', 100)
        self.timeout = self.config.get('timeout', 10)
        self.delay = self.config.get('delay_between_requests', 2)
        self.user_agent = self.config.get('user_agent',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')

        self.driver = None
        self.posts: List[KooPost] = []

    def _init_driver(self):
        """Initialize Selenium WebDriver"""
        if self.driver is None:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument(f'user-agent={self.user_agent}')

            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def _extract_hashtags(self, text: str) -> List[str]:
        """Extract hashtags from text"""
        return re.findall(r'#(\w+)', text)

    def _extract_mentions(self, text: str) -> List[str]:
        """Extract mentions from text"""
        return re.findall(r'@(\w+)', text)

    def scrape_trending_topics(self) -> List[str]:
        """
        Scrape trending topics/hashtags

        Returns:
            List of trending topics
        """
        # Placeholder implementation
        # In reality, you'd scrape the trending section
        print("Note: KOO platform is no longer active")
        print("This is a template implementation")
        return []

    def scrape_by_hashtag(self, hashtag: str, max_posts: Optional[int] = None) -> List[KooPost]:
        """
        Scrape posts by hashtag

        Args:
            hashtag: Hashtag to search for
            max_posts: Maximum number of posts to scrape

        Returns:
            List of KooPost objects
        """
        max_posts = max_posts or self.max_posts
        posts = []

        print(f"Scraping posts with hashtag: #{hashtag}")
        print("Note: This is a template. Adapt for active platforms.")

        # Template implementation
        # In a real scenario, you would:
        # 1. Navigate to hashtag page
        # 2. Scroll and load posts
        # 3. Extract post data
        # 4. Create KooPost objects

        return posts

    def scrape_user_profile(self, username: str, max_posts: Optional[int] = None) -> List[KooPost]:
        """
        Scrape posts from a user profile

        Args:
            username: Username to scrape
            max_posts: Maximum number of posts to scrape

        Returns:
            List of KooPost objects
        """
        max_posts = max_posts or self.max_posts
        posts = []

        print(f"Scraping profile: @{username}")
        print("Note: This is a template. Adapt for active platforms.")

        return posts

    def load_from_file(self, file_path: str) -> List[KooPost]:
        """
        Load posts from a JSON file

        Args:
            file_path: Path to JSON file

        Returns:
            List of KooPost objects
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        posts = []
        for item in data:
            if isinstance(item, dict):
                # Handle different JSON formats
                post = self._parse_post_from_dict(item)
                if post:
                    posts.append(post)

        self.posts.extend(posts)
        print(f"Loaded {len(posts)} posts from {file_path}")
        return posts

    def _parse_post_from_dict(self, data: Dict) -> Optional[KooPost]:
        """
        Parse a post from dictionary data

        Args:
            data: Dictionary containing post data

        Returns:
            KooPost object or None
        """
        try:
            # Flexible parsing to handle different data formats
            text = data.get('text') or data.get('content') or data.get('message', '')

            post = KooPost(
                post_id=str(data.get('id') or data.get('post_id', f"post_{len(self.posts)}")),
                text=text,
                author=data.get('author') or data.get('username') or data.get('user', 'unknown'),
                timestamp=self._parse_timestamp(data.get('timestamp') or data.get('created_at')),
                language=data.get('language') or data.get('lang'),
                likes=int(data.get('likes', 0)),
                reposts=int(data.get('reposts', 0) or data.get('retweets', 0)),
                comments=int(data.get('comments', 0)),
                hashtags=data.get('hashtags') or self._extract_hashtags(text),
                mentions=data.get('mentions') or self._extract_mentions(text),
                url=data.get('url')
            )
            return post
        except Exception as e:
            print(f"Error parsing post: {e}")
            return None

    def _parse_timestamp(self, timestamp) -> datetime:
        """Parse timestamp from various formats"""
        if timestamp is None:
            return datetime.now()

        if isinstance(timestamp, datetime):
            return timestamp

        if isinstance(timestamp, (int, float)):
            return datetime.fromtimestamp(timestamp)

        if isinstance(timestamp, str):
            try:
                return datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            except:
                try:
                    return datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
                except:
                    return datetime.now()

        return datetime.now()

    def save_posts(self, output_path: str, format: str = 'json'):
        """
        Save scraped posts to file

        Args:
            output_path: Path to save file
            format: Output format ('json' or 'csv')
        """
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        if format == 'json':
            with open(path, 'w', encoding='utf-8') as f:
                json.dump([post.to_dict() for post in self.posts], f,
                         indent=2, ensure_ascii=False)
        elif format == 'csv':
            import pandas as pd
            df = pd.DataFrame([post.to_dict() for post in self.posts])
            df.to_csv(path, index=False, encoding='utf-8')

        print(f"Saved {len(self.posts)} posts to {output_path}")

    def create_sample_data(self, num_posts: int = 50) -> List[KooPost]:
        """
        Create sample data for testing

        Args:
            num_posts: Number of sample posts to create

        Returns:
            List of sample KooPost objects
        """
        sample_texts = {
            'en': [
                "Great initiative by the government! #IndiaForward #Development",
                "The new policy will help millions of people. Proud moment! 🇮🇳",
                "Disappointed with the recent announcement. We need better solutions.",
                "Amazing progress in technology sector. India is rising! #TechIndia",
                "This is not acceptable. We demand transparency and accountability.",
            ],
            'hi': [
                "बहुत अच्छी पहल है। आगे बढ़ते रहो! #भारत #विकास",
                "यह निर्णय देश के लिए अच्छा है। धन्यवाद!",
                "मुझे इस बात से निराशा हुई। हमें बेहतर समाधान चाहिए।",
                "प्रौद्योगिकी क्षेत्र में शानदार प्रगति। भारत उभर रहा है!",
                "यह स्वीकार्य नहीं है। हम पारदर्शिता और जवाबदेही की मांग करते हैं।",
            ],
            'ta': [
                "அருமையான முயற்சி! வாழ்த்துக்கள் #இந்தியா #வளர்ச்சி",
                "இந்த கொள்கை மில்லியன் கணக்கான மக்களுக்கு உதவும்.",
                "சமீபத்திய அறிவிப்பில் ஏமாற்றம். எங்களுக்கு சிறந்த தீர்வுகள் தேவை.",
                "தொழில்நுட்ப துறையில் அற்புதமான முன்னேற்றம்!",
                "இது ஏற்றுக்கொள்ள முடியாதது. வெளிப்படைத்தன்மை வேண்டும்.",
            ]
        }

        posts = []
        for i in range(num_posts):
            lang = ['en', 'hi', 'ta'][i % 3]
            text = sample_texts[lang][i % len(sample_texts[lang])]

            post = KooPost(
                post_id=f"sample_{i+1}",
                text=text,
                author=f"user_{(i % 10) + 1}",
                timestamp=datetime.now(),
                language=lang,
                likes=int((i * 37) % 1000),
                reposts=int((i * 13) % 100),
                comments=int((i * 7) % 50),
                hashtags=self._extract_hashtags(text),
                mentions=self._extract_mentions(text)
            )
            posts.append(post)

        self.posts = posts
        print(f"Created {len(posts)} sample posts")
        return posts

    def close(self):
        """Clean up resources"""
        if self.driver:
            self.driver.quit()
            self.driver = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
