import os
import json
import base64
from flask import Flask, request
from flask_cors import CORS  # ← 追加
from datetime import datetime
from pytz import timezone
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)
CORS(app)  # ← 追加：すべてのリクエストにCORSを許可

# スプレッドシート名（任意）
SPREADSHEET_NAME = "click_log"

# 環境変数から credentials.json を再現
base64_creds = os.environ["GOOGLE_CREDENTIALS_BASE64"]
creds_json = base64.b64decode(base64_creds).decode("utf-8")
credentials_dict = json.loads(creds_json)

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
gc = gspread.authorize(credentials)

@app.route("/click", methods=["POST"])
def log_click():
    data = request.get_json()
    event = data.get("button", "unknown")
    timestamp = datetime.now(timezone("Asia/Tokyo")).strftime("%Y-%m-%d %H:%M:%S")

    sh = gc.open(SPREADSHEET_NAME)

    try:
        sheet = sh.worksheet(event)
    except gspread.exceptions.WorksheetNotFound:
        sheet = sh.add_worksheet(title=event, rows="1000", cols="2")
        sheet.append_row(["timestamp", "event"])

    sheet.append_row([timestamp, event])
    return {"status": "ok"}

# ✅ Renderのポートで起動する（ここが重要！）
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
