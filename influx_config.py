# backend/influx_config.py

from influxdb_client_3 import InfluxDBClient3

# Update these values after setting up InfluxDB
INFLUX_URL = "http://localhost:8181"
INFLUX_TOKEN = "b7kTRovNbLUNwB8TB57OsmHGVUHpl-JFUssxpTGxihMo7EOCQB_07IUxzMxl6eDPfCB20IvQxJgl7xk-sZZP6w=="     
INFLUX_ORG = "healnet_org"
INFLUX_BUCKET = "healnet_bucket"

def get_client():
    client = InfluxDBClient3(
        host=INFLUX_URL,
        token=INFLUX_TOKEN,
        org=INFLUX_ORG
    )
    return client
