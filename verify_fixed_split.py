from pathlib import Path
import pandas as pd

root = Path(r"E:\movie chrome\WDSEventDB-main\WDSEventDB-main\WDSEventDB\WDSEventDB")

# Keep one file for validation and two files as unseen tests.
validation_files = {"LeakEvent2.xlsx"}
test_files = {"LeakEvent1.xlsx", "CyberEvent1-4.xlsx"}

for file in sorted(root.rglob("*.xlsx")):
    if "__MACOSX" in str(file) or file.name.startswith("~$"):
        continue
    if file.parent.name not in ["Clean", "Cyberattack", "Leakage", "Sensor Failure"]:
        continue

    df = pd.read_excel(file)
    if "Labels" not in df.columns:
        continue

    if file.name in validation_files:
        split = "VALIDATION"
    elif file.name in test_files:
        split = "TEST"
    else:
        split = "TRAIN"

    counts = df["Labels"].value_counts().to_dict()
    print(f"{split:10} | {file.parent.name:15} | {file.name:25} | {counts}")
