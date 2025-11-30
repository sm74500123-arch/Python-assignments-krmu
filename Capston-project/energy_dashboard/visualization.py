# energy_dashboard/visualization.py

from typing import Optional

import pandas as pd
import matplotlib.pyplot as plt


def create_dashboard(
    daily_df: pd.DataFrame,
    weekly_df: pd.DataFrame,
    building_summary: pd.DataFrame,
    output_path: str = "output/dashboard.png",
) -> None:
    """
    Create a multi-chart dashboard:
    - Line chart: daily consumption over time for all buildings
    - Bar chart: average weekly usage per building
    - Scatter plot: peak (max) daily usage per building

    Saves the figure as dashboard.png.
    """
    # Ensure required columns exist
    required_daily = {"timestamp", "building", "daily_kwh"}
    required_weekly = {"timestamp", "building", "weekly_kwh"}

    if not required_daily.issubset(daily_df.columns):
        raise ValueError(f"daily_df must contain columns: {required_daily}")
    if not required_weekly.issubset(weekly_df.columns):
        raise ValueError(f"weekly_df must contain columns: {required_weekly}")

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # 1. Line chart - daily consumption over time for all buildings
    ax1 = axes[0]
    for building, group in daily_df.groupby("building"):
        ax1.plot(group["timestamp"], group["daily_kwh"], label=building)
    ax1.set_title("Daily Consumption Over Time")
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Daily kWh")
    ax1.tick_params(axis="x", rotation=45)
    ax1.legend(fontsize=8)

    # 2. Bar chart - average weekly usage per building
    ax2 = axes[1]
    weekly_mean = weekly_df.groupby("building")["weekly_kwh"].mean().reset_index()
    ax2.bar(weekly_mean["building"], weekly_mean["weekly_kwh"])
    ax2.set_title("Average Weekly Usage by Building")
    ax2.set_xlabel("Building")
    ax2.set_ylabel("Average Weekly kWh")
    ax2.tick_params(axis="x", rotation=45)

    # 3. Scatter plot - peak daily consumption per building
    ax3 = axes[2]
    peak_daily = daily_df.groupby("building")["daily_kwh"].max().reset_index()
    ax3.scatter(peak_daily["building"], peak_daily["daily_kwh"])
    ax3.set_title("Peak Daily Consumption by Building")
    ax3.set_xlabel("Building")
    ax3.set_ylabel("Peak Daily kWh")
    ax3.tick_params(axis="x", rotation=45)

    fig.tight_layout()
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)
