from pathlib import Path
import pandas as pd

root = Path(r"E:\movie chrome\WDSEventDB-main\WDSEventDB-main\WDSEventDB\WDSEventDB")
file = root / "Cyberattack" / "CyberEvent1-4.xlsx"
df = pd.read_excel(file)

features = df.drop(columns=["Labels"])
print("Cyberattack label counts:")
print(df["Labels"].value_counts().sort_index().to_string())

print("\nMean sensor values by label:")
print(df.groupby("Labels")[features.columns].mean().round(3).T.to_string())

print("\nSensor standard deviations by label:")
print(df.groupby("Labels")[features.columns].std().round(3).T.to_string())
