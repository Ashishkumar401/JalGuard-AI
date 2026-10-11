import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

file = Path(r"E:\movie chrome\WDSEventDB-main\WDSEventDB-main\WDSEventDB\WDSEventDB\Cyberattack\CyberEvent1-4.xlsx")
df = pd.read_excel(file)

X = df.drop(columns=["Labels"])
y = df["Labels"].astype(int)

cut = int(len(df) * 0.75)
X_train, X_test = X.iloc[:cut], X.iloc[cut:]
y_train, y_test = y.iloc[:cut], y.iloc[cut:]

print("Training labels:", y_train.value_counts().sort_index().to_dict())
print("Testing labels:", y_test.value_counts().sort_index().to_dict())

model = RandomForestClassifier(
    n_estimators=100,
    max_depth=16,
    class_weight="balanced",
    random_state=42,
    n_jobs=2
)
model.fit(X_train, y_train)
pred = model.predict(X_test)

print("\nConfusion matrix [label 0, label 1]:")
print(confusion_matrix(y_test, pred, labels=[0, 1]))
print("\nClassification report:")
print(classification_report(y_test, pred, labels=[0, 1], zero_division=0))
