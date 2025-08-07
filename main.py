from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from datetime import datetime
import traceback

app = Flask(__name__)

@app.route("/scrape", methods=["POST"])
def scrape_page():
    data = request.get_json()
    url = data.get("url")
    timeout_ms = data.get("timeout_ms", 5000)

    if not url:
        return jsonify({"error": "Missing URL"}), 400

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            try:
                page = browser.new_page()
                page.goto(url, timeout=60000)
                page.wait_for_timeout(timeout_ms)

                cards = page.query_selector_all("div.JobCard_card__primaryContainer__g6oiP")
                results = []

                for card in cards:
                    titre_el = card.query_selector("h2")
                    entreprise_el = card.query_selector(".JobCard_card__company__EmAvV")
                    localisation_el = card.query_selector(".JobCard_card__location__yG0sQ")
                    lien_el = card.query_selector("a")

                    if not all([titre_el, entreprise_el, localisation_el, lien_el]):
                        continue

                    results.append({
                        "date": datetime.today().strftime('%Y-%m-%d'),
                        "source": "MakeSense",
                        "entreprise": entreprise_el.inner_text().strip(),
                        "localisation": localisation_el.inner_text().strip(),
                        "secteur": "",
                        "taille_entreprise": "",
                        "poste": titre_el.inner_text().strip(),
                        "experience_demande": "",
                        "competences": [],
                        "score": 80,
                        "pitch": "",
                        "statut": "À traiter",
                        "date_candidature": "",
                        "date_reponse": "",
                        "delai_reponse": "",
                        "commentaires": "",
                        "lien": lien_el.get_attribute("href")
                    })

                return jsonify(results)
            finally:
                browser.close()

    except PlaywrightTimeoutError:
        return jsonify({"error": "Timeout while loading the page"}), 504
    except Exception as e:
        print("❌ Exception lors de l'exécution de Playwright :")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "Playwright scraper for jobs.makesense.org is running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)