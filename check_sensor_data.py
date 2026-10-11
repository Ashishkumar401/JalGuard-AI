from pathlib import Path
import pandas as pd

root = Path(r"E:\movie chrome\WDSEventDB-main\WDSEventDB-main\WDSEventDB\WDSEventDB")

for file in sorted(root.rglob("*.xlsx")):
    if "__MACOSX" in str(file) or file.name.startswith("~$"):
        continue
    if file.parent.name not in ["Clean", "Cyberattack", "Leakage", "Sensor Failure"]:
        continue

    df = pd.read_excel(file)
    if "Labels" not in df.columns:
        continue

    features = df.drop(columns=["Labels"])
    numeric = features.select_dtypes(include="number").columns.tolist()

    print(f"\n{file.parent.name} / {file.name}")
    print("Rows:", len(df))
    print("Numeric sensor columns:", len(numeric))
    print("Non-numeric columns:", [c for c in features.columns if c not in numeric])
    print("Label counts:", df["Labels"].value_counts().sort_index().to_dict())
    print("Infinite values:", int((features.select_dtypes(include="number").isin([float("inf"), float("-inf")])).sum().sum()))
