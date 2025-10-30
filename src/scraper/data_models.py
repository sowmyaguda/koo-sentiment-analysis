"""
Data models for KOO posts
"""

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional, List, Dict


@dataclass
class KooPost:
    """Represents a KOO post/tweet"""

    post_id: str
    text: str
    author: str
    timestamp: datetime
    language: Optional[str] = None
    likes: int = 0
    reposts: int = 0
    comments: int = 0
    hashtags: List[str] = None
    mentions: List[str] = None
    url: Optional[str] = None

    def __post_init__(self):
        if self.hashtags is None:
            self.hashtags = []
        if self.mentions is None:
            self.mentions = []

    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: Dict) -> 'KooPost':
        """Create from dictionary"""
        if isinstance(data['timestamp'], str):
            data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        return cls(**data)
