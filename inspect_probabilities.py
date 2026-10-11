exec(open("corrected_evaluation.py", encoding="utf-8-sig").read().split("# Select threshold on validation file only.")[0])

import numpy as np

for name in ["LeakEvent2.xlsx", "LeakEvent1.xlsx", "CyberEvent1-4.xlsx"]:
    item = frames[name]
    probs = model.predict_proba(item["X"])[:, pos_idx]

    print(f"\n{name}")
    print("Actual labels:", item["y"].value_counts().sort_index().to_dict())
    print("Probability min / median / max:",
          round(float(probs.min()), 4),
          round(float(np.median(probs)), 4),
          round(float(probs.max()), 4))

    for t in [0.05, 0.10, 0.20, 0.30, 0.50]:
        print(f"Threshold {t:.2f}: {(probs >= t).sum()} predicted events")
