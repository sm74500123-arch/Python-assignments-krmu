# main.py

from pathlib import Path

import pandas as pd

from energy_dashboard.ingestion import load_energy_data
from energy_dashboard.aggregation import (
    calculate_daily_totals,
    calculate_weekly_aggregates,
    building_wise_summary,
    campus_summary_numbers,
)
from energy_dashboard.models import BuildingManager
from energy_dashboard.visualization import create_dashboard
from energy_dashboard.persistence import (
    save_cleaned_data,
    save_building_summary,
    save_text_summary,
)


def generate_trend_comments(daily_df: pd.DataFrame, weekly_df: pd.DataFrame) -> tuple[str, str]:
    """
    Create simple human-readable comments about daily and weekly trends.
    (You can make this fancier later if you want.)
    """
    # Daily trend comment
    daily_total_by_date = daily_df.groupby("timestamp")["daily_kwh"].sum().reset_index()

    if len(daily_total_by_date) >= 2:
        first = daily_total_by_date.iloc[0]["daily_kwh"]
        last = daily_total_by_date.iloc[-1]["daily_kwh"]
        if last > first:
            daily_comment = "Overall daily consumption shows an increasing trend over time."
        elif last < first:
            daily_comment = "Overall daily consumption shows a decreasing trend over time."
        else:
            daily_comment = "Overall daily consumption remains relatively stable."
    else:
        daily_comment = "Not enough data to determine daily trends."

    # Weekly trend comment
    weekly_total_by_week = weekly_df.groupby("timestamp")["weekly_kwh"].sum().reset_index()
    if len(weekly_total_by_week) >= 2:
        first_w = weekly_total_by_week.iloc[0]["weekly_kwh"]
        last_w = weekly_total_by_week.iloc[-1]["weekly_kwh"]
        if last_w > first_w:
            weekly_comment = "Weekly consumption is trending upwards."
        elif last_w < first_w:
            weekly_comment = "Weekly consumption is trending downwards."
        else:
            weekly_comment = "Weekly consumption appears stable."
    else:
        weekly_comment = "Not enough data to determine weekly trends."

    return daily_comment, weekly_comment


def main():
    print("=== Campus Energy Dashboard ===")

    # ---------- Task 1: Data Ingestion ----------
    print("[1/5] Loading data from 'data/' folder...")
    df_raw, error_logs = load_energy_data("data")

    if error_logs:
        print("Some issues were found while loading data:")
        for err in error_logs:
            print("  -", err)
    else:
        print("All CSV files loaded successfully.")

    # Keep a copy of cleaned data (ensuring timestamp is parsed)
    df_raw["timestamp"] = pd.to_datetime(df_raw["timestamp"], errors="coerce")
    df_clean = df_raw.dropna(subset=["timestamp", "kwh", "building"])

    # ---------- Task 2: Aggregations ----------
    print("[2/5] Calculating daily and weekly aggregates, and building summary...")
    daily_totals = calculate_daily_totals(df_clean)
    weekly_aggregates = calculate_weekly_aggregates(df_clean)
    building_summary_df = building_wise_summary(df_clean)

    # ---------- Task 3: Object-Oriented Modeling ----------
    print("[3/5] Creating Building and MeterReading objects...")
    manager = BuildingManager()
    manager.load_from_dataframe(df_clean)
    building_reports = manager.generate_all_reports()

    print("  OOP reports (sample):")
    for report in building_reports[:3]:
        print("   >", report)

    # ---------- Campus-level numbers for summary ----------
    total_campus_kwh, highest_building, peak_time = campus_summary_numbers(df_clean, daily_totals)

    # ---------- Task 4: Visualization ----------
    print("[4/5] Creating dashboard visualization...")
    output_dir = "output"
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    dashboard_path = str(Path(output_dir) / "dashboard.png")

    create_dashboard(
        daily_df=daily_totals,
        weekly_df=weekly_aggregates,
        building_summary=building_summary_df,
        output_path=dashboard_path,
    )

    print(f"  Dashboard saved as: {dashboard_path}")

    # ---------- Task 5: Persistence & Summary ----------
    print("[5/5] Saving cleaned data, summary CSV, and text report...")

    cleaned_path = save_cleaned_data(df_clean, output_dir=output_dir)
    summary_csv_path = save_building_summary(building_summary_df, output_dir=output_dir)

    daily_comment, weekly_comment = generate_trend_comments(daily_totals, weekly_aggregates)

    summary_txt_path = save_text_summary(
        output_dir=output_dir,
        total_campus_kwh=total_campus_kwh,
        highest_building=highest_building,
        peak_time=peak_time,
        daily_trend_comment=daily_comment,
        weekly_trend_comment=weekly_comment,
    )

    print(f"  Cleaned data saved to: {cleaned_path}")
    print(f"  Building summary saved to: {summary_csv_path}")
    print(f"  Text summary saved to: {summary_txt_path}")

    print("\nAll tasks completed successfully!")


if __name__ == "__main__":
    main()
