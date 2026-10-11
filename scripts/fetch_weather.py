import json
from pathlib import Path
import requests

URL = "https://archive-api.open-meteo.com/v1/archive"
PARAMS = {
    "latitude": 18.52, "longitude": 73.86,
    "start_date": "2026-10-01", "end_date": "2026-10-10",
    "daily": "temperature_2m_max,apparent_temperature_max,precipitation_sum",
    "timezone": "Asia/Kolkata"
}
def main():
    response = requests.get(URL, params=PARAMS, timeout=30)
    response.raise_for_status()
    raw = response.json()
    daily = raw.get("daily", {})
    dates = daily.get("time", [])
    result = {
        "source": "Open-Meteo Historical Weather API",
        "source_url": "https://open-meteo.com/en/docs/historical-weather-api",
        "location": {"name":"Pune, Maharashtra, India","latitude":18.52,"longitude":73.86},
        "daily": []
    }
    for i, date in enumerate(dates):
        result["daily"].append({
            "date": date,
            "temperature_max_c": daily.get("temperature_2m_max", [None]*len(dates))[i],
            "apparent_temperature_max_c": daily.get("apparent_temperature_max", [None]*len(dates))[i],
            "precipitation_mm": daily.get("precipitation_sum", [None]*len(dates))[i]
        })
    out = Path(__file__).resolve().parents[1] / "frontend" / "public" / "data" / "pune_weather.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"Saved {len(result['daily'])} daily records to {out}")
if __name__ == "__main__":
    main()
