import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

file = Path(r"E:\movie chrome\WDSEventDB-main\WDSEventDB-main\WDSEventDB\WDSEventDB\Cyberattack\CyberEvent1-4.xlsx")
df = pd.read_excel(file)

X = df.drop(columns=["Labels", "Analog Valve 2"])
y = df["Labels"].astype(int)

cut = int(len(df) * 0.75)
model = RandomForestClassifier(
    n_estimators=100, max_depth=16,
    class_weight="balanced", random_state=42, n_jobs=2
)
model.fit(X.iloc[:cut], y.iloc[:cut])
pred = model.predict(X.iloc[cut:])

print("Without Analog Valve 2:")
print(classification_report(y.iloc[cut:], pred, labels=[0, 1], zero_division=0))
