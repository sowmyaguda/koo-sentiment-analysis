"""
Configuration Loader
"""

import yaml
from pathlib import Path
from typing import Dict, Any


def load_config(config_path: str = None) -> Dict[str, Any]:
    """
    Load configuration from YAML file

    Args:
        config_path: Path to config file. If None, loads default config.

    Returns:
        Configuration dictionary
    """
    if config_path is None:
        # Default config path
        current_dir = Path(__file__).parent.parent.parent
        config_path = current_dir / 'config' / 'config.yaml'
    else:
        config_path = Path(config_path)

    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    return config


def get_scraping_config(config: Dict) -> Dict:
    """Extract scraping configuration"""
    return config.get('scraping', {})


def get_sentiment_config(config: Dict) -> Dict:
    """Extract sentiment analysis configuration"""
    return config.get('sentiment', {})


def get_output_config(config: Dict) -> Dict:
    """Extract output configuration"""
    return config.get('output', {})


def get_dashboard_config(config: Dict) -> Dict:
    """Extract dashboard configuration"""
    return config.get('dashboard', {})
