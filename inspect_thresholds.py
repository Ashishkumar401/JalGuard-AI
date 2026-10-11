from pathlib import Path
import pandas as pd
import numpy as np
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
        "file": file.name,
        "category": file.parent.name
    })

# Inspect leakage event file as an unseen test file.
test = next(f for f in frames if f["file"] == "LeakEvent1.xlsx")
train = [f for f in frames if f["file"] != "LeakEvent1.xlsx"]

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

probs = model.predict_proba(test["X"])[:, list(model.classes_).index(1)]
print("Test file:", test["file"])
print("Actual label-1 count:", int(test["y"].sum()))
print("Probability min / median / max:",
      round(float(probs.min()), 4),
      round(float(np.median(probs)), 4),
      round(float(probs.max()), 4))

for threshold in [0.2, 0.3, 0.4, 0.5, 0.6]:
    pred = (probs >= threshold).astype(int)
    tp = int(((pred == 1) & (test["y"].to_numpy() == 1)).sum())
    fp = int(((pred == 1) & (test["y"].to_numpy() == 0)).sum())
    fn = int(((pred == 0) & (test["y"].to_numpy() == 1)).sum())
    precision = tp / (tp + fp) if tp + fp else 0
    recall = tp / (tp + fn) if tp + fn else 0
    print(f"Threshold {threshold:.1f}: predicted_events={int(pred.sum())}, "
          f"precision={precision:.3f}, recall={recall:.3f}")
