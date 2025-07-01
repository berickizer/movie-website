import requests
from bs4 import BeautifulSoup

IMDB_USER_ID = "ur188754091"
IMDB_URL = f"https://m.imdb.com/user/{IMDB_USER_ID}/ratings"
OUTPUT_FILE = "recommendations.html"

def fetch_recommendations():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    response = requests.get(IMDB_URL, headers=headers)
    if response.status_code != 200:
        raise Exception("Failed to fetch IMDb page")

    soup = BeautifulSoup(response.text, "html.parser")
    items = soup.select("div.col-title")[:6]  # Top 6 rated titles

    reviews_html = ""

    for item in items:
        title_tag = item.find("a")
        if not title_tag:
            continue

        title = title_tag.text.strip()
        href = title_tag["href"]
        imdb_link = "https://www.imdb.com" + href
        poster = "https://via.placeholder.com/400x600?text=No+Image"

        rating_tag = item.find_next("span", class_="rating-rating")
        rating = rating_tag.text.strip() if rating_tag else "⭐⭐⭐⭐⭐⭐⭐⭐ (8/10)"

        reviews_html += f"""
        <div class="review-card">
          <h3 style="color: #00ffcc;">🎬 {title}</h3>
          <img src="{poster}" alt="{title} Poster">
          <p><strong>Why Watch:</strong> Personally recommended by Fakira based on IMDb ratings and rewatch value.</p>
          <p><strong>Rating:</strong> {rating}</p>
          <a href="{imdb_link}" target="_blank" class="button">More Info 🔍</a>
        </div>
        """

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html>
<html>
<head>
  <title>Recommendations – Fakira Movie Zone</title>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <link rel="stylesheet" href="style.css" />
</head>
<body>

  <!-- Top Navigation -->
  <div class="top-nav">
    <a href="/movie-website/index.html">🏠 Home</a>
    <a href="/movie-website/movies.html">🎬 Movies</a>
    <a href="/movie-website/tvshows.html">📺 TV Shows</a>
    <a href="/movie-website/latest.html">🆕 Latest</a>
    <a href="/movie-website/recommendations.html">🤖 Recommendations</a>
    <a href="/movie-website/disclaimer.html">⚖️ Disclaimer</a>
  </div>

  <h2 class="section-title">🤖 Recommended by Fakira</h2>
  <p style="text-align:center;">Auto-updated from <a href="https://www.imdb.com/user/{IMDB_USER_ID}/" target="_blank">IMDb profile</a> daily. Handpicked and rated by Fakira.</p>

  <div class="review-grid">
    {reviews_html}
  </div>

</body>
</html>
""")

if __name__ == "__main__":
    fetch_recommendations()
