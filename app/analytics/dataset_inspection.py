from pathlib import Path
import pandas as pd


# Project root folder
BASE_DIR = Path(__file__).resolve().parents[2]

# Dataset folder
DATA_DIR = BASE_DIR / "data" / "raw"


def inspect_dataset(file_path):
    """Print a short and useful summary of one dataset."""

    print("\n" + "=" * 60)
    print(f"DATASET: {file_path.name}")
    print("=" * 60)

    try:
        # Read CSV file
        df = pd.read_csv(file_path)

        # Basic information
        print(f"\nRows: {df.shape[0]}")
        print(f"Columns: {df.shape[1]}")

        # Column names
        print("\nCOLUMN NAMES:")

        for column in df.columns:
            print(f"- {column}")

        # Missing values summary
        total_missing = df.isnull().sum().sum()

        print(f"\nTOTAL MISSING VALUES: {total_missing}")

        # Duplicate rows
        duplicate_rows = df.duplicated().sum()

        print(f"DUPLICATE ROWS: {duplicate_rows}")

        # Data types summary
        print("\nDATA TYPES:")

        print(df.dtypes.value_counts())

        # First 3 rows only
        print("\nFIRST 3 ROWS:")

        print(df.head(3))

    except Exception as error:
        print(f"\nError reading {file_path.name}:")
        print(error)


def main():

    # Find all CSV files
    csv_files = list(DATA_DIR.glob("*.csv"))

    if not csv_files:
        print("No CSV files found.")
        return

    print(f"Found {len(csv_files)} CSV files.")

    # Inspect every CSV dataset
    for file_path in csv_files:
        inspect_dataset(file_path)


if __name__ == "__main__":
    main()