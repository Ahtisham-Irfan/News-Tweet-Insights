# 📊 News & Tweet Insights

A Python toolkit that scrapes *news headlines* and *tweets* on any topic, runs *sentiment analysis*, and visualizes *trending keywords* — all in one clean, modular project.

Two tools in one repo:

1. **Sentiment Tracker** (CLI) — compares public sentiment in news vs. Twitter for any search query.
2. **Trending Dashboard** (Streamlit) — live web dashboard showing trending keywords + word cloud from multiple news sources.

---

## 🗂️ Project Structure

```
news-tweet-insights/
├── src/
│   ├── __init__.py
│   ├── news_scraper.py       # Scrapes news via Google News RSS
│   ├── tweet_scraper.py      # Scrapes tweets via snscrape
│   ├── sentiment_analyzer.py # TextBlob-based sentiment scoring
│   └── main.py                # CLI entry point for Sentiment Tracker
├── dashboard/
│   └── app.py                  # Streamlit Trending Dashboard
├── data/                        # Output CSVs land here (gitignored)
├── tests/
│   └── test_sentiment.py      # Unit tests for sentiment logic
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

---

## ⚙️ Installation

```bash
git clone https://github.com/yourusername/news-tweet-insights.git
cd news-tweet-insights
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## 🚀 Usage

### 1. Sentiment Tracker (CLI)

```bash
python -m src.main --query "Pakistan cricket" --tweet-limit 30
```

Output:
- Console summary of Positive/Negative/Neutral counts
- `data/news_sentiment.csv`
- `data/tweet_sentiment.csv`

### 2. Trending Dashboard (Streamlit)

```bash
streamlit run dashboard/app.py
```

Opens a browser dashboard where you can:
- Pick a news source (Dawn / BBC Urdu)
- Fetch latest headlines
- See top trending keywords (bar chart)
- See a word cloud visualization

---

## 🧪 Running Tests

```bash
pytest tests/
```

---

## 📦 Requirements

- Python 3.9+
- See `requirements.txt` for full package list

---

## ⚠️ Notes & Limitations

- **Twitter scraping** uses `snscrape`, which depends on Twitter/X's public web structure. If it breaks, this is due to upstream changes — switching to the official `tweepy` API (with a developer key) is the reliable long-term fix.
- Always check a website's `robots.txt` and Terms of Service before scraping.
- News site HTML structures change over time — CSS selectors in `news_scraper.py` may need periodic updates.
- Add delays (`time.sleep()`) between requests if you hit rate limits.

---

## 🛣️ Roadmap Ideas

- [ ] Add more news sources (Geo, Al Jazeera, Reuters)
- [ ] Swap TextBlob for a transformer-based sentiment model (e.g., `cardiffnlp/twitter-roberta-base-sentiment`)
- [ ] Add scheduling (cron / APScheduler) for automated daily reports
- [ ] Add a combined dashboard (news + tweets + trends in one view)
- [ ] Dockerize the project

---

