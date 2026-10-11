from pathlib import Path
import pandas as pd

root = Path(r"E:\movie chrome\WDSEventDB-main\WDSEventDB-main\WDSEventDB\WDSEventDB")
frames = []

for file in sorted(root.rglob("*.xlsx")):
    if "__MACOSX" in str(file) or file.name.startswith("~$"):
        continue
    category = file.parent.name
    if category not in ["Clean", "Cyberattack", "Leakage", "Sensor Failure"]:
        continue

    df = pd.read_excel(file)
    if "Labels" not in df.columns:
        continue

    df["Category"] = category
    df["SourceFile"] = file.name
    frames.append(df)

data = pd.concat(frames, ignore_index=True)
print("Total rows:", len(data))
print("\nRows by category:")
print(data.groupby("Category").size().to_string())
print("\nLabels by category:")
print(pd.crosstab(data["Category"], data["Labels"]).to_string())
print("\nMissing values:", int(data.isna().sum().sum()))

out = Path("dataset_summary.csv")
pd.crosstab(data["Category"], data["Labels"]).to_csv(out)
print("\nSummary saved to:", out.resolve())
