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

    print(f"\n{file.parent.name} / {file.name}")
    print(df[["Pressure 1 Out", "Water Flow 1", "Labels"]].iloc[:3].to_string(index=False))
    print("First label transitions:")
    changes = df.index[df["Labels"].ne(df["Labels"].shift())].tolist()
    for i in changes[:4]:
        print(df.iloc[max(0, i-1):min(len(df), i+2)][["Pressure 1 Out", "Water Flow 1", "Labels"]].to_string(index=False))
