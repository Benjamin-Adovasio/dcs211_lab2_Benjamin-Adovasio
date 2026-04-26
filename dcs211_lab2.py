import pandas as pd
import matplotlib.pyplot as plt
from prettytable import PrettyTable


def printTableBy(df: pd.DataFrame, field: str, how_many: int, title: str) -> None:
    """
    Prints a PrettyTable showing the top and bottom counties based on a given field.

    Parameters:
        df (pd.DataFrame): The dataset
        field (str): Column to sort by
        how_many (int): Number of rows to display (top and bottom)
        title (str): Title to print above the table
    """

    table = PrettyTable()
    table.field_names = ["State", "County", "PCI", "Poverty Rate", "Unemployment"]

    print("\n" + title)

    # Top (descending)
    top = df.sort_values(by=field, ascending=False).head(how_many)
    for _, row in top.iterrows():
        table.add_row([
            f"{row['state']:<20}",
            f"{row['county']:<20}",
            f"{row['pci']:.2f}",
            f"{row['poverty_rate']:.2f}",
            f"{row['unemployment']:.2f}"
        ])

    table.add_divider()

    # Bottom (ascending)
    bottom = df.sort_values(by=field, ascending=True).head(how_many)
    for _, row in bottom.iterrows():
        table.add_row([
            f"{row['state']:<20}",
            f"{row['county']:<20}",
            f"{row['pci']:.2f}",
            f"{row['poverty_rate']:.2f}",
            f"{row['unemployment']:.2f}"
        ])

    print(table)


def createByStateBarPlot(
    df: pd.DataFrame,
    field: str,
    filename: str,
    title: str,
    ylabel: str
) -> None:
    """
    Creates and saves a bar plot of state averages for a given field.

    Parameters:
        df (pd.DataFrame): The dataset
        field (str): Column to analyze
        filename (str): Output PNG file
        title (str): Plot title
        ylabel (str): Y-axis label
    """

    grouped = df.groupby("state")[field].mean().sort_values()

    state_abbrev = {
        "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR",
        "California": "CA", "Colorado": "CO", "Connecticut": "CT",
        "Delaware": "DE", "Florida": "FL", "Georgia": "GA",
        "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN",
        "Iowa": "IA", "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA",
        "Maine": "ME", "Maryland": "MD", "Massachusetts": "MA",
        "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS",
        "Missouri": "MO", "Montana": "MT", "Nebraska": "NE",
        "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ",
        "New Mexico": "NM", "New York": "NY", "North Carolina": "NC",
        "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK",
        "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI",
        "South Carolina": "SC", "South Dakota": "SD", "Tennessee": "TN",
        "Texas": "TX", "Utah": "UT", "Vermont": "VT", "Virginia": "VA",
        "Washington": "WA", "West Virginia": "WV", "Wisconsin": "WI",
        "Wyoming": "WY"
    }

    grouped.index = [state_abbrev.get(s, s) for s in grouped.index]

    plt.figure(figsize=(12, 6))
    plt.bar(grouped.index, grouped.values)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xticks(rotation=90)

    plt.savefig(filename)
    plt.close()


# =========================
# DATA LOADING + CLEANING
# =========================

arc_data = pd.read_csv(
    "county_economic_status_2025.csv",
    skiprows=4,
    thousands=","
)

arc_data = arc_data.iloc[1:].reset_index(drop=True)

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

arc_data.loc[:, "pci"] = pd.to_numeric(arc_data["pci"])
arc_data.loc[:, "poverty_rate"] = pd.to_numeric(arc_data["poverty_rate"])
arc_data.loc[:, "unemployment"] = pd.to_numeric(arc_data["unemployment"])


# =========================
# ANALYSIS OUTPUT
# =========================

print("\nPoverty Rate Stats:")
print("Mean:", arc_data["poverty_rate"].mean())
print("Std:", arc_data["poverty_rate"].std())
print("Min:", arc_data["poverty_rate"].min())
print("Max:", arc_data["poverty_rate"].max())

print("\nType of state column:")
print(type(arc_data["state"]))

counts = arc_data["state"].value_counts()

print("\nCounties per state:")
print(counts)


# =========================
# TOP / BOTTOM STATES
# =========================

top_states = counts.head(10)

table = PrettyTable()
table.field_names = ["State", "# Counties", "PCI Mean", "PCI Median", "Poverty Rate"]

for state in top_states.index:
    state_data = arc_data[arc_data["state"] == state]
    table.add_row([
        state,
        len(state_data),
        f"{state_data['pci'].mean():.2f}",
        f"{state_data['pci'].median():.2f}",
        f"{state_data['poverty_rate'].mean():.2f}"
    ])

print("\nTOP 10 STATES:")
print(table)


bottom_states = counts.drop("District of Columbia", errors="ignore").sort_values().head(10)

table = PrettyTable()
table.field_names = ["State", "# Counties", "PCI Mean", "PCI Median", "Poverty Rate"]

for state in bottom_states.index:
    state_data = arc_data[arc_data["state"] == state]
    table.add_row([
        state,
        len(state_data),
        f"{state_data['pci'].mean():.2f}",
        f"{state_data['pci'].median():.2f}",
        f"{state_data['poverty_rate'].mean():.2f}"
    ])

print("\nBOTTOM 10 STATES:")
print(table)


# =========================
# REQUIRED FUNCTION USAGE
# =========================

printTableBy(arc_data, "poverty_rate", 10, "COUNTIES BY POVERTY RATE")
printTableBy(arc_data, "pci", 10, "COUNTIES BY INCOME")
printTableBy(arc_data, "unemployment", 10, "COUNTIES BY UNEMPLOYMENT")


# =========================
# BAR PLOTS
# =========================

createByStateBarPlot(arc_data, "poverty_rate", "poverty.png", "States by Poverty Rate", "Poverty Rate")
createByStateBarPlot(arc_data, "pci", "pci.png", "States by Income", "Income")
createByStateBarPlot(arc_data, "unemployment", "unemployment.png", "States by Unemployment", "Unemployment")