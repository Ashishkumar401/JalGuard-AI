from pathlib import Path
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, recall_score, f1_score, balanced_accuracy_score

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

threshold = 0.10
results = []

for test in frames:
    # Keep the complete test file out of training.
    train = [f for f in frames if f["file"] != test["file"]]
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

    pos_idx = list(model.classes_).index(1)
    probs = model.predict_proba(test["X"])[:, pos_idx]
    pred = (probs >= threshold).astype(int)
    y = test["y"]

    results.append({
        "category": test["category"],
        "file": test["file"],
        "rows": len(y),
        "actual_events": int(y.sum()),
        "predicted_events": int(pred.sum()),
        "precision": round(precision_score(y, pred, zero_division=0), 3),
        "recall": round(recall_score(y, pred, zero_division=0), 3),
        "F1": round(f1_score(y, pred, zero_division=0), 3),
        "balanced_accuracy": round(balanced_accuracy_score(y, pred), 3)
    })

out = pd.DataFrame(results)
print("\nFIXED THRESHOLD:", threshold)
print(out.to_string(index=False))
out.to_csv("all_category_threshold_test.csv", index=False)
print("\nSaved: all_category_threshold_test.csv")
