"""
news_scraper.py
----------------
Scrapes recent news headlines for a given query using Google News RSS feed.
No API key required.
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict


def scrape_news(query: str, region: str = "PK", language: str = "en", limit: int = 15) -> List[Dict]:
    """
    Fetch recent news headlines matching `query` from Google News RSS.

    Args:
        query: Search term, e.g. "Pakistan cricket"
        region: Country code, e.g. "PK", "US"
        language: Language code, e.g. "en"
        limit: Max number of articles to return

    Returns:
        List of dicts with keys: title, link, pubDate, source
    """
    url = (
        f"https://news.google.com/rss/search?q={query}"
        f"&hl={language}-{region}&gl={region}&ceid={region}:{language}"
    )
    headers = {"User-Agent": "Mozilla/5.0 (compatible; NewsBot/1.0)"}

    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "xml")
    items = soup.find_all("item")[:limit]

    articles = []
    for item in items:
        source_tag = item.find("source")
        articles.append({
            "title": item.title.text if item.title else "",
            "link": item.link.text if item.link else "",
            "pubDate": item.pubDate.text if item.pubDate else "",
            "source": source_tag.text if source_tag else "Unknown",
        })

    return articles


if __name__ == "__main__":
    results = scrape_news("Pakistan cricket")
    for r in results:
        print(f"- {r['title']} ({r['source']})")
