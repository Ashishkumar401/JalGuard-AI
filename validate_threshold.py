from pathlib import Path
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, recall_score, f1_score

root = Path(r"E:\movie chrome\WDSEventDB-main\WDSEventDB-main\WDSEventDB\WDSEventDB")
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

# Test file stays completely separate from threshold selection.
test_name = "LeakEvent1.xlsx"
validation_name = "LeakEvent2.xlsx"

train = [v for k, v in frames.items() if k not in [test_name, validation_name]]
val = frames[validation_name]
test = frames[test_name]

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
val_probs = model.predict_proba(val["X"])[:, positive_index]

# Choose threshold on validation file only.
candidates = [0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50]
scores = []

for threshold in candidates:
    pred = (val_probs >= threshold).astype(int)
    scores.append((
        f1_score(val["y"], pred, zero_division=0),
        threshold,
        precision_score(val["y"], pred, zero_division=0),
        recall_score(val["y"], pred, zero_division=0)
    ))

best_f1, best_threshold, val_precision, val_recall = max(scores)

# Evaluate the locked threshold once on the untouched test file.
test_probs = model.predict_proba(test["X"])[:, positive_index]
test_pred = (test_probs >= best_threshold).astype(int)

print("Validation file:", validation_name)
print("Selected threshold:", best_threshold)
print(f"Validation precision={val_precision:.3f}, recall={val_recall:.3f}, F1={best_f1:.3f}")

print("\nUntouched test file:", test_name)
print(f"Test precision={precision_score(test['y'], test_pred, zero_division=0):.3f}")
print(f"Test recall={recall_score(test['y'], test_pred, zero_division=0):.3f}")
print(f"Test F1={f1_score(test['y'], test_pred, zero_division=0):.3f}")
print("Actual events:", int(test["y"].sum()))
print("Predicted events:", int(test_pred.sum()))
print("\nNote: this is one validation/test split, not a final generalization claim.")
