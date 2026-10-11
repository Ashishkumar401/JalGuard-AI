from pathlib import Path
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

root = Path(r"E:\movie chrome\WDSEventDB-main\WDSEventDB-main\WDSEventDB\WDSEventDB")
frames = []

for file in sorted(root.rglob("*.xlsx")):
    if "__MACOSX" in str(file) or file.name.startswith("~$"):
        continue
    if file.parent.name not in ["Clean", "Cyberattack", "Leakage", "Sensor Failure"]:
        continue

    df = pd.read_excel(file)
    if "Labels" not in df.columns:
        continue

    frames.append({
        "X": df.drop(columns=["Labels"]).astype("float32"),
        "y": df["Labels"].astype(int),
        "file": file.name
    })

# Hold out the cyberattack file completely.
train = [f for f in frames if f["file"] != "CyberEvent1-4.xlsx"]
X_train = pd.concat([f["X"] for f in train], ignore_index=True)
y_train = pd.concat([f["y"] for f in train], ignore_index=True)

model = RandomForestClassifier(
    n_estimators=100,
    max_depth=16,
    min_samples_leaf=2,
    class_weight="balanced",
    random_state=42,
    n_jobs=2
)
model.fit(X_train, y_train)

importance = pd.DataFrame({
    "sensor": X_train.columns,
    "importance": model.feature_importances_
}).sort_values("importance", ascending=False)

print("Top sensor features:")
print(importance.to_string(index=False))
importance.to_csv("sensor_feature_importance.csv", index=False)
print("\nSaved: sensor_feature_importance.csv")
