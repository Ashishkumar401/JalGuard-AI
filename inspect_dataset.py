from pathlib import Path
import pandas as pd

root = Path(r"E:\movie chrome\WDSEventDB-main\WDSEventDB-main\WDSEventDB\WDSEventDB")

for file in sorted(root.rglob("*.xlsx")):
    if "__MACOSX" in str(file):
        continue

    print("\n" + "=" * 65)
    print("CATEGORY:", file.parent.name)
    print("FILE:", file.name)

    try:
        excel = pd.ExcelFile(file)
        for sheet in excel.sheet_names:
            df = pd.read_excel(file, sheet_name=sheet)
            print(f"\nSheet: {sheet} | Rows: {len(df)} | Columns: {len(df.columns)}")
            print("Column names:", df.columns.tolist())

            for col in df.columns:
                if "label" in str(col).lower():
                    print(f"Label counts for '{col}':")
                    print(df[col].value_counts(dropna=False).to_dict())

    except Exception as e:
        print("Could not read file:", e)
