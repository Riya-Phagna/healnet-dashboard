import requests
import csv
import os
from datetime import datetime


# ==============================
# InfluxDB Configuration (2.x)
# ==============================

INFLUX_URL = "http://localhost:8086/api/v2/write?org=healnet-org&bucket=healnet&precision=ns"
INFLUX_TOKEN = "b7kTRovNbLUNwB8TB57OsmHGVUHpl-JFUssxpTGxihMo7EOCQB_07IUxzMxl6eDPfCB20IvQxJgl7xk-sZZP6w=="

INFLUX_WRITE_URL = "http://localhost:8086/api/v2/write"
INFLUX_TOKEN = "b7kTRovNbLUNwB8TB57OsmHGVUHpl-JFUssxpTGxihMo7EOCQB_07IUxzMxl6eDPfCB20IvQxJgl7xk-sZZP6w=="
ORG = "healnet-org"
BUCKET = "healnet"


def write_health_data(timestamp,
                      heart_rate,
                      spo2,
                      sleep_hours,
                      steps,
                      risk_score,
                      patient_id):

    # Convert timestamp to nanoseconds
    timestamp_ns = int(timestamp * 1e9)

    # Line protocol format
    line = (
        f"health_metrics,patient_id={patient_id} "
        f"heart_rate={heart_rate},"
        f"spo2={spo2},"
        f"sleep_hours={sleep_hours},"
        f"steps={steps},"
        f"risk_score={risk_score} "
        f"{timestamp_ns}"
    )

    response = requests.post(
        INFLUX_WRITE_URL,
        params={
            "org": ORG,
            "bucket": BUCKET,
            "precision": "ns"
        },
        headers={
            "Authorization": f"Token {INFLUX_TOKEN}",
            "Content-Type": "text/plain"
        },
        data=line
    )

    if response.status_code != 204:
        print("InfluxDB Write Error:", response.text)


CSV_FALLBACK_FILE = "output/influx_fallback.csv"


def write_health_data(
    timestamp,
    heart_rate,
    spo2,
    sleep_hours,
    steps,
    risk_score,
    patient_id="P001"   # ✅ Added Multi-Patient Support
):
    # Ensure output folder exists
    os.makedirs("output", exist_ok=True)

    # If timestamp not provided, use current time
    if timestamp is None:
        timestamp = datetime.utcnow()

    # Safe timestamp handling
    if isinstance(timestamp, (int, float)):
        timestamp_ns = int(timestamp * 1e9)
    else:
        timestamp_ns = int(timestamp.timestamp() * 1e9)

    # ==============================
    # InfluxDB Line Protocol
    # ==============================

    line_protocol = (
        f"health_metrics,patient_id={patient_id} "
        f"heart_rate={heart_rate},"
        f"spo2={spo2},"
        f"sleep_hours={sleep_hours},"
        f"steps={steps},"
        f"risk_score={risk_score} "
        f"{timestamp_ns}"
    )

    try:
        response = requests.post(
            INFLUX_URL,
            data=line_protocol,
            headers={
                "Authorization": f"Token {INFLUX_TOKEN}",
                "Content-Type": "text/plain; charset=utf-8"
            },
            timeout=5
        )

        if response.status_code in [200, 204]:
            print("✅ Data written to InfluxDB successfully")
            return
        else:
            print(f"❌ InfluxDB Error: {response.status_code}")
            print(response.text)

    except Exception as e:
        print("❌ InfluxDB not available:", str(e))

    # ==============================
    # CSV FALLBACK
    # ==============================

    file_exists = os.path.exists(CSV_FALLBACK_FILE)

    with open(CSV_FALLBACK_FILE, mode="a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow([
                "timestamp",
                "patient_id",
                "heart_rate",
                "spo2",
                "sleep_hours",
                "steps",
                "risk_score"
            ])

        writer.writerow([
            datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            patient_id,
            heart_rate,
            spo2,
            sleep_hours,
            steps,
            risk_score
        ])

    print("📁 Data saved to CSV fallback")
