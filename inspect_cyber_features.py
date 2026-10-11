import pandas as pd
from pathlib import Path

file = Path(r"E:\movie chrome\WDSEventDB-main\WDSEventDB-main\WDSEventDB\WDSEventDB\Cyberattack\CyberEvent1-4.xlsx")
df = pd.read_excel(file)

features = df.drop(columns=["Labels"])
summary = features.groupby(df["Labels"]).agg(["mean", "std"])

for col in features.columns:
    m0 = summary.loc[0, (col, "mean")]
    m1 = summary.loc[1, (col, "mean")]
    s0 = summary.loc[0, (col, "std")]
    s1 = summary.loc[1, (col, "std")]
    print(f"{col:20} | label0 mean={m0:10.4f} std={s0:10.4f} | label1 mean={m1:10.4f} std={s1:10.4f}")
