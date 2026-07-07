"""
main.py
--------
CLI entry point for the News + Tweet Sentiment Tracker.

Usage:
    python -m src.main --query "Pakistan cricket" --tweet-limit 30
"""

import argparse
import os
import pandas as pd

from src.news_scraper import scrape_news
from src.tweet_scraper import scrape_tweets
from src.sentiment_analyzer import get_sentiment

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


def analyze(query: str, news_limit: int = 15, tweet_limit: int = 20):
    print(f"\n🔎 Fetching news for: '{query}'...")
    news = scrape_news(query, limit=news_limit)

    print(f"🔎 Fetching tweets for: '{query}'...")
    try:
        tweets = scrape_tweets(query, limit=tweet_limit)
    except RuntimeError as e:
        print(f"⚠️  Tweet scraping failed: {e}")
        tweets = []

    news_df = pd.DataFrame(news)
    if not news_df.empty:
        news_df["sentiment"] = news_df["title"].apply(get_sentiment)

    tweets_df = pd.DataFrame(tweets)
    if not tweets_df.empty:
        tweets_df["sentiment"] = tweets_df["content"].apply(get_sentiment)

    print("\n📰 NEWS SENTIMENT SUMMARY:")
    print(news_df["sentiment"].value_counts() if not news_df.empty else "No news found.")

    print("\n🐦 TWEET SENTIMENT SUMMARY:")
    print(tweets_df["sentiment"].value_counts() if not tweets_df.empty else "No tweets found.")

    return news_df, tweets_df


def main():
    parser = argparse.ArgumentParser(description="News + Tweet Sentiment Tracker")
    parser.add_argument("--query", type=str, required=True, help="Search topic, e.g. 'Pakistan cricket'")
    parser.add_argument("--news-limit", type=int, default=15, help="Max number of news articles to fetch")
    parser.add_argument("--tweet-limit", type=int, default=20, help="Max number of tweets to fetch")
    args = parser.parse_args()

    os.makedirs(DATA_DIR, exist_ok=True)

    news_df, tweets_df = analyze(args.query, args.news_limit, args.tweet_limit)

    news_path = os.path.join(DATA_DIR, "news_sentiment.csv")
    tweets_path = os.path.join(DATA_DIR, "tweet_sentiment.csv")

    news_df.to_csv(news_path, index=False)
    tweets_df.to_csv(tweets_path, index=False)

    print(f"\n✅ Saved: {news_path}")
    print(f"✅ Saved: {tweets_path}")


if __name__ == "__main__":
    main()
