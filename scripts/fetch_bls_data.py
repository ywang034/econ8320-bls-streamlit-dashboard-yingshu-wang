import requests
import pandas as pd
from datetime import datetime

API_KEY = ""

SERIES_IDS = {
    "LNS14000000": "Unemployment Rate",
    "CES0000000001": "Total Nonfarm Employment",
    "CES0500000002": "Avg Weekly Hours (Private)",
    "CES0500000003": "Avg Hourly Earnings (Private)"
}

def fetch_bls(start_year, end_year):
    url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
    
    payload = {
        "seriesid": list(SERIES_IDS.keys()),
        "startyear": start_year,
        "endyear": end_year
    }

    if API_KEY:
        payload["registrationKey"] = API_KEY

    response = requests.post(url, json=payload).json()
    
    all_rows = []

    for series in response["Results"]["series"]:
        sid = series["seriesID"]
        name = SERIES_IDS[sid]

        for d in series["data"]:
            if d["period"][0] != "M":
                continue
            all_rows.append({
                "series_id": sid,
                "series_name": name,
                "year": int(d["year"]),
                "month": int(d["period"][1:]),
                "value": float(d["value"])
            })

    df = pd.DataFrame(all_rows)
    df["date"] = pd.to_datetime(df[["year", "month"]].assign(day=1))

    return df.sort_values("series_id")

if __name__ == "__main__":
    df = fetch_bls(2020, datetime.now().year)
    df.to_csv("data/bls_data.csv", index=False)
