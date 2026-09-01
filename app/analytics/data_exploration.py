from pathlib import Path
import pandas as pd


# -------------------------------------------------
# PATHS
# -------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"


# -------------------------------------------------
# EXPLORE DATASET
# -------------------------------------------------

def explore_dataset(file_path):
    print("\n" + "=" * 60)
    print(f"EXPLORING: {file_path.name}")
    print("=" * 60)

    try:
        # Read CSV file
        df = pd.read_csv(file_path)

        print(f"\nRows: {df.shape[0]}")
        print(f"Columns: {df.shape[1]}")

        print("\nCOLUMN NAMES:")
        for column in df.columns:
            print(f"- {column}")

        print("\nDATA TYPES:")
        print(df.dtypes)

        print("\nMISSING VALUES:")
        missing = df.isnull().sum()
        missing = missing[missing > 0]

        if missing.empty:
            print("No missing values.")
        else:
            print(missing)

        print("\nFIRST 3 ROWS:")
        print(df.head(3))

    except Exception as e:
        print(f"\nError exploring {file_path.name}:")
        print(e)


# -------------------------------------------------
# MAIN
# -------------------------------------------------

def main():
    print("\n" + "=" * 60)
    print("DATA EXPLORATION")
    print("=" * 60)

    csv_files = list(PROCESSED_DATA_DIR.glob("*.csv"))

    if not csv_files:
        print("\nNo cleaned CSV files found.")
        return

    print(f"\nFound {len(csv_files)} cleaned datasets.")

    for file_path in csv_files:
        explore_dataset(file_path)

    print("\n" + "=" * 60)
    print("DATA EXPLORATION COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()