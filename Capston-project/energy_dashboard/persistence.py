# energy_dashboard/persistence.py

from pathlib import Path
from typing import Tuple

import pandas as pd


def save_cleaned_data(df: pd.DataFrame, output_dir: str = "output") -> str:
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    output_path = Path(output_dir) / "cleaned_energy_data.csv"
    df.to_csv(output_path, index=False)
    return str(output_path)


def save_building_summary(summary_df: pd.DataFrame, output_dir: str = "output") -> str:
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    output_path = Path(output_dir) / "building_summary.csv"
    summary_df.to_csv(output_path, index=False)
    return str(output_path)


def save_text_summary(
    output_dir: str,
    total_campus_kwh: float,
    highest_building: str,
    peak_time,
    daily_trend_comment: str,
    weekly_trend_comment: str,
) -> str:
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    output_path = Path(output_dir) / "summary.txt"

    lines = [
        "Campus Energy Consumption Summary\n",
        "---------------------------------\n\n",
        f"Total campus consumption: {total_campus_kwh:.2f} kWh\n",
        f"Highest-consuming building: {highest_building}\n",
        f"Peak load time (max single reading): {peak_time}\n\n",
        "Daily Trend Insights:\n",
        f"{daily_trend_comment}\n\n",
        "Weekly Trend Insights:\n",
        f"{weekly_trend_comment}\n",
    ]

    with open(output_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

    return str(output_path)
