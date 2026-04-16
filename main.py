from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

OZON_API = "https://api-seller.ozon.ru"

@app.route("/")
def index():
    return "Ozon FBO Proxy — работает ✅"

@app.route("/proxy", methods=["POST"])
def proxy():
    body = request.get_json()
    client_id = body.get("client_id", "")
    api_key   = body.get("api_key", "")
    endpoint  = body.get("endpoint", "")
    payload   = body.get("payload", {})

    if not client_id or not api_key or not endpoint:
        return jsonify({"error": "Не переданы client_id, api_key или endpoint"}), 400

    headers = {
        "Client-Id":    str(client_id),
        "Api-Key":      api_key,
        "Content-Type": "application/json",
    }

    try:
        resp = requests.post(OZON_API + endpoint, headers=headers, json=payload, timeout=30)
        return (resp.text, resp.status_code, {"Content-Type": "application/json"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
