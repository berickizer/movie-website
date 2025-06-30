import requests
from bs4 import BeautifulSoup

URL = "https://m.imdb.com/user/ur188754091/ratings"

def fetch_rated_titles():
    res = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(res.text, "html.parser")
    items = soup.select("section div div.ipc-title a")

    cards = ""
    for item in items[:5]:  # Show only top 5
        title = item.text.strip()
        link = "https://www.imdb.com" + item.get("href")
        cards += f"""
        <div class="review-card">
          <h3 style="color: #00ffcc;">🎯 {title}</h3>
          <a href="{link}" target="_blank" class="button">View on IMDb 🔍</a>
        </div>
        """
    return cards

html_path = "recommendations.html"
with open(html_path, "r") as f:
    content = f.read()

start = content.find('<div id="recommendations">')
end = content.find('</div>', start) + 6

updated_html = content[:start] + '<div id="recommendations">\n' + fetch_rated_titles() + '\n</div>' + content[end:]

with open(html_path, "w") as f:
    f.write(updated_html)
