# energy_dashboard/ingestion.py

import os
from pathlib import Path
from typing import Tuple, List

import pandas as pd


def load_energy_data(data_dir: str = "data") -> Tuple[pd.DataFrame, List[str]]:
    """
    Read all CSV files from a directory and combine them into a single DataFrame.

    Assumes each CSV has at least:
    - 'timestamp' column (date/time of reading)
    - 'kwh' column (energy consumption)

    If 'building' is missing, it is inferred from filename.
    If 'month' is missing, it is inferred from timestamp.

    Returns:
        df_combined: merged DataFrame of all buildings.
        error_logs: list of error messages for missing / corrupt files.
    """
    data_path = Path(data_dir)
    if not data_path.exists():
        raise FileNotFoundError(f"Data directory not found: {data_dir}")

    csv_files = [f for f in data_path.iterdir() if f.suffix.lower() == ".csv"]

    all_dfs = []
    error_logs = []

    for csv_file in csv_files:
        try:
            # Try reading CSV; skip bad lines instead of failing.
            df = pd.read_csv(csv_file, on_bad_lines="skip")

            # Ensure required columns exist
            if "kwh" not in df.columns:
                error_logs.append(f"File {csv_file.name} missing 'kwh' column. Skipped.")
                continue

            # Handle timestamp
            if "timestamp" not in df.columns:
                error_logs.append(f"File {csv_file.name} missing 'timestamp' column. Skipped.")
                continue

            df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
            df = df.dropna(subset=["timestamp"])

            # If building column missing → infer from filename (e.g. 'library_jan.csv' → 'library')
            if "building" not in df.columns:
                building_name = csv_file.stem   # filename without extension
                df["building"] = building_name

            # If month column missing → infer from timestamp
            if "month" not in df.columns:
                df["month"] = df["timestamp"].dt.to_period("M").astype(str)

            all_dfs.append(df)

        except FileNotFoundError:
            error_logs.append(f"File not found: {csv_file}")
        except pd.errors.EmptyDataError:
            error_logs.append(f"Empty or invalid CSV file: {csv_file}")
        except Exception as e:
            error_logs.append(f"Error reading {csv_file.name}: {e}")

    if not all_dfs:
        raise ValueError("No valid CSV files were loaded from the data directory.")

    df_combined = pd.concat(all_dfs, ignore_index=True)

    # Sort by time for convenience
    df_combined = df_combined.sort_values(by="timestamp")

    return df_combined, error_logs
