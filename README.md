# International-Debt-Analysis

# International Debt Statistics — Analytics Pipeline

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

## 3. Dashboard
```bash
streamlit run app.py
```
Open the local URL Streamlit prints (usually http://localhost:8501).

### Dashboard tabs
1. **Country-wise Debt** — choropleth map + region pie + sortable table for the selected indicator/year
2. **Top / Bottom Countries** — adjustable top-N / bottom-N bar charts
3. **Indicator Distribution** — top indicators by value + topic-level treemap
4. **Trends Over Time** — regional trend lines, country comparison, YoY % change
5. **Raw Data Explorer** — filtered table + CSV download

### Sidebar filters
Year range · Region · Income Group · Primary indicator (drives most charts)

## Notes
- Data source: World Bank International Debt Statistics (IDS), through 2032 (forecast years included where reported).
- "Is Aggregate" flag distinguishes real countries from WB aggregate groupings (income levels, etc.) — the dashboard uses only real countries for country-level views.
