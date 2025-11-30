# Campus Energy Dashboard – Moin Khan

This project is a capstone assignment for **Programming for Problem Solving using Python**.  
It analyses campus electricity usage from multiple buildings and presents insights through
aggregations and visualizations.

## Objectives

- Read and validate multiple CSV files with monthly electricity data.
- Use Pandas to combine and clean the data.
- Compute daily and weekly energy consumption.
- Design object-oriented models (`Building`, `MeterReading`, `BuildingManager`).
- Build a multi-chart dashboard using Matplotlib.
- Export cleaned datasets, building-wise summaries, and an executive text summary.

## Project Structure

```text
project/
├─ data/                     # Raw CSV files (input)
├─ output/                   # Cleaned CSVs, summary.txt, dashboard.png
├─ energy_dashboard/         # Python package with modules
│  ├─ ingestion.py
│  ├─ aggregation.py
│  ├─ models.py
│  ├─ visualization.py
│  └─ persistence.py
├─ main.py                   # Orchestrates all tasks
├─ requirements.txt
└─ README.md
