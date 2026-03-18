import requests
import pandas as pd

INFLUX_URL = "http://localhost:8181/api/v3/query"
DATABASE = "healnet"

def read_recent_data(limit=10):
    query = f"""
    SELECT *
    FROM health_metrics
    ORDER BY time DESC
    LIMIT {limit}
    """

    response = requests.post(
        INFLUX_URL,
        params={"db": DATABASE},
        data=query
    )

    return pd.read_csv(pd.compat.StringIO(response.text))
