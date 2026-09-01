from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# PATH SETUP
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"
OUTPUT_DIR = BASE_DIR / "data" / "visualizations"

OUTPUT_DIR.mkdir(exist_ok=True)


# ============================================================
# HELPER FUNCTION
# ============================================================

def save_plot(filename):
    """
    Save the current chart and close it.
    """

    output_path = OUTPUT_DIR / filename

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"Saved chart: {filename}")


# ============================================================
# STRESS LEVEL DISTRIBUTION
# ============================================================

def plot_stress_distribution(df, dataset_name):

    if "stress_level" not in df.columns:
        return

    counts = df["stress_level"].value_counts()

    plt.figure(figsize=(8, 5))

    plt.bar(counts.index.astype(str), counts.values)

    plt.title(f"Stress Level Distribution\n{dataset_name}")

    plt.xlabel("Stress Level")
    plt.ylabel("Number of Students")

    save_plot(
        f"{dataset_name}_stress_distribution.png"
    )


# ============================================================
# SLEEP HOURS DISTRIBUTION
# ============================================================

def plot_sleep_distribution(df, dataset_name):

    if "sleep_hours" not in df.columns:
        return

    plt.figure(figsize=(8, 5))

    plt.hist(
        df["sleep_hours"].dropna(),
        bins=10
    )

    plt.title(f"Sleep Hours Distribution\n{dataset_name}")

    plt.xlabel("Sleep Hours")
    plt.ylabel("Number of Students")

    save_plot(
        f"{dataset_name}_sleep_distribution.png"
    )


# ============================================================
# STRESS VS SLEEP
# ============================================================

def plot_stress_vs_sleep(df, dataset_name):

    if (
        "stress_level" not in df.columns
        or "sleep_hours" not in df.columns
    ):
        return

    stress_mapping = {
        "Low": 1,
        "Medium": 2,
        "High": 3
    }

    stress_values = (
        df["stress_level"]
        .astype(str)
        .map(stress_mapping)
    )

    plt.figure(figsize=(8, 5))

    plt.scatter(
        df["sleep_hours"],
        stress_values
    )

    plt.title(f"Stress Level vs Sleep Hours\n{dataset_name}")

    plt.xlabel("Sleep Hours")

    plt.ylabel("Stress Level")

    plt.yticks(
        [1, 2, 3],
        ["Low", "Medium", "High"]
    )

    save_plot(
        f"{dataset_name}_stress_vs_sleep.png"
    )


# ============================================================
# ANXIETY SCORE DISTRIBUTION
# ============================================================

def plot_anxiety_distribution(df, dataset_name):

    if "anxiety_score" not in df.columns:
        return

    plt.figure(figsize=(8, 5))

    plt.hist(
        df["anxiety_score"].dropna(),
        bins=10
    )

    plt.title(f"Anxiety Score Distribution\n{dataset_name}")

    plt.xlabel("Anxiety Score")

    plt.ylabel("Number of Students")

    save_plot(
        f"{dataset_name}_anxiety_distribution.png"
    )


# ============================================================
# BURNOUT LEVEL DISTRIBUTION
# ============================================================

def plot_burnout_distribution(df, dataset_name):

    if "burnout_level" not in df.columns:
        return

    counts = df["burnout_level"].value_counts()

    plt.figure(figsize=(8, 5))

    plt.bar(
        counts.index.astype(str),
        counts.values
    )

    plt.title(f"Burnout Level Distribution\n{dataset_name}")

    plt.xlabel("Burnout Level")

    plt.ylabel("Number of Students")

    save_plot(
        f"{dataset_name}_burnout_distribution.png"
    )


# ============================================================
# VISUALIZE DATASET
# ============================================================

def visualize_dataset(file_path):

    print("\n" + "=" * 60)

    print(f"VISUALIZING: {file_path.name}")

    print("=" * 60)

    try:

        df = pd.read_csv(file_path)

        dataset_name = file_path.stem

        plot_stress_distribution(
            df,
            dataset_name
        )

        plot_sleep_distribution(
            df,
            dataset_name
        )

        plot_stress_vs_sleep(
            df,
            dataset_name
        )

        plot_anxiety_distribution(
            df,
            dataset_name
        )

        plot_burnout_distribution(
            df,
            dataset_name
        )

    except Exception as error:

        print(
            f"Error visualizing "
            f"{file_path.name}: {error}"
        )


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():

    print("\n" + "=" * 60)

    print("MENTAL HEALTH DATA VISUALIZATION")

    print("=" * 60)


    csv_files = list(
        PROCESSED_DATA_DIR.glob("*_cleaned.csv")
    )


    print(
        f"\nFound {len(csv_files)} cleaned datasets."
    )


    for file_path in csv_files:

        visualize_dataset(file_path)


    print("\n" + "=" * 60)

    print("DATA VISUALIZATION COMPLETED")

    print("=" * 60)


# ============================================================
# RUN PROGRAM
# ============================================================

if __name__ == "__main__":

    main()