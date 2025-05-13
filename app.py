import os
import json
import base64
from flask import Flask, request
from datetime import datetime
from pytz import timezone
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

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
