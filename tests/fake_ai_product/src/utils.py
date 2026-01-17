"""
Utility functions for text preprocessing.
"""

import re

def preprocess_text(text: str) -> str:
    """
    Preprocess text for sentiment analysis.
    
    Steps:
        1. Convert to lowercase
        2. Remove punctuation
        3. Strip extra whitespace
    
    Args:
        text: Raw input text.
    
    Returns:
        Cleaned text string.
    """
    # Lowercase
    text = text.lower()
    
    # Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)
    
    # Strip extra whitespace
    text = ' '.join(text.split())
    
    return text
