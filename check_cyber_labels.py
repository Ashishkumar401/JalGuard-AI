import pandas as pd
from pathlib import Path

file = Path(r"E:\movie chrome\WDSEventDB-main\WDSEventDB-main\WDSEventDB\WDSEventDB\Cyberattack\CyberEvent1-4.xlsx")
df = pd.read_excel(file)

features = df.drop(columns=["Labels"])
y = df["Labels"].astype(int)

print("Rows:", len(df))
print("Label counts:", y.value_counts().sort_index().to_dict())
print("Label transitions:", int(y.ne(y.shift()).sum() - 1))

duplicate_features = features.duplicated(keep=False)
print("Rows with duplicated sensor readings:", int(duplicate_features.sum()))

both_labels = (
    df.assign(_feature_key=features.astype(str).agg("|".join, axis=1))
      .groupby("_feature_key")["Labels"].nunique()
)
print("Identical sensor readings found with both labels:", int((both_labels > 1).sum()))

print("\nFirst 10 label transitions (row index and label):")
transition_idx = y.index[y.ne(y.shift())].tolist()
for i in transition_idx[:10]:
    print(i, int(y.iloc[i]))
