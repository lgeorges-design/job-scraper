from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/scrape", methods=["POST"])
def test_scrape():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "Missing URL"}), 400

    return jsonify({
        "ok": True,
        "url_received": url,
        "message": "Le endpoint /scrape fonctionne correctement."
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)