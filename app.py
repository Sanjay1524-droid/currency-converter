from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Using free ExchangeRate-API (no key needed for basic endpoint)
EXCHANGE_API = "https://open.er-api.com/v6/latest"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/convert", methods=["POST"])
def convert():
    data = request.get_json()
    amount = float(data.get("amount", 1))
    from_currency = data.get("from_currency", "USD").upper()
    to_currency = data.get("to_currency", "INR").upper()

    try:
        response = requests.get(f"{EXCHANGE_API}/{from_currency}", timeout=5)
        res_data = response.json()

        if res_data.get("result") != "success":
            return jsonify({"error": "Failed to fetch rates"}), 400

        rates = res_data["rates"]
        if to_currency not in rates:
            return jsonify({"error": f"Currency {to_currency} not supported"}), 400

        rate = rates[to_currency]
        converted = round(amount * rate, 4)

        return jsonify({
            "from": from_currency,
            "to": to_currency,
            "amount": amount,
            "converted": converted,
            "rate": rate
        })

    except requests.exceptions.RequestException:
        return jsonify({"error": "Network error. Check your internet connection."}), 500

@app.route("/currencies")
def currencies():
    try:
        response = requests.get(f"{EXCHANGE_API}/USD", timeout=5)
        data = response.json()
        if data.get("result") == "success":
            return jsonify(sorted(data["rates"].keys()))
    except:
        pass
    # Fallback common currencies
    return jsonify(["AED","AUD","BRL","CAD","CHF","CNY","EUR","GBP","HKD","IDR",
                    "INR","JPY","KRW","MXN","MYR","NOK","NZD","PHP","PKR","SAR",
                    "SEK","SGD","THB","TRY","TWD","USD","ZAR"])

if __name__ == "__main__":
    app.run(debug=True)
