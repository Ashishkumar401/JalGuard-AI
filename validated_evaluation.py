from pathlib import Path
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, recall_score, f1_score, balanced_accuracy_score

root = Path(r"E:\movie chrome\WDSEventDB-main\WDSEventDB-main\WDSEventDB\WDSEventDB")
data = {}

for file in sorted(root.rglob("*.xlsx")):
    if "__MACOSX" in str(file) or file.name.startswith("~$"):
        continue
    if file.parent.name not in ["Clean", "Cyberattack", "Leakage", "Sensor Failure"]:
        continue

    df = pd.read_excel(file)
    if "Labels" not in df.columns:
        continue

    data[file.name] = {
        "X": df.drop(columns=["Labels"]).astype("float32"),
        "y": df["Labels"].astype(int),
        "category": file.parent.name
    }

# Fixed split: validation file selects threshold; test file remains unseen.
validation_file = "LeakEvent2.xlsx"
test_files = ["LeakEvent1.xlsx", "LeakEvent3.xlsx",
              "SensorEvent1.xlsx", "SensorEvent23.xlsx",
              "SensorEvent45.xlsx", "SensorEvent67.xlsx",
              "CyberEvent1-4.xlsx"]

excluded = [validation_file] + test_files
train = [v for name, v in data.items() if name not in excluded]

if validation_file not in data or any(name not in data for name in test_files):
    raise SystemExit("A required validation/test file was not found.")

X_train = pd.concat([v["X"] for v in train], ignore_index=True)
y_train = pd.concat([v["y"] for v in train], ignore_index=True)

model = RandomForestClassifier(
    n_estimators=100,
    max_depth=16,
    min_samples_leaf=2,
    class_weight="balanced",
    random_state=42,
    n_jobs=2
)
model.fit(X_train, y_train)

positive_index = list(model.classes_).index(1)
val = data[validation_file]
val_probs = model.predict_proba(val["X"])[:, positive_index]

thresholds = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50]
scores = []

for t in thresholds:
    pred = (val_probs >= t).astype(int)
    scores.append({
        "threshold": t,
        "precision": precision_score(val["y"], pred, zero_division=0),
        "recall": recall_score(val["y"], pred, zero_division=0),
        "f1": f1_score(val["y"], pred, zero_division=0)
    })

score_df = pd.DataFrame(scores)
best = score_df.sort_values(["f1", "threshold"], ascending=[False, True]).iloc[0]
threshold = float(best["threshold"])

print("Validation file:", validation_file)
print("Selected threshold:", threshold)
print("Validation F1:", round(float(best["f1"]), 3))

results = []
for name in test_files:
    item = data[name]
    probs = model.predict_proba(item["X"])[:, positive_index]
    pred = (probs >= threshold).astype(int)
    y = item["y"]

    results.append({
        "category": item["category"],
        "file": name,
        "rows": len(y),
        "actual_events": int(y.sum()),
        "predicted_events": int(pred.sum()),
        "precision": round(precision_score(y, pred, zero_division=0), 3),
        "recall": round(recall_score(y, pred, zero_division=0), 3),
        "F1": round(f1_score(y, pred, zero_division=0), 3),
        "balanced_accuracy": round(balanced_accuracy_score(y, pred), 3)
    })

result_df = pd.DataFrame(results)
print("\n=== UNSEEN TEST FILE RESULTS ===")
print(result_df.to_string(index=False))
result_df.to_csv("validated_event_detection_results.csv", index=False)
score_df.to_csv("validation_threshold_scores.csv", index=False)
print("\nSaved: validated_event_detection_results.csv")
print("Saved: validation_threshold_scores.csv")
print("\nCaution: results cover this fixed split only; the threshold is selected on one leakage validation file.")
