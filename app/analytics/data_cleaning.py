from pathlib import Path
import pandas as pd


# Find project root directory
BASE_DIR = Path(__file__).resolve().parents[2]

# Raw and processed data folders
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"


def clean_column_names(df):
    """Make column names consistent."""

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("?", "", regex=False)
        .str.replace("/", "_")
        .str.replace("-", "_")
    )

    return df


def clean_dataset(file_path):
    """Read and perform basic safe cleaning on one dataset."""

    print("\n" + "=" * 60)
    print(f"CLEANING: {file_path.name}")
    print("=" * 60)

    try:

        # Read CSV files
        if file_path.suffix.lower() == ".csv":
            df = pd.read_csv(file_path)

        # Read Excel files
        elif file_path.suffix.lower() in [".xlsx", ".xls"]:
            df = pd.read_excel(file_path)

        else:
            print("Unsupported file type.")
            return

        original_rows = len(df)

        # Clean column names
        df = clean_column_names(df)

        # Remove completely empty rows
        df = df.dropna(how="all")

        # Remove duplicate rows
        df = df.drop_duplicates()

        # Remove leading/trailing spaces from text values
        for column in df.select_dtypes(include="object").columns:
            df[column] = df[column].astype(str).str.strip()

        # Replace empty strings with missing values
        df = df.replace("", pd.NA)

        # Create output filename
        output_name = file_path.stem + "_cleaned.csv"

        output_path = PROCESSED_DATA_DIR / output_name

        # Save cleaned dataset
        df.to_csv(output_path, index=False)

        # Print summary
        print(f"\nOriginal rows: {original_rows}")
        print(f"Cleaned rows: {len(df)}")
        print(f"Duplicates removed: {original_rows - len(df)}")
        print(f"Saved to: {output_path.name}")

    except Exception as error:
        print(f"\nError cleaning {file_path.name}:")
        print(error)


def main():

    # Create processed folder if it doesn't exist
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Find CSV and Excel files
    data_files = list(RAW_DATA_DIR.glob("*.csv"))
    data_files += list(RAW_DATA_DIR.glob("*.xlsx"))
    data_files += list(RAW_DATA_DIR.glob("*.xls"))

    if not data_files:
        print("No datasets found.")
        return

    print(f"Found {len(data_files)} datasets.")

    # Clean every dataset
    for file_path in data_files:
        clean_dataset(file_path)

    print("\n" + "=" * 60)
    print("DATA CLEANING COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()