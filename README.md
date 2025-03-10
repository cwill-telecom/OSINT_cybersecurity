

<h1 align="center">🔍 OSINT Cyber Threat Intelligence Scraper</h1>

<p>
  <b>A Flask-based web application that automates Open Source Intelligence (OSINT) gathering from leading cybersecurity news sources.</b><br>
  The tool scrapes real-time cyber threat data, filters it using cybercrime-related keywords, and allows exporting data to CSV for analysis.
</p>

---

<h2>Features</h2>

✅ <b>Automated Web Scraping</b> – Gathers cybersecurity intelligence from top OSINT sources. <br>
✅ <b>Real-Time Threat Monitoring</b> – Periodic data refresh using <code>APScheduler</code>. <br>
✅ <b>Cybercrime Keyword Filtering</b> – Focus on <i>breaches, exploits, malware, ransomware, and APT threats</i>. <br>
✅ <b>Extract Article Publish Dates</b> – Improves timeline analysis of threats. <br>
✅ <b>Web-Based UI</b> – View articles in a simple Flask-powered dashboard. <br>
✅ <b>CSV Export</b> – Download filtered intelligence reports for analysis. <br>

---

<h2>📡 OSINT Sources Monitored</h2>

<ul>
  <li>🔸 <a href="https://thehackernews.com/">The Hacker News</a></li>
  <li>🔸 <a href="https://www.cybersecuritynews.com/">Cyber Security News</a></li>
  <li>🔸 <a href="https://www.theregister.com/security/">The Register</a></li>
  <li>🔸 <a href="https://www.hackread.com/">HackRead</a></li>
  <li>🔸 <a href="https://gbhackers.com/">GBHackers</a></li>
  <li>🔸 <a href="https://www.cybersecurityintelligence.com/">Cyber Security Intelligence</a></li>
  <li>🔸 <a href="https://www.cybersecuritydive.com/topic/vulnerability/">Cyber Security Dive</a></li>
  <li>🔸 <a href="https://thecyberexpress.com/firewall-daily/dark-web-news/">Dark Web News (Cyber Express)</a></li>
</ul>

# 📂 Installation & Setup

Follow these steps to install and run the OSINT Cyber Threat Intelligence Scraper.

1️⃣ Clone the Repository

Run the following commands:

```bash
git clone https://github.com/yourusername/osint-cyber-scraper.git
cd osint-cyber-scraper

 ```

2️⃣ Install Dependencies
Install the required Python packages:
```bash
pip install -r requirements.txt

 ```
3️⃣ Run the Flask Application
Start the Flask server:
```bash
python app.py

 ```
Now, open http://127.0.0.1:5000/ in your browser.


