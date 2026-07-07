"""
sentiment_analyzer.py
----------------------
Simple sentiment scoring using TextBlob's polarity score.
"""

from textblob import TextBlob


def get_sentiment(text: str, threshold: float = 0.1) -> str:
    """
    Classify text as Positive, Negative, or Neutral.

    Args:
        text: Input string to analyze
        threshold: Polarity cutoff for classifying as non-neutral

    Returns:
        One of "Positive", "Negative", "Neutral"
    """
    if not text or not text.strip():
        return "Neutral"

    polarity = TextBlob(text).sentiment.polarity

    if polarity > threshold:
        return "Positive"
    elif polarity < -threshold:
        return "Negative"
    return "Neutral"


def get_polarity_score(text: str) -> float:
    """Return the raw polarity score (-1.0 to 1.0) for a piece of text."""
    if not text or not text.strip():
        return 0.0
    return TextBlob(text).sentiment.polarity
