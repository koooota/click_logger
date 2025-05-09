from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

@app.route("/click", methods=["POST"])
def log_click():
    data = request.get_json()
    button_type = data.get("button", "unknown")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 安全なファイル名に変換
    safe_filename = f"{button_type}.csv"

    # 書き込み処理
    with open(safe_filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp])

    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(debug=True)
