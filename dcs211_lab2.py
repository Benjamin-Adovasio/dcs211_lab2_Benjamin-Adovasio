import pandas as pd
import matplotlib.pyplot as plt
from prettytable import PrettyTable

arc_data = pd.read_csv(
    "county_economic_status_2025.csv",
    thousands=","
)

print(arc_data.head())
print(arc_data.columns)