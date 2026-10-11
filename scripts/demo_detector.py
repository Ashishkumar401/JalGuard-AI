# Synthetic UI data only. These are not actual water-network sensor readings.
import json
from pathlib import Path
records = [
 {"id":"DEMO-001","timestamp":"2026-10-10 08:00","flow":48.2,"pressure":51.4,"anomaly_score":0.12,"flagged":False,"label":"Normal demo record"},
 {"id":"DEMO-002","timestamp":"2026-10-10 09:00","flow":47.9,"pressure":50.8,"anomaly_score":0.18,"flagged":False,"label":"Normal demo record"},
 {"id":"DEMO-003","timestamp":"2026-10-10 10:00","flow":63.5,"pressure":39.1,"anomaly_score":0.91,"flagged":True,"label":"Synthetic anomaly example"},
 {"id":"DEMO-004","timestamp":"2026-10-10 11:00","flow":64.2,"pressure":38.6,"anomaly_score":0.94,"flagged":True,"label":"Synthetic anomaly example"},
 {"id":"DEMO-005","timestamp":"2026-10-10 12:00","flow":49.0,"pressure":50.5,"anomaly_score":0.22,"flagged":False,"label":"Normal demo record"}
]
payload={"source":"Synthetic demo records — NOT BattLeDIM data and NOT Pune incidents.",
         "metrics":{"precision":None,"recall":None,"false_positive_rate":None,"status":"Not evaluated on benchmark labels"},
         "records":records}
out=Path(__file__).resolve().parents[1]/"frontend"/"public"/"data"/"benchmark_results.json"
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(payload,indent=2),encoding="utf-8")
print(f"Wrote {len(records)} synthetic demo rows to {out}")
