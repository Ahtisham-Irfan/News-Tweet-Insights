"""
app.py
-------
Streamlit dashboard: scrapes headlines from multiple news sources,
extracts trending keywords, and visualizes them as a bar chart + word cloud.

Run with:
    streamlit run dashboard/app.py
"""

import re
from collections import Counter

import matplotlib.pyplot as plt
import pandas as pd
import requests
import streamlit as st
from bs4 import BeautifulSoup
from wordcloud import WordCloud

st.set_page_config(page_title="Trending News Dashboard", layout="wide")
st.title("📊 Live Trending Topics Dashboard")

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; TrendBot/1.0)"}

STOPWORDS = {
    "the", "a", "an", "in", "on", "of", "to", "for", "and", "is", "are",
    "with", "after", "says", "as", "at", "by", "from", "over", "into",
    "amid", "his", "her", "its", "will", "has", "have", "was", "were",
}


@st.cache_data(ttl=300)
def scrape_dawn():
    url = "https://www.dawn.com/latest-news"
    resp = requests.get(url, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(resp.content, "html.parser")
    headlines = [h.get_text(strip=True) for h in soup.select("article h2 a")]
    return headlines[:20]


@st.cache_data(ttl=300)
def scrape_bbc_urdu():
    url = "https://www.bbc.com/urdu"
    resp = requests.get(url, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(resp.content, "html.parser")
    headlines = [h.get_text(strip=True) for h in soup.find_all("h2")]
    return headlines[:20]


def get_keywords(headlines, top_n=15):
    words = []
    for h in headlines:
        cleaned = re.findall(r"\b[a-zA-Z]{3,}\b", h.lower())
        words.extend(w for w in cleaned if w not in STOPWORDS)
    return Counter(words).most_common(top_n)


source = st.selectbox("Choose News Source", ["Dawn", "BBC Urdu"])

if st.button("🔄 Fetch Latest News"):
    with st.spinner("Scraping latest headlines..."):
        headlines = scrape_dawn() if source == "Dawn" else scrape_bbc_urdu()

    if not headlines:
        st.warning("No headlines found. The site's layout may have changed, or it may be blocking requests.")
    else:
        st.subheader(f"Latest Headlines from {source}")
        for h in headlines:
            st.write("•", h)

        keywords = get_keywords(headlines)

        if keywords:
            df_keywords = pd.DataFrame(keywords, columns=["Keyword", "Frequency"])

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("🔥 Top Trending Keywords")
                st.bar_chart(df_keywords.set_index("Keyword"))

            with col2:
                st.subheader("☁️ Word Cloud")
                wc = WordCloud(width=600, height=400, background_color="white").generate_from_frequencies(dict(keywords))
                fig, ax = plt.subplots()
                ax.imshow(wc, interpolation="bilinear")
                ax.axis("off")
                st.pyplot(fig)
else:
    st.info("👆 Select a source and click 'Fetch Latest News' to begin.")
