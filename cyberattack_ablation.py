import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

file = Path(r"E:\movie chrome\WDSEventDB-main\WDSEventDB-main\WDSEventDB\WDSEventDB\Cyberattack\CyberEvent1-4.xlsx")
df = pd.read_excel(file)

X = df.drop(columns=["Labels"])
y = df["Labels"].astype(int)

remove_groups = {
    "All sensors": [],
    "Without Analog Valve 2": ["Analog Valve 2"],
    "Without pressure sensors": [
        "Pressure 1 Out", "Pressure 2 Out",
        "Pressure 3 In", "Pressure 4 In"
    ],
    "Without VFD sensors": [
        "VFD 1", "VFD 2", "VFD 3", "VFD 4-1", "VFD 4-2"
    ],
}

# Keep the same chronological split for every experiment.
cut = int(len(df) * 0.75)
for name, remove in remove_groups.items():
    features = X.drop(columns=remove)
    model = RandomForestClassifier(
        n_estimators=100, max_depth=16,
        class_weight="balanced", random_state=42, n_jobs=2
    )
    model.fit(features.iloc[:cut], y.iloc[:cut])
    pred = model.predict(features.iloc[cut:])
    print(f"\n--- {name} ---")
    print(classification_report(
        y.iloc[cut:], pred, labels=[0, 1], zero_division=0
    ))
