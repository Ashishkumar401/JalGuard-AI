from pathlib import Path
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, recall_score, f1_score, balanced_accuracy_score

root = Path(r"E:\movie chrome\WDSEventDB-main\WDSEventDB-main\WDSEventDB\WDSEventDB")
validation_files = {"LeakEvent2.xlsx"}
test_files = {"LeakEvent1.xlsx", "CyberEvent1-4.xlsx"}
frames = {}

for file in sorted(root.rglob("*.xlsx")):
    if "__MACOSX" in str(file) or file.name.startswith("~$"):
        continue
    if file.parent.name not in ["Clean", "Cyberattack", "Leakage", "Sensor Failure"]:
        continue

    df = pd.read_excel(file)
    if "Labels" not in df.columns:
        continue

    frames[file.name] = {
        "X": df.drop(columns=["Labels"]).astype("float32"),
        "y": df["Labels"].astype(int),
        "category": file.parent.name
    }

train = [v for name, v in frames.items()
         if name not in validation_files | test_files]

X_train = pd.concat([v["X"] for v in train], ignore_index=True)
y_train = pd.concat([v["y"] for v in train], ignore_index=True)

print("Training rows:", len(y_train))
print("Training label counts:", y_train.value_counts().sort_index().to_dict())

model = RandomForestClassifier(
    n_estimators=100,
    max_depth=16,
    min_samples_leaf=2,
    class_weight="balanced",
    random_state=42,
    n_jobs=2
)
model.fit(X_train, y_train)
pos_idx = list(model.classes_).index(1)

# Select threshold on validation file only.
val = frames["LeakEvent2.xlsx"]
val_probs = model.predict_proba(val["X"])[:, pos_idx]
threshold_scores = []

for t in [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50]:
    pred = (val_probs >= t).astype(int)
    threshold_scores.append({
        "threshold": t,
        "precision": precision_score(val["y"], pred, zero_division=0),
        "recall": recall_score(val["y"], pred, zero_division=0),
        "f1": f1_score(val["y"], pred, zero_division=0)
    })

scores = pd.DataFrame(threshold_scores)
best = scores.sort_values(["f1", "threshold"], ascending=[False, True]).iloc[0]
threshold = float(best["threshold"])

print("\nValidation threshold:", threshold)
print("Validation F1:", round(float(best["f1"]), 3))

# Evaluate only on the two untouched test files.
results = []
for name in sorted(test_files):
    item = frames[name]
    probs = model.predict_proba(item["X"])[:, pos_idx]
    pred = (probs >= threshold).astype(int)
    y = item["y"]

    results.append({
        "category": item["category"],
        "file": name,
        "actual_events": int(y.sum()),
        "predicted_events": int(pred.sum()),
        "precision": round(precision_score(y, pred, zero_division=0), 3),
        "recall": round(recall_score(y, pred, zero_division=0), 3),
        "F1": round(f1_score(y, pred, zero_division=0), 3),
        "balanced_accuracy": round(balanced_accuracy_score(y, pred), 3)
    })

result_df = pd.DataFrame(results)
print("\n=== HELD-OUT TEST RESULTS ===")
print(result_df.to_string(index=False))
result_df.to_csv("corrected_model_test_results.csv", index=False)
scores.to_csv("corrected_threshold_scores.csv", index=False)
print("\nSaved corrected_model_test_results.csv")
print("Saved corrected_threshold_scores.csv")
