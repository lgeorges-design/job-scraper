from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from datetime import datetime

app = Flask(__name__)

@app.route("/scrape", methods=["POST"])
def scrape_makesense():
    data = request.get_json()
    url = data.get("url")
    if not url:
        return jsonify({"error": "Missing URL"}), 400

    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    results = []
    cards = soup.find_all("article", class_="job-card")

    for card in cards:
        titre = card.find("div", class_="job-card__title")
        entreprise = card.find("div", class_="job-card__company")
        lieu = card.find("div", class_="job-card__location")
        lien = card.find("a", href=True)

        if not titre or not entreprise or not lieu or not lien:
            continue

        results.append({
            "date": datetime.today().strftime('%Y-%m-%d'),
            "source": "MakeSense",
            "entreprise": entreprise.text.strip(),
            "localisation": lieu.text.strip(),
            "secteur": "",
            "taille_entreprise": "",
            "poste": titre.text.strip(),
            "experience_demande": "",
            "competences": [],
            "score": 80,
            "pitch": "",
            "statut": "À traiter",
            "date_candidature": "",
            "date_reponse": "",
            "delai_reponse": "",
            "commentaires": "",
            "lien": "https://jobs.makesense.org" + lien['href']
        })

    return jsonify(results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)