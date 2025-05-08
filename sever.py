from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
from datetime import datetime

app = Flask(__name__)
CORS(app)  # ローカルHTMLからのアクセスを許可

@app.route("/click", methods=["POST"])
def log_click():
    data = request.get_json()
    button = data.get("button")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("click_log.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([button, timestamp])

    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(debug=True)
