import requests
import pandas as pd
from io import StringIO

# ===============================
# InfluxDB Configuration
# ===============================
INFLUX_URL = "http://localhost:8086"
ORG = "healnet-org"
BUCKET = "healnet"

# ✅ TOKEN MUST BE STRING
INFLUX_TOKEN = "b7kTRovNbLUNwB8TB57OsmHGVUHpl-JFUssxpTGxihMo7EOCQB_07IUxzMxl6eDPfCB20IvQxJgl7xk-sZZP6w=="

QUERY_URL = f"{INFLUX_URL}/api/v2/query"


# ===============================
# Fetch Health Data
# ===============================
def fetch_health_data(patient_id, hours=6):

    flux_query = f'''
    from(bucket: "{BUCKET}")
      |> range(start: -{hours}h)
      |> filter(fn: (r) => r._measurement == "health_metrics")
      |> filter(fn: (r) => r.patient_id == "{patient_id}")
    '''

    headers = {
        "Authorization": f"Token {INFLUX_TOKEN}",   # ✅ correct usage
        "Content-Type": "application/vnd.flux"
    }

    response = requests.post(
        QUERY_URL,
        headers=headers,
        params={"org": ORG},
        data=flux_query
    )

    if response.status_code != 200:
        print("Query Error:", response.text)
        return pd.DataFrame()

    df = pd.read_csv(StringIO(response.text), comment="#")
    return df