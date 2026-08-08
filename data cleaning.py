

import pandas as pd
import numpy as np
import os

# --------------------------------------------------------------------------
# 0. CONFIG
# --------------------------------------------------------------------------
RAW_DATA_PATH = "."   # folder containing the raw CSVs
OUTPUT_PATH = "."     # folder to write cleaned_debt_data.csv

MAIN_FILE = os.path.join(RAW_DATA_PATH, "IDS_ALLCountries_Data (1).csv")
COUNTRY_META_FILE = os.path.join(RAW_DATA_PATH, "IDS_CountryMetaData (1).csv")
SERIES_META_FILE = os.path.join(RAW_DATA_PATH, "IDS_SeriesMetaData (1).csv")

# The World Bank export uses latin-1 encoding, not utf-8
ENCODING = "latin1"

# Only keep actual/historical data up to this year (drops forecast years,
# e.g. 2025-2032, which are projections rather than reported figures)
MAX_YEAR = 2024


def load_raw_data():
    """Load the three CSV files needed for the pipeline."""
    print("Loading raw files...")
    main_df = pd.read_csv(MAIN_FILE, encoding=ENCODING)
    country_meta = pd.read_csv(COUNTRY_META_FILE, encoding=ENCODING)
    series_meta = pd.read_csv(SERIES_META_FILE, encoding=ENCODING)
    print(f"  Main data:      {main_df.shape}")
    print(f"  Country meta:   {country_meta.shape}")
    print(f"  Series meta:    {series_meta.shape}")
    return main_df, country_meta, series_meta


def clean_main_data(main_df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the wide-format main data file:
      - Drop footer/summary rows (World Bank appends metadata rows at the
        bottom of the export, e.g. "Data from database: ...")
      - Strip whitespace from text columns (Country Code has trailing spaces)
      - Melt year columns (2000...2032) into a single 'Year' / 'Value' pair
      - Convert Value to numeric, drop rows with no data at all
    """
    df = main_df.copy()

    # 1. Drop footer rows: valid rows must have a non-null Country Code
    df = df[df["Country Code"].notna()].copy()
    df = df[df["Country Code"].astype(str).str.len() <= 10].copy()  # guards against stray text rows

    # 2. Strip whitespace from key text columns
    text_cols = ["Country Name", "Country Code", "Counterpart-Area Name",
                 "Counterpart-Area Code", "Series Name", "Series Code"]
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    # 3. Identify year columns (numeric-looking column names), capped at MAX_YEAR
    year_cols = [c for c in df.columns
                 if str(c).strip().isdigit() and int(str(c).strip()) <= MAX_YEAR]

    id_cols = ["Country Name", "Country Code", "Counterpart-Area Name",
               "Counterpart-Area Code", "Series Name", "Series Code"]

    # 4. Melt (wide -> long) so we get one row per Country-Series-Year
    long_df = df.melt(
        id_vars=id_cols,
        value_vars=year_cols,
        var_name="Year",
        value_name="Value"
    )

    # 5. Clean the Value column: World Bank uses ".." / blank for missing data
    long_df["Value"] = long_df["Value"].replace(["..", "", " ", "NA"], np.nan)
    long_df["Value"] = pd.to_numeric(long_df["Value"], errors="coerce")

    # 6. Drop rows with no value at all (keeps file size manageable)
    long_df = long_df.dropna(subset=["Value"])

    # 7. Correct dtypes
    long_df["Year"] = long_df["Year"].astype(int)

    # 8. Drop exact duplicate rows
    long_df = long_df.drop_duplicates()

    print(f"Cleaned long-format data: {long_df.shape}")
    return long_df


def clean_country_meta(country_meta: pd.DataFrame) -> pd.DataFrame:
    """Keep only the useful columns from country metadata and rename them."""
    keep_cols = ["Code", "Long Name", "Income Group", "Region",
                 "Lending category", "Currency Unit"]
    keep_cols = [c for c in keep_cols if c in country_meta.columns]
    meta = country_meta[keep_cols].copy()
    meta = meta.rename(columns={"Code": "Country Code"})
    meta["Country Code"] = meta["Country Code"].astype(str).str.strip()
    # Drop rows that are aggregates without a region (e.g. "World", income-group rows)
    meta = meta.dropna(subset=["Region"])
    return meta


def clean_series_meta(series_meta: pd.DataFrame) -> pd.DataFrame:
    """Keep only useful columns describing each debt indicator."""
    keep_cols = ["Code", "Indicator Name", "Topic", "Periodicity", "Aggregation method"]
    keep_cols = [c for c in keep_cols if c in series_meta.columns]
    meta = series_meta[keep_cols].copy()
    meta = meta.rename(columns={"Code": "Series Code"})
    meta["Series Code"] = meta["Series Code"].astype(str).str.strip()
    return meta


def merge_all(long_df, country_meta, series_meta) -> pd.DataFrame:
    """Join country + series metadata onto the long-format debt data."""
    merged = long_df.merge(country_meta, on="Country Code", how="left")
    merged = merged.merge(series_meta, on="Series Code", how="left")

    # Rows where Region is NaN are World/Region aggregates already present in
    # the raw file as "countries" (e.g. "Low income", "World") — flag them
    merged["Is Aggregate"] = merged["Region"].isna()

    return merged


def run_pipeline():
    main_df, country_meta_raw, series_meta_raw = load_raw_data()

    long_df = clean_main_data(main_df)
    country_meta = clean_country_meta(country_meta_raw)
    series_meta = clean_series_meta(series_meta_raw)

    final_df = merge_all(long_df, country_meta, series_meta)

    out_file = os.path.join(OUTPUT_PATH, "cleaned_debt_data.csv")
    final_df.to_csv(out_file, index=False)
    print(f"\nSaved cleaned dataset -> {out_file}")
    print(f"Final shape: {final_df.shape}")
    print("\nColumns:", list(final_df.columns))
    print("\nSample rows:")
    print(final_df.head())

    return final_df


if __name__ == "__main__":
    run_pipeline()
