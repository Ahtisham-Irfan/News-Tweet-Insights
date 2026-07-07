"""
test_sentiment.py
-------------------
Basic unit tests for sentiment_analyzer.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.sentiment_analyzer import get_sentiment, get_polarity_score


def test_positive_sentiment():
    assert get_sentiment("This is a wonderful and amazing achievement!") == "Positive"


def test_negative_sentiment():
    assert get_sentiment("This is a terrible and horrible disaster.") == "Negative"


def test_neutral_sentiment():
    assert get_sentiment("The meeting is scheduled for 3 PM tomorrow.") == "Neutral"


def test_empty_string():
    assert get_sentiment("") == "Neutral"
    assert get_polarity_score("") == 0.0


def test_polarity_score_range():
    score = get_polarity_score("I love this so much, it's fantastic!")
    assert -1.0 <= score <= 1.0
    assert score > 0
