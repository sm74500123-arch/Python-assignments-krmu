# energy_dashboard/models.py

from dataclasses import dataclass
from typing import List, Dict

import pandas as pd


@dataclass
class MeterReading:
    timestamp: pd.Timestamp
    kwh: float


class Building:
    def __init__(self, name: str):
        self.name = name
        self.meter_readings: List[MeterReading] = []

    def add_reading(self, reading: MeterReading) -> None:
        self.meter_readings.append(reading)

    def calculate_total_consumption(self) -> float:
        return sum(r.kwh for r in self.meter_readings)

    def calculate_peak_load(self) -> MeterReading | None:
        if not self.meter_readings:
            return None
        return max(self.meter_readings, key=lambda r: r.kwh)

    def generate_report(self) -> Dict[str, float | str]:
        """
        Returns a small dictionary summarizing this building.
        """
        total = self.calculate_total_consumption()
        peak = self.calculate_peak_load()

        report = {
            "building": self.name,
            "total_kwh": total,
            "peak_kwh": peak.kwh if peak else 0.0,
            "peak_time": str(peak.timestamp) if peak else "N/A",
            "readings_count": len(self.meter_readings),
        }
        return report


class BuildingManager:
    def __init__(self):
        self.buildings: Dict[str, Building] = {}

    def get_or_create_building(self, name: str) -> Building:
        if name not in self.buildings:
            self.buildings[name] = Building(name)
        return self.buildings[name]

    def load_from_dataframe(self, df: pd.DataFrame) -> None:
        """
        Convert rows from raw DataFrame into Building and MeterReading objects.

        Expects 'building', 'timestamp', 'kwh' columns.
        """
        for _, row in df.iterrows():
            building_name = row["building"]
            timestamp = pd.to_datetime(row["timestamp"])
            kwh = float(row["kwh"])

            building = self.get_or_create_building(building_name)
            building.add_reading(MeterReading(timestamp, kwh))

    def generate_all_reports(self) -> List[Dict[str, float | str]]:
        """
        Generate a report for each building.
        """
        return [b.generate_report() for b in self.buildings.values()]
