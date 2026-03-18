import os
import json
import base64
import secrets
import requests
from flask import Flask, redirect, request, jsonify
from datetime import datetime

# -----------------------------
# Flask App Setup
# -----------------------------
app = Flask(__name__)

# -----------------------------
# Environment Variables
# -----------------------------
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

ACCESS_TOKEN = None
REFRESH_TOKEN = None

# -----------------------------
# STEP 1: Connect Fitbit
# -----------------------------
@app.route("/connect-fitbit")
def connect_fitbit():
    state = secrets.token_hex(16)

    auth_url = (
        "https://www.fitbit.com/oauth2/authorize"
        f"?response_type=code"
        f"&client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope=activity heartrate sleep profile"
        f"&state={state}"
    )

    return redirect(auth_url)


# -----------------------------
# STEP 2: Callback
# -----------------------------
@app.route("/callback")
def callback():
    global ACCESS_TOKEN, REFRESH_TOKEN

    code = request.args.get("code")

    if not code:
        return "Authorization failed. No code received."

    token_url = "https://api.fitbit.com/oauth2/token"

    credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "client_id": CLIENT_ID,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
        "code": code
    }

    response = requests.post(token_url, headers=headers, data=data)

    if response.status_code != 200:
        return f"Token exchange failed: {response.text}"

    token_data = response.json()

    ACCESS_TOKEN = token_data.get("access_token")
    REFRESH_TOKEN = token_data.get("refresh_token")

    # Save tokens
    with open("tokens.json", "w") as f:
        json.dump(token_data, f)

    return "Fitbit connected successfully! You can close this tab."


# -----------------------------
# STEP 3: Fetch Fitbit Data
# -----------------------------
@app.route("/fetch-fitbit-data")
def fetch_fitbit_data():
    global ACCESS_TOKEN

    if not ACCESS_TOKEN:
        try:
            with open("tokens.json", "r") as f:
                token_data = json.load(f)
                ACCESS_TOKEN = token_data.get("access_token")
        except:
            return jsonify({"error": "Not connected to Fitbit"}), 401

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    today = datetime.now().strftime("%Y-%m-%d")

    # Heart Rate
    hr_response = requests.get(
        f"https://api.fitbit.com/1/user/-/activities/heart/date/{today}/1d.json",
        headers=headers
    )

    # Sleep
    sleep_response = requests.get(
        f"https://api.fitbit.com/1.2/user/-/sleep/date/{today}.json",
        headers=headers
    )

    # Activity
    activity_response = requests.get(
        f"https://api.fitbit.com/1/user/-/activities/date/{today}.json",
        headers=headers
    )

    if hr_response.status_code != 200:
        return jsonify({"error": hr_response.text}), 400

    hr_data = hr_response.json()
    sleep_data = sleep_response.json()
    activity_data = activity_response.json()

    # Extract metrics
    resting_hr = None
    try:
        resting_hr = hr_data["activities-heart"][0]["value"].get("restingHeartRate")
    except:
        resting_hr = None

    sleep_minutes = sleep_data.get("summary", {}).get("totalMinutesAsleep", 0)
    steps = activity_data.get("summary", {}).get("steps", 0)

    return jsonify({
        "resting_heart_rate": resting_hr,
        "sleep_minutes": sleep_minutes,
        "steps": steps
    })


# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True, port=5000)
