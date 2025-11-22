"""
Weather Data Visualizer - Lab Assignment 4
-----------------------------------------
Uses: weather_dataset.csv (must be in same folder)

Tasks covered:
- Task 1: Load CSV and inspect structure
- Task 2: Clean data (dates, NaN, filter columns)
- Task 3: Statistics (daily/monthly/yearly, NumPy-style metrics)
- Task 4: Matplotlib plots and combined figure
- Task 5: Grouping by month and season
- Task 6: Export cleaned CSV + produce plots for report
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# ---------------- CONFIG ----------------

DATA_PATH = Path("weather_dataset.csv")
CLEANED_DATA_PATH = Path("cleaned_weather_dataset.csv")
PLOTS_DIR = Path("plots")
PLOTS_DIR.mkdir(exist_ok=True)


# ------------- Helper: find columns ------------- #

def detect_column(df: pd.DataFrame, candidates):
    """
    Try to find a column whose name matches one of 'candidates' (case-insensitive).
    Raise an error with available columns if none found.
    """
    lower_cols = {c.lower(): c for c in df.columns}
    for name in candidates:
        if name.lower() in lower_cols:
            return lower_cols[name.lower()]
    raise ValueError(
        f"None of {candidates} found in dataset. "
        f"Available columns: {list(df.columns)}"
    )


# ---------------- Task 1: Load data ---------------- #

def load_data(path: Path) -> pd.DataFrame:
    print(f"\n[Task 1] Loading data from {path} ...")
    df = pd.read_csv(path)

    print("\n--- HEAD ---")
    print(df.head())

    print("\n--- INFO ---")
    print(df.info())

    print("\n--- DESCRIBE (numeric) ---")
    print(df.describe())

    return df


# ---------------- Task 2: Clean data ---------------- #

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    - Detect date, temperature, rainfall, humidity columns.
    - Convert date to datetime.
    - Handle NaNs (fill numeric cols with mean).
    - Keep only needed columns.
    """
    print("\n[Task 2] Cleaning data...")

    # ⚠️ If your column names differ, add them to these candidate lists
    date_col = detect_column(df, ["date", "Date", "DATE"])
    temp_col = detect_column(df, ["temperature", "Temperature", "temp", "Temp", "TAVG", "TMAX", "TMIN"])
    rain_col = detect_column(df, ["rainfall", "Rainfall", "rain", "Rain", "precipitation", "PRCP"])
    hum_col = detect_column(df, ["humidity", "Humidity", "RH", "RelHumidity"])

    # Keep only needed columns
    df = df[[date_col, temp_col, rain_col, hum_col]].copy()
    df.columns = ["date", "temperature", "rainfall", "humidity"]

    # Convert date column
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])

    # Fill numeric NaNs with column mean
    for col in ["temperature", "rainfall", "humidity"]:
        if df[col].isna().any():
            mean_val = df[col].mean()
            print(f"Filling NaN in {col} with mean {mean_val:.2f}")
            df[col] = df[col].fillna(mean_val)

    # Sort by date
    df = df.sort_values("date").reset_index(drop=True)

    print("\n--- CLEANED DATA PREVIEW ---")
    print(df.head())

    return df


# ---------------- Task 3: Statistics ---------------- #

def compute_statistics(df: pd.DataFrame):
    """
    Compute:
    - Overall daily stats (mean, min, max, std)
    - Monthly stats via resample('M')
    - Yearly stats via resample('Y')
    """
    print("\n[Task 3] Computing statistics...")

    df = df.set_index("date")

    daily_stats = df[["temperature", "rainfall", "humidity"]].agg(
        ["mean", "min", "max", "std"]
    )
    print("\n--- OVERALL STATS ---")
    print(daily_stats)

    monthly_stats = df.resample("M").agg(
        {
            "temperature": ["mean", "min", "max", "std"],
            "rainfall": ["sum", "mean"],
            "humidity": ["mean", "min", "max"],
        }
    )
    print("\n--- MONTHLY STATS (first 5 rows) ---")
    print(monthly_stats.head())

    yearly_stats = df.resample("Y").agg(
        {
            "temperature": ["mean", "min", "max", "std"],
            "rainfall": ["sum", "mean"],
            "humidity": ["mean", "min", "max"],
        }
    )
    print("\n--- YEARLY STATS ---")
    print(yearly_stats)

    return df.reset_index(), daily_stats, monthly_stats, yearly_stats


# ---------------- Task 4: Visualizations ---------------- #

