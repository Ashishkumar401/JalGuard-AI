import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
import joblib

file = Path(r"E:\movie chrome\WDSEventDB-main\WDSEventDB-main\WDSEventDB\WDSEventDB\Cyberattack\CyberEvent1-4.xlsx")
df = pd.read_excel(file)

X = df.drop(columns=["Labels"])
y = df["Labels"].astype(int)

model = RandomForestClassifier(
    n_estimators=100,
    max_depth=16,
    class_weight="balanced",
    random_state=42,
    n_jobs=2
)
model.fit(X, y)

artifact = {
    "model": model,
    "features": list(X.columns),
    "label_meaning": "Dataset Labels; confirm interpretation against dataset documentation",
    "status": "experimental",
    "dataset": "WDSEventDB Cyberattack"
}

joblib.dump(artifact, "jalguard_cyberattack_model.joblib")
print("Saved: jalguard_cyberattack_model.joblib")
print("Feature count:", len(X.columns))
print("Status: experimental; not validated for real-world deployment")
