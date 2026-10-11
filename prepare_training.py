from pathlib import Path
import pandas as pd

root = Path(r"E:\movie chrome\WDSEventDB-main\WDSEventDB-main\WDSEventDB\WDSEventDB")
files = []

for file in sorted(root.rglob("*.xlsx")):
    if "__MACOSX" in str(file) or file.name.startswith("~$"):
        continue
    if file.parent.name not in ["Clean", "Cyberattack", "Leakage", "Sensor Failure"]:
        continue

    df = pd.read_excel(file)
    if "Labels" not in df.columns:
        continue

    files.append({
        "category": file.parent.name,
        "file": file.name,
        "rows": len(df),
        "label_0": int((df["Labels"] == 0).sum()),
        "label_1": int((df["Labels"] == 1).sum())
    })

summary = pd.DataFrame(files)
print(summary.to_string(index=False))
print("\nFiles available:", len(summary))
print("Ready for file-based evaluation.")
