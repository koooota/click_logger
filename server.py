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

@app.route("/log")
def view_log():
    log_type = request.args.get("q")
    filename = f"{log_type}.csv"

    if not os.path.exists(filename):
        return f"ログファイル '{filename}' が存在しません。", 404

    with open(filename, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)

    html = f"<h2>ログ: {filename}</h2><ul>"
    for row in rows:
        html += f"<li>{row[0]}</li>"
    html += "</ul>"

    return html


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True
            )
