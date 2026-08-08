

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)

OUT_DIR = "eda_charts"
os.makedirs(OUT_DIR, exist_ok=True)


def load():
    df = pd.read_csv("cleaned_debt_data.csv")
    countries = df[df["Is Aggregate"] == False].copy()
    return df, countries


def basic_overview(df, countries):
    print("=" * 70)
    print("BASIC DATASET OVERVIEW")
    print("=" * 70)
    print(f"Total rows (long format): {len(df):,}")
    print(f"Unique countries: {countries['Country Name'].nunique()}")
    print(f"Unique indicators (series): {df['Series Name'].nunique()}")
    print(f"Year range: {df['Year'].min()} - {df['Year'].max()}")
    print(f"Regions: {sorted(countries['Region'].dropna().unique())}")
    print(f"Income groups: {sorted(countries['Income Group'].dropna().unique())}")
    print("\nMissing values per key column:")
    print(df[["Country Name", "Series Name", "Year", "Value"]].isna().sum())
    print()


def top_bottom_countries(countries, indicator, n=10):
    print("=" * 70)
    print(f"TOP / BOTTOM {n} COUNTRIES — {indicator}")
    print("=" * 70)
    ind_df = countries[countries["Series Name"] == indicator]
    latest_year = ind_df["Year"].max()
    snap = ind_df[ind_df["Year"] == latest_year].groupby("Country Name")["Value"].sum()

    top = snap.sort_values(ascending=False).head(n)
    bottom = snap[snap > 0].sort_values().head(n)

    print(f"\nTop {n} ({latest_year}):")
    print(top)
    print(f"\nBottom {n} nonzero ({latest_year}):")
    print(bottom)

    fig, ax = plt.subplots()
    top.sort_values().plot(kind="barh", ax=ax, color="firebrick")
    ax.set_title(f"Top {n} countries — {indicator} ({latest_year})")
    ax.set_xlabel("Value (current US$)")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "top10_countries_latest.png"), dpi=150)
    plt.close()
    print(f"\nSaved chart -> {OUT_DIR}/top10_countries_latest.png\n")
    return snap, latest_year


def debt_by_region(countries, indicator, latest_year):
    print("=" * 70)
    print(f"DEBT DISTRIBUTION BY REGION — {indicator} ({latest_year})")
    print("=" * 70)
    ind_df = countries[
        (countries["Series Name"] == indicator) & (countries["Year"] == latest_year)
    ]
    region_sum = ind_df.groupby("Region")["Value"].sum().sort_values(ascending=False)
    print(region_sum)

    fig, ax = plt.subplots()
    region_sum.plot(kind="bar", ax=ax, color="steelblue")
    ax.set_title(f"Debt by Region — {indicator} ({latest_year})")
    ax.set_ylabel("Value (current US$)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "debt_by_region.png"), dpi=150)
    plt.close()
    print(f"\nSaved chart -> {OUT_DIR}/debt_by_region.png\n")


def income_group_debt(countries, indicator, latest_year):
    print("=" * 70)
    print(f"DEBT BY INCOME GROUP — {indicator} ({latest_year})")
    print("=" * 70)
    ind_df = countries[
        (countries["Series Name"] == indicator) & (countries["Year"] == latest_year)
    ]
    inc_sum = ind_df.groupby("Income Group")["Value"].sum().sort_values(ascending=False)
    print(inc_sum)

    fig, ax = plt.subplots()
    inc_sum.plot(kind="bar", ax=ax, color="seagreen")
    ax.set_title(f"Debt by Income Group — {indicator} ({latest_year})")
    ax.set_ylabel("Value (current US$)")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "income_group_debt.png"), dpi=150)
    plt.close()
    print(f"\nSaved chart -> {OUT_DIR}/income_group_debt.png\n")


def top_indicators(df, latest_year):
    print("=" * 70)
    print(f"TOP 10 INDICATORS BY TOTAL VALUE ({latest_year})")
    print("=" * 70)
    snap = df[df["Year"] == latest_year]
    top_ind = snap.groupby("Series Name")["Value"].sum().sort_values(ascending=False).head(10)
    print(top_ind)

    fig, ax = plt.subplots()
    top_ind.sort_values().plot(kind="barh", ax=ax, color="darkorange")
    ax.set_title(f"Top 10 Indicators by Total Value ({latest_year})")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "top_indicators.png"), dpi=150)
    plt.close()
    print(f"\nSaved chart -> {OUT_DIR}/top_indicators.png\n")


def global_trend(countries, indicator):
    print("=" * 70)
    print(f"GLOBAL TREND OVER TIME — {indicator}")
    print("=" * 70)
    ind_df = countries[countries["Series Name"] == indicator]
    trend = ind_df.groupby("Year")["Value"].sum()
    print(trend)

    fig, ax = plt.subplots()
    trend.plot(ax=ax, marker="o", color="purple")
    ax.set_title(f"Global Trend — {indicator}")
    ax.set_ylabel("Total value (current US$)")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "global_trend.png"), dpi=150)
    plt.close()
    print(f"\nSaved chart -> {OUT_DIR}/global_trend.png\n")


def run_eda():
    df, countries = load()
    basic_overview(df, countries)

    # Pick a widely-populated headline indicator
    indicator = "Debt service on external debt, total (TDS, current US$)"
    if indicator not in countries["Series Name"].unique():
        indicator = countries["Series Name"].value_counts().index[0]

    snap, latest_year = top_bottom_countries(countries, indicator)
    debt_by_region(countries, indicator, latest_year)
    income_group_debt(countries, indicator, latest_year)
    top_indicators(df, latest_year)
    global_trend(countries, indicator)

    print("=" * 70)
    print("EDA COMPLETE. Charts saved in ./eda_charts/")
    print("=" * 70)


if __name__ == "__main__":
    run_eda()
