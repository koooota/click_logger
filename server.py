from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# server.py のある場所
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 1つ上にある "click_counter" フォルダ
CLICK_LOG_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "click_counter"))

# フォルダがなければ作成（初回起動時も安心）
os.makedirs(CLICK_LOG_DIR, exist_ok=True)


@app.route("/click", methods=["POST"])
def log_click():
    data = request.get_json()
    button_type = data.get("button", "unknown")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 保存先ファイルパスを関数内で定義
    filename = os.path.join(CLICK_LOG_DIR, f"{button_type}.csv")

    try:
        with open(filename, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([timestamp])
        print("✅ 書き込み成功")
    except Exception as e:
        print("❌ 書き込み失敗:", e)
    
    print("✅ CSV保存先：", filename)

    return jsonify({"status": "ok"})


@app.route("/log")
def view_log():
    log_type = request.args.get("q")
    filename = os.path.join(CLICK_LOG_DIR, f"{log_type}.csv")

    if not os.path.exists(filename):
        return f"ログファイル '{filename}' が存在しません。", 404

    with open(filename, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)

    html = f"<h2>ログ: {log_type}.csv</h2><ul>"
    for row in rows:
        html += f"<li>{row[0]}</li>"
    html += "</ul>"

    return html

from flask import send_file

@app.route("/download")
def download_csv():
    log_type = request.args.get("q")
    filename = os.path.join(CLICK_LOG_DIR, f"{log_type}.csv")

    if not os.path.exists(filename):
        return f"ファイル {filename} が存在しません。", 404

    return send_file(filename, as_attachment=True)



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
    
