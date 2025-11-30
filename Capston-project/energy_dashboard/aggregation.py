# energy_dashboard/aggregation.py

from typing import Dict, Tuple

import pandas as pd


def prepare_time_index(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ensure the DataFrame uses a DateTimeIndex based on 'timestamp'.
    """
    df = df.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.dropna(subset=["timestamp"])
    df = df.set_index("timestamp")
    return df


def calculate_daily_totals(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate daily total kWh per building.

    Returns a DataFrame with date index and one row per building per day.
    """
    df = prepare_time_index(df)
    daily = df.groupby("building").resample("D")["kwh"].sum().reset_index()
    daily = daily.rename(columns={"kwh": "daily_kwh"})
    return daily


def calculate_weekly_aggregates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate weekly total kWh per building.

    Returns a DataFrame with week start date and one row per building per week.
    """
    df = prepare_time_index(df)
    weekly = df.groupby("building").resample("W")["kwh"].sum().reset_index()
    weekly = weekly.rename(columns={"kwh": "weekly_kwh"})
    return weekly


def building_wise_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute summary statistics (mean, min, max, total) for each building.

    Returns a DataFrame with one row per building.
    """
    grouped = df.groupby("building")["kwh"]

    summary = grouped.agg(
        total_kwh="sum",
        mean_kwh="mean",
        min_kwh="min",
        max_kwh="max",
        readings_count="count",
    ).reset_index()

    return summary


def campus_summary_numbers(df: pd.DataFrame, daily: pd.DataFrame) -> Tuple[float, str, pd.Timestamp]:
    """
    Helper to compute:
    - total campus consumption
    - highest consuming building
    - peak load time (timestamp with max kwh)
    """
    # Total campus consumption
    total_campus_kwh = df["kwh"].sum()

    # Highest consuming building
    building_totals = df.groupby("building")["kwh"].sum()
    highest_building = building_totals.idxmax()

    # Peak load time (timestamp at which kwh is maximum)
    peak_row = df.loc[df["kwh"].idxmax()]
    peak_time = peak_row["timestamp"]

    return total_campus_kwh, highest_building, peak_time