def plot_daily_temperature(df: pd.DataFrame):
    plt.figure(figsize=(10, 5))
    plt.plot(df["date"], df["temperature"])
    plt.title("Daily Temperature Trend")
    plt.xlabel("Date")
    plt.ylabel("Temperature")
    plt.grid(True)
    plt.tight_layout()
    out = PLOTS_DIR / "daily_temperature_trend.png"
    plt.savefig(out)
    plt.close()
    print(f"Saved plot: {out}")


def plot_monthly_rainfall(df: pd.DataFrame):
    monthly_rain = (
        df.set_index("date")["rainfall"]
          .resample("M")
          .sum()
    )
    plt.figure(figsize=(10, 5))
    plt.bar(monthly_rain.index.strftime("%Y-%m"), monthly_rain.values)
    plt.xticks(rotation=45, ha="right")
    plt.title("Monthly Rainfall Totals")
    plt.xlabel("Month")
    plt.ylabel("Total Rainfall")
    plt.tight_layout()
    out = PLOTS_DIR / "monthly_rainfall_bar.png"
    plt.savefig(out)
    plt.close()
    print(f"Saved plot: {out}")


def plot_humidity_vs_temperature(df: pd.DataFrame):
    plt.figure(figsize=(7, 5))
    plt.scatter(df["temperature"], df["humidity"], alpha=0.6)
    plt.title("Humidity vs Temperature")
    plt.xlabel("Temperature")
    plt.ylabel("Humidity")
    plt.grid(True)
    plt.tight_layout()
    out = PLOTS_DIR / "humidity_vs_temperature_scatter.png"
    plt.savefig(out)
    plt.close()
    print(f"Saved plot: {out}")


def plot_combined(df: pd.DataFrame):
    df = df.set_index("date")

    fig, axes = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    axes[0].plot(df.index, df["temperature"])
    axes[0].set_title("Daily Temperature")
    axes[0].set_ylabel("Temperature")
    axes[0].grid(True)

    axes[1].bar(df.index, df["rainfall"])
    axes[1].set_title("Daily Rainfall")
    axes[1].set_xlabel("Date")
    axes[1].set_ylabel("Rainfall")
    axes[1].grid(True)

    fig.suptitle("Combined Weather Plots", fontsize=14)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])

    out = PLOTS_DIR / "combined_temperature_rainfall.png"
    plt.savefig(out)
    plt.close()
    print(f"Saved plot: {out}")

    return df.reset_index()


# ---------------- Task 5: Grouping & Aggregation ---------------- #

def month_to_season(m: int) -> str:
    # Simple mapping – you can adjust to your local climate
    if m in (12, 1, 2):
        return "Winter"
    elif m in (3, 4, 5):
        return "Summer"
    elif m in (6, 7, 8, 9):
        return "Monsoon"
    else:
        return "Post-Monsoon"


def grouping_and_aggregation(df: pd.DataFrame):
    print("\n[Task 5] Grouping and aggregation...")

    df["month"] = df["date"].dt.month
    df["year"] = df["date"].dt.year
    df["season"] = df["month"].apply(month_to_season)

    by_month = df.groupby("month").agg(
        avg_temp=("temperature", "mean"),
        total_rain=("rainfall", "sum"),
        avg_humidity=("humidity", "mean"),
    )
    print("\n--- GROUPED BY MONTH ---")
    print(by_month)

    by_season = df.groupby("season").agg(
        avg_temp=("temperature", "mean"),
        total_rain=("rainfall", "sum"),
        avg_humidity=("humidity", "mean"),
    )
    print("\n--- GROUPED BY SEASON ---")
    print(by_season)

    return by_month, by_season


# ---------------- Task 6: Export ---------------- #

def export_cleaned_data(df: pd.DataFrame):
    df.to_csv(CLEANED_DATA_PATH, index=False)
    print(f"\n[Task 6] Cleaned data exported to {CLEANED_DATA_PATH}")


# ---------------- Main ---------------- #

def main():
    df = load_data(DATA_PATH)
    df = clean_data(df)
    df, daily_stats, monthly_stats, yearly_stats = compute_statistics(df)

    # Plots
    plot_daily_temperature(df)
    plot_monthly_rainfall(df)
    plot_humidity_vs_temperature(df)
    df = plot_combined(df)

    # Grouping
    by_month, by_season = grouping_and_aggregation(df)

    # Export
    export_cleaned_data(df)

    print("\nAll tasks completed. Check:")
    print(" - cleaned_weather_dataset.csv")
    print(" - plots/ folder")
    print("Use these plus the printed stats for your Markdown/text report.")


if __name__ == "__main__":
    main()
