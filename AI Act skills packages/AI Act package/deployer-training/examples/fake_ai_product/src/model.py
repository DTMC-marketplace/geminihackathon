"""
Sentiment Analysis Model Module

Contains the SentimentModel class for classifying text.
"""

class SentimentModel:
    """A simple sentiment classifier using keyword matching (for demo purposes)."""
    
    POSITIVE_KEYWORDS = ['good', 'great', 'excellent', 'happy', 'love', 'amazing', 'wonderful']
    NEGATIVE_KEYWORDS = ['bad', 'terrible', 'awful', 'sad', 'hate', 'horrible', 'disappointing']
    
    def __init__(self):
        """Initialize the model."""
        self.is_loaded = True
    
    def predict(self, text: str) -> tuple:
        """
        Predict sentiment of the given text.
        
        Args:
            text: Preprocessed text string.
        
        Returns:
            Tuple of (sentiment_label, confidence_score)
        """
        text_lower = text.lower()
        
        pos_count = sum(1 for word in self.POSITIVE_KEYWORDS if word in text_lower)
        neg_count = sum(1 for word in self.NEGATIVE_KEYWORDS if word in text_lower)
        
        total = pos_count + neg_count
        if total == 0:
            return ('neutral', 0.5)
        
        if pos_count > neg_count:
            return ('positive', 0.6 + (pos_count / (total + 1)) * 0.35)
        elif neg_count > pos_count:
            return ('negative', 0.6 + (neg_count / (total + 1)) * 0.35)
        else:
            return ('neutral', 0.5)
