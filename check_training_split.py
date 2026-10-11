from pathlib import Path
import pandas as pd

root = Path(r"E:\movie chrome\WDSEventDB-main\WDSEventDB-main\WDSEventDB\WDSEventDB")
validation_file = "LeakEvent2.xlsx"
test_files = [
    "LeakEvent1.xlsx", "LeakEvent3.xlsx",
    "SensorEvent1.xlsx", "SensorEvent23.xlsx",
    "SensorEvent45.xlsx", "SensorEvent67.xlsx",
    "CyberEvent1-4.xlsx"
]

excluded = [validation_file] + test_files
total_rows = 0
label_counts = {0: 0, 1: 0}

for file in sorted(root.rglob("*.xlsx")):
    if "__MACOSX" in str(file) or file.name.startswith("~$"):
        continue
    if file.parent.name not in ["Clean", "Cyberattack", "Leakage", "Sensor Failure"]:
        continue
    if file.name in excluded:
        continue

    df = pd.read_excel(file)
    if "Labels" not in df.columns:
        continue

    print(file.parent.name, file.name, df["Labels"].value_counts().to_dict())
    total_rows += len(df)
    counts = df["Labels"].value_counts()
    for label in [0, 1]:
        label_counts[label] += int(counts.get(label, 0))

print("\nTraining rows:", total_rows)
print("Training labels:", label_counts)
