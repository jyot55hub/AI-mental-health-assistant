from pathlib import Path
import pandas as pd


# ============================================================
# PATH SETUP
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"


# ============================================================
# LOAD DATASET
# ============================================================

def load_dataset(file_path):
    """
    Load a CSV dataset safely.
    """

    try:
        df = pd.read_csv(file_path)

        print("\n" + "=" * 70)
        print(f"ANALYZING: {file_path.name}")
        print("=" * 70)

        return df

    except Exception as error:
        print(f"\nError loading {file_path.name}: {error}")
        return None


# ============================================================
# BASIC DATA ANALYSIS
# ============================================================

def basic_analysis(df):
    """
    Perform basic statistical analysis.
    """

    print("\nBASIC DATASET INFORMATION")
    print("-" * 70)

    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")


    # --------------------------------------------------------
    # NUMERICAL SUMMARY
    # --------------------------------------------------------

    numeric_columns = df.select_dtypes(include="number")

    if not numeric_columns.empty:

        print("\nNUMERICAL SUMMARY:")

        print(numeric_columns.describe())


    # --------------------------------------------------------
    # CATEGORICAL SUMMARY
    # --------------------------------------------------------

    categorical_columns = df.select_dtypes(
        include=["object", "string"]
    )

    if not categorical_columns.empty:

        print("\nCATEGORICAL VALUE COUNTS:")

        for column in categorical_columns.columns:

            print("\n" + "-" * 50)

            print(f"COLUMN: {column}")

            print("-" * 50)

            print(
                df[column]
                .value_counts()
                .head(10)
            )


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():

    print("\n" + "=" * 70)

    print("MENTAL HEALTH DATA ANALYSIS")

    print("=" * 70)


    # Find cleaned datasets

    csv_files = list(
        PROCESSED_DATA_DIR.glob("*_cleaned.csv")
    )


    if not csv_files:

        print("\nNo cleaned datasets found.")

        return


    print(
        f"\nFound {len(csv_files)} cleaned datasets."
    )


    # Analyze each dataset

    for file_path in csv_files:

        df = load_dataset(file_path)

        if df is not None:

            basic_analysis(df)


    print("\n" + "=" * 70)

    print("DATA ANALYSIS COMPLETED")

    print("=" * 70)


# ============================================================
# RUN PROGRAM
# ============================================================

if __name__ == "__main__":

    main()