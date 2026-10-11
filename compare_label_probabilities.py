exec(open("inspect_probabilities.py", encoding="utf-8-sig").read().split("for name in")[0])

for name in ["LeakEvent2.xlsx", "LeakEvent1.xlsx", "CyberEvent1-4.xlsx"]:
    item = frames[name]
    probs = model.predict_proba(item["X"])[:, pos_idx]

    print(f"\n--- {name} ---")
    for label in [0, 1]:
        p = probs[item["y"].to_numpy() == label]
        if len(p):
            print(
                f"Actual label {label}: n={len(p)}, "
                f"median={p.mean():.3f}, "
                f"p10={float(__import__('numpy').percentile(p, 10)):.3f}, "
                f"p90={float(__import__('numpy').percentile(p, 90)):.3f}"
            )
