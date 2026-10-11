import pandas as pd
from pathlib import Path

file = Path(r"E:\movie chrome\WDSEventDB-main\WDSEventDB-main\WDSEventDB\WDSEventDB\Cyberattack\CyberEvent1-4.xlsx")
df = pd.read_excel(file)

print("Unique values per sensor:")
for col in df.drop(columns=["Labels"]).columns:
    print(f"{col:20} {df[col].nunique()}")

print("\nMean sensor values by label:")
print(df.groupby("Labels").mean(numeric_only=True).round(4).T.to_string())

print("\nSensor standard deviations by label:")
print(df.groupby("Labels").std(numeric_only=True).round(4).T.to_string())
