"""
tweet_scraper.py
-----------------
Scrapes recent tweets for a given query using snscrape (no API key required).

Note: Twitter/X frequently changes its internal structure, which can break
snscrape. If this stops working, consider switching to the official
Twitter API v2 via `tweepy` (requires a developer account/API key).
"""

import subprocess
import json
from typing import List, Dict


def scrape_tweets(query: str, limit: int = 20) -> List[Dict]:
    """
    Fetch recent tweets matching `query` using snscrape's CLI.

    Args:
        query: Search term or hashtag, e.g. "PakistanCricket"
        limit: Max number of tweets to fetch

    Returns:
        List of dicts with keys: content, date, username, url
    """
    cmd = [
        "snscrape",
        "--jsonl",
        "--max-results", str(limit),
        "twitter-search", query,
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

    if result.returncode != 0:
        raise RuntimeError(f"snscrape failed: {result.stderr.strip()}")

    tweets = []
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        data = json.loads(line)
        tweets.append({
            "content": data.get("content", ""),
            "date": data.get("date", ""),
            "username": data.get("user", {}).get("username", ""),
            "url": data.get("url", ""),
        })

    return tweets


if __name__ == "__main__":
    results = scrape_tweets("Pakistan cricket", limit=10)
    for t in results:
        print(f"- @{t['username']}: {t['content'][:80]}")
