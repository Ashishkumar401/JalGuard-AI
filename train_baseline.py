from pathlib import Path
import warnings
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    balanced_accuracy_score,
    f1_score
)

warnings.filterwarnings("ignore")

root = Path(r"E:\movie chrome\WDSEventDB-main\WDSEventDB-main\WDSEventDB\WDSEventDB")
frames = []
feature_columns = None

for file in sorted(root.rglob("*.xlsx")):
    if "__MACOSX" in str(file) or file.name.startswith("~$"):
        continue
    if file.parent.name not in ["Clean", "Cyberattack", "Leakage", "Sensor Failure"]:
        continue

    df = pd.read_excel(file)
    if "Labels" not in df.columns:
        continue

    if not set(df["Labels"].dropna().unique()).issubset({0, 1}):
        print("Skipping unexpected labels:", file.name)
        continue

    features = df.drop(columns=["Labels"])
    if feature_columns is None:
        feature_columns = features.columns.tolist()

    if features.columns.tolist() != feature_columns:
        print("Skipping mismatched columns:", file.name)
        continue

    frames.append({
        "X": features.astype("float32"),
        "y": df["Labels"].astype(int),
        "file": file.name,
        "category": file.parent.name
    })

if len(frames) < 3:
    raise SystemExit("Not enough valid files to evaluate.")

actual_all = []
pred_all = []
results = []

for test_i, test in enumerate(frames):
    train_frames = [f for i, f in enumerate(frames) if i != test_i]
    X_train = pd.concat([f["X"] for f in train_frames], ignore_index=True)
    y_train = pd.concat([f["y"] for f in train_frames], ignore_index=True)
    X_test, y_test = test["X"], test["y"]

    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=16,
        min_samples_leaf=2,
        class_weight="balanced",
        random_state=42,
        n_jobs=2
    )
    model.fit(X_train, y_train)
    pred = model.predict(X_test)

    actual_all.extend(y_test.tolist())
    pred_all.extend(pred.tolist())

    results.append({
        "category": test["category"],
        "file": test["file"],
        "rows": len(y_test),
        "positive_label_1": int(y_test.sum()),
        "F1_label_1": round(f1_score(y_test, pred, zero_division=0), 4),
        "balanced_accuracy": round(balanced_accuracy_score(y_test, pred), 4)
    })

print("\n=== HELD-OUT FILE RESULTS ===")
print(pd.DataFrame(results).to_string(index=False))

print("\n=== COMBINED OUT-OF-FILE RESULTS ===")
print("Confusion matrix (rows=actual, columns=predicted; labels 0,1):")
print(confusion_matrix(actual_all, pred_all, labels=[0, 1]))
print("\nClassification report:")
print(classification_report(
    actual_all, pred_all, labels=[0, 1],
    target_names=["Label 0", "Label 1"],
    digits=4, zero_division=0
))

out = Path("baseline_file_holdout_results.csv")
pd.DataFrame(results).to_csv(out, index=False)
print("Per-file results saved to:", out.resolve())
print("\nNote: label meaning is provisional; these results do not prove real-world performance.")
