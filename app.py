from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import requests
import csv
import os
from urllib.parse import urljoin
from apscheduler.schedulers.background import BackgroundScheduler
from bs4 import BeautifulSoup
from datetime import datetime

app = Flask(__name__, template_folder="templates", static_folder="static")

# --- OSINT Sources (Updated for Cyber Security News) ---
OSINT_SOURCES = [
    ("The Hacker News", "https://thehackernews.com/"),
    ("Cyber Security News", "https://www.cybersecuritynews.com/"),
    ("The Register", "https://www.theregister.com/security/"),
    ("HackRead", "https://www.hackread.com/"),
    ("GBHackers", "https://gbhackers.com/"),
    ("Cyber Security Intelligence", "https://www.cybersecurityintelligence.com/blog/category/news-cybersecurity-news-20.html"),
    ("Cyber Security Dive", "https://www.cybersecuritydive.com/topic/vulnerability/"),
    ("Cyber Express Dark Web", "https://thecyberexpress.com/firewall-daily/dark-web-news/")
]

# --- Cybercrime Keywords ---
CRIME_KEYWORDS = [
    "hacking", "cybercrime", "breach", "data leak", "phishing",
    "ransomware", "malware", "DDoS", "exploit", "zero-day", "APT",
    "cyber attack", "cyber espionage", "cyber threat", "dark web",
    "hacker", "security vulnerability", "cybersecurity incident",
    "malware", "Cybersecurity", "c2", "backdoors", "C2"
]

# --- Global Storage for Articles ---
filtered_articles = []

# --- Extract Article Published Date ---
def extract_published_date(article_page_url):
    """Fetches the article page and extracts the published date."""
    try:
        response = requests.get(article_page_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # --- Define possible date selectors for various sites ---
        date_selectors = [
            ("time", "datetime"),  # <time datetime="2024-03-01">March 1, 2024</time>
            ("meta", "article:published_time"),  # <meta property="article:published_time" content="2024-03-01T12:30:00Z"/>
            ("span", "entry-date"),  # <span class="entry-date">March 1, 2024</span>
            ("div", "date"),  # <div class="date">March 1, 2024</div>
        ]

        # Try extracting from each format
        for tag, attr in date_selectors:
            if attr == "datetime":
                date_element = soup.find(tag, datetime=True)
                if date_element:
                    return date_element["datetime"]
            else:
                date_element = soup.find(tag, attrs={"property": attr}) or soup.find(tag, class_=attr)
                if date_element:
                    return date_element.get("content") or date_element.text.strip()

    except Exception as e:
        print(f"⚠️ Error fetching article date from {article_page_url}: {e}")

    return "Unknown"  # Default if no date is found

# --- Function to Scrape OSINT Data ---
def scrape_osint_data():
    """Fetches real-time OSINT data and removes duplicates."""
    global filtered_articles
    filtered_articles.clear()
    seen_articles = set()

    for source_name, url in OSINT_SOURCES:
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")

                # Extract headlines and links correctly
                if "thehackernews.com" in url:
                    articles = soup.find_all('div', class_=lambda x: x and ('cf pop-article clear' in x or 'cf pop-article clear last-three' in x))
                elif "thecyberexpress.com/firewall-daily/dark-web-news/" in url:
                    articles = soup.find_all('h3', class_="jeg_post_title")
                elif "cybersecuritynews.com" in url:
                    articles = soup.find_all("h3", class_="entry-title td-module-title")
                elif "theregister.com" in url:
                    articles = soup.find_all('div', class_="article_text_elements")
                elif "hackread.com" in url:
                    articles = soup.find_all("h6")
                elif "gbhackers.com" in url:
                    articles = soup.find_all("h3", class_="entry-title td-module-title")
                elif "cybersecurityintelligence.com" in url:
                    articles = soup.find_all('h4', class_="list-group-item-heading")
                elif "cybersecuritydive.com" in url:
                    articles = soup.find_all('h3', class_='feed__title feed__title--display')
                else:
                    continue

                for article in articles:
                    headline_tag = article.find("a")
                    link_tag = headline_tag

                    if headline_tag and link_tag:
                        headline = headline_tag.text.strip()
                        raw_link = link_tag["href"] if "href" in link_tag.attrs else None
                        link = urljoin(url, raw_link) if raw_link else url

                        if headline and headline not in seen_articles and link:
                            seen_articles.add(headline)

                            # ✅ Extract the article's published date
                            published_date = extract_published_date(link)

                            # Store data
                            filtered_articles.append({
                                "headline": headline,
                                "url": link,
                                "source": source_name,
                                "published_date": published_date  # ✅ Display article's actual date
                            })

        except Exception as e:
            print(f"⚠️ Error fetching OSINT data from {source_name}: {e}")

# --- Route for Home Page ---
@app.route("/")
def home():
    return render_template("index.html", articles=filtered_articles)

# --- Route to Refresh Data in Real-Time ---
@app.route("/refresh")
def refresh():
    scrape_osint_data()
    return jsonify({"message": "Data refreshed successfully!", "articles": filtered_articles})

# --- Route to Export CSV ---
@app.route("/export")
def export():
    filename = "osint_cybercrime_filtered.csv"
    df = pd.DataFrame(filtered_articles)

    if not df.empty:
        df.to_csv(filename, index=False)
        return send_file(filename, as_attachment=True)
    return "No data available to export.", 404

# --- Schedule Scraper to Run Every Hour ---
scheduler = BackgroundScheduler()
scheduler.add_job(scrape_osint_data, "interval", hours=1)
scheduler.start()

# --- Run Initial Scrape ---
scrape_osint_data()

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)

    # run app in debug mode on port 5000
    app.run(debug=True, port=5000, host='0.0.0.0')

