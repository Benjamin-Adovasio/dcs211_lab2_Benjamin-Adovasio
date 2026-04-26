import pandas as pd
import matplotlib.pyplot as plt
from prettytable import PrettyTable

arc_data = pd.read_csv(
    "county_economic_status_2025.csv",
    skiprows=4,
    thousands=","
)

print(arc_data.head())
print(arc_data.columns)

# ✅ REMOVE EMPTY ROW
arc_data = arc_data.iloc[1:]

arc_data = arc_data.rename(columns={
    "FIPS": "fips",
    "State": "state",
    "County": "county",
    "Per Capita Market Income, 2022": "pci",
    "Poverty Rate, 2018-2022": "poverty_rate",
    "Three-Year Average Unemployment Rate, 2020-2022": "unemployment"
})

arc_data = arc_data[[
    "fips",
    "state",
    "county",
    "pci",
    "poverty_rate",
    "unemployment"
]]

arc_data["pci"] = pd.to_numeric(arc_data["pci"])
arc_data["poverty_rate"] = pd.to_numeric(arc_data["poverty_rate"])
arc_data["unemployment"] = pd.to_numeric(arc_data["unemployment"])

print("\nCLEANED DATA:")
print(arc_data.head())

print("\nDATA TYPES:")
print(arc_data.dtypes)