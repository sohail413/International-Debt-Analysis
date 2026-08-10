# International-Debt-Analysis

## International Debt Statistics — Analytics Pipeline

End-to-end pipeline: clean raw World Bank IDS data → EDA → interactive Streamlit dashboard.

## Files
- `data_cleaning.py` — cleans the 5 raw IDS CSVs into one tidy file: `cleaned_debt_data.csv`
- `eda.py` — exploratory analysis; prints insights, saves charts to `eda_charts/`
- `app.py` — Streamlit dashboard (5 tabs: country map, top/bottom countries, indicator distribution, trends, raw data explorer)
- `cleaned_debt_data.csv` — already generated for you from your uploaded files, so the app runs immediately
- `requirements.txt`

## Setup
```bash
pip install -r requirements.txt
```

## 1. Data Cleaning (re-run if you get new raw exports)
Place the raw World Bank files in the same folder, named:
`IDS_ALLCountries_Data.csv`, `IDS_CountryMetaData.csv`, `IDS_SeriesMetaData.csv`
(rename the `_1_` suffixed downloads, or edit the paths at the top of the script), then:
```bash
python data_cleaning.py
```
This produces `cleaned_debt_data.csv` (long/tidy format: one row per Country × Indicator × Year),
merged with country metadata (Region, Income Group) and series metadata (Topic, Indicator Name).

## 2. EDA
```bash
python eda.py
```
Prints console insights (top/bottom countries, region & income-group breakdowns, top indicators,
global trend) and saves 5 PNG charts to `eda_charts/`.

## 3. Dashboard — Unified App (CSV **or** PostgreSQL)
`app.py` is a single Streamlit app that can run off **either** data source —
pick it with the radio button at the top of the sidebar:

- **CSV File** — reads `cleaned_debt_data.csv` (from step 1 above). Gives you full
  Region / Income Group / Topic / world-map features since the CSV carries that metadata.
- **PostgreSQL Database** — connects live to your pgAdmin-managed DB. Expects:
  - `debt` — columns: `"country name"`, `"series code"`, `year`, `value`
  - `seriesmd` — columns: `code`, `"indicator name"`

  Enter Host / Port / Database / User / Password in the sidebar (or set env vars
  `DB_HOST` / `DB_PORT` / `DB_NAME` / `DB_USER` / `DB_PASSWORD` before launching).
  Since the raw `debt`/`seriesmd` tables don't carry Region/Income Group/Topic,
  the app gracefully falls back to country-only views (bar chart instead of
  choropleth map, etc.) in this mode — an extra **🛠️ Custom SQL Query** tab is
  also added so you can run any read-only query straight from the dashboard.

```bash
streamlit run app.py
```
Open the local URL Streamlit prints (usually http://localhost:8501).

### Dashboard tabs
1. **Country-wise Debt** — choropleth map (CSV mode) or bar chart (DB mode) + region/top-5 pie + sortable table
2. **Top / Bottom Countries** — adjustable top-N / bottom-N bar charts
3. **Indicator Distribution** — top indicators by value + topic treemap (CSV mode only)
4. **Trends Over Time** — regional/global trend lines, country comparison, cumulative debt, YoY % change
5. **Rankings & Tiers** — ranked table, High/Medium/Low tier classification, max−min spread
6. **5%+ Contributors** — countries over 5% share of the selected total, top-3-per-indicator
7. **Raw Data Explorer** — filtered table + CSV download
8. **Custom SQL Query** *(PostgreSQL mode only)* — free-form read-only SQL box with CSV export

### Sidebar filters
Data source toggle · Year range · Region · Income Group (CSV mode only) · Primary indicator (drives most charts)

## Notes
- Data source: World Bank International Debt Statistics (IDS), through 2032 (forecast years included where reported).
- "Is Aggregate" flag distinguishes real countries from WB aggregate groupings (income levels, etc.) — the dashboard uses only real countries for country-level views.
