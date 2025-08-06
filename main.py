from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from datetime import datetime

app = Flask(__name__)

@app.route("/scrape", methods=["POST"])
def scrape_hellowork_homepage():
    data = request.get_json()
    url = data.get("url")
    if not url:
        return jsonify({"error": "Missing URL"}), 400

    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Exemple : récupérer les <h1>, <h2> et quelques liens visibles
    h1 = soup.find("h1")
    h2_list = [h2.text.strip() for h2 in soup.find_all("h2")]
    links = [{"text": a.text.strip(), "href": a['href']} for a in soup.find_all("a", href=True)][:10]  # limiter à 10

    return jsonify({
        "ok": True,
        "message": "Scraping page d'accueil HelloWork terminé.",
        "date": datetime.today().strftime('%Y-%m-%d'),
        "url_received": url,
        "h1": h1.text.strip() if h1 else None,
        "h2_list": h2_list,
        "links": links
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
