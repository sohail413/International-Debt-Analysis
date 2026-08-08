

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# ------------------------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------------------------
st.set_page_config(
    page_title="International Debt Statistics Dashboard",
    page_icon="💰",
    layout="wide",
)

DATA_FILE = "cleaned_debt_data.csv"


# ------------------------------------------------------------------------
# DATA LOADING (cached)
# ------------------------------------------------------------------------
@st.cache_data
def load_data():
    if not os.path.exists(DATA_FILE):
        return None
    df = pd.read_csv(DATA_FILE)
    # Only keep real countries (drop region/income-group aggregate rows)
    # for country-level insights, but retain full df for indicator EDA.
    return df


df = load_data()

if df is None:
    st.error(
        f"Could not find `{DATA_FILE}`. Please run `data_cleaning.py` first "
        "to generate the cleaned dataset, then place it next to this app."
    )
    st.stop()

# Countries only (exclude World Bank aggregate groupings like income levels)
countries_df = df[df["Is Aggregate"] == False].copy()

# ------------------------------------------------------------------------
# SIDEBAR FILTERS
# ------------------------------------------------------------------------
st.sidebar.title("🔎 Filters")

years = sorted(countries_df["Year"].unique())
year_range = st.sidebar.slider(
    "Year range",
    min_value=int(min(years)),
    max_value=int(max(years)),
    value=(int(min(years)), int(max(years))),
)

regions = sorted(countries_df["Region"].dropna().unique())
selected_regions = st.sidebar.multiselect("Region", regions, default=regions)

income_groups = sorted(countries_df["Income Group"].dropna().unique())
selected_income = st.sidebar.multiselect(
    "Income Group", income_groups, default=income_groups
)

all_indicators = sorted(countries_df["Series Name"].dropna().unique())
default_indicator = "Debt service on external debt, total (TDS, current US$)"
default_indicator = default_indicator if default_indicator in all_indicators else all_indicators[0]

selected_indicator = st.sidebar.selectbox(
    "Primary Debt Indicator (used across most charts)",
    all_indicators,
    index=all_indicators.index(default_indicator),
)

# Apply filters
mask = (
    countries_df["Year"].between(year_range[0], year_range[1])
    & countries_df["Region"].isin(selected_regions)
    & countries_df["Income Group"].isin(selected_income)
)
fdf = countries_df[mask].copy()

indicator_df = fdf[fdf["Series Name"] == selected_indicator].copy()

# ------------------------------------------------------------------------
# HEADER
# ------------------------------------------------------------------------
st.title("💰 International Debt Statistics Dashboard")
st.caption(
    "Explore external debt trends across countries, regions, and indicators "
    "using World Bank International Debt Statistics (IDS) data."
)

# ------------------------------------------------------------------------
# KPI ROW
# ------------------------------------------------------------------------
k1, k2, k3, k4 = st.columns(4)
k1.metric("Countries in view", f"{fdf['Country Name'].nunique():,}")
k2.metric("Indicators available", f"{fdf['Series Name'].nunique():,}")
k3.metric("Year range", f"{year_range[0]} – {year_range[1]}")
if len(indicator_df):
    total_latest_year = indicator_df["Year"].max()
    total_val = indicator_df[indicator_df["Year"] == total_latest_year]["Value"].sum()
    k4.metric(f"Total '{selected_indicator[:22]}...' ({total_latest_year})",
              f"${total_val/1e9:,.1f}B")
else:
    k4.metric("Total (selected indicator)", "No data")

st.markdown("---")

# ------------------------------------------------------------------------
# TABS
# ------------------------------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["🌍 Country-wise Debt", "🏆 Top / Bottom Countries",
     "📊 Indicator Distribution", "📈 Trends Over Time", "🗂️ Raw Data Explorer"]
)

# ==========================================================================
# TAB 1 - COUNTRY-WISE DEBT DISTRIBUTION
# ==========================================================================
with tab1:
    st.subheader(f"Country-wise distribution — {selected_indicator}")

    latest_year = indicator_df["Year"].max() if len(indicator_df) else None

    if latest_year is not None:
        snap = indicator_df[indicator_df["Year"] == latest_year]
        snap_by_country = (
            snap.groupby(["Country Name", "Country Code", "Region"], as_index=False)["Value"]
            .sum()
        )

        c1, c2 = st.columns([2, 1])

        with c1:
            fig_map = px.choropleth(
                snap_by_country,
                locations="Country Code",
                color="Value",
                hover_name="Country Name",
                color_continuous_scale="Reds",
                title=f"World map — {selected_indicator} ({latest_year})",
            )
            fig_map.update_layout(margin=dict(l=0, r=0, t=40, b=0))
            st.plotly_chart(fig_map, use_container_width=True)

        with c2:
            region_sum = snap_by_country.groupby("Region", as_index=False)["Value"].sum()
            fig_pie = px.pie(
                region_sum, names="Region", values="Value",
                title=f"Share by Region ({latest_year})", hole=0.4
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        st.markdown("#### Debt value by country (sortable table)")
        st.dataframe(
            snap_by_country.sort_values("Value", ascending=False)
            .reset_index(drop=True),
            use_container_width=True,
        )
    else:
        st.info("No data available for the selected indicator/filters.")

# ==========================================================================
# TAB 2 - TOP / BOTTOM COUNTRIES
# ==========================================================================
with tab2:
    st.subheader(f"Top & Bottom Countries — {selected_indicator}")

    if latest_year is not None:
        n = st.slider("Number of countries to show", 5, 30, 10)

        top_n = snap_by_country.sort_values("Value", ascending=False).head(n)
        bottom_n = snap_by_country[snap_by_country["Value"] > 0].sort_values(
            "Value", ascending=True
        ).head(n)

        c1, c2 = st.columns(2)
        with c1:
            fig_top = px.bar(
                top_n.sort_values("Value"),
                x="Value", y="Country Name", orientation="h",
                color="Value", color_continuous_scale="Reds",
                title=f"Top {n} countries ({latest_year})",
            )
            st.plotly_chart(fig_top, use_container_width=True)

        with c2:
            fig_bottom = px.bar(
                bottom_n.sort_values("Value", ascending=False),
                x="Value", y="Country Name", orientation="h",
                color="Value", color_continuous_scale="Blues",
                title=f"Bottom {n} countries (nonzero, {latest_year})",
            )
            st.plotly_chart(fig_bottom, use_container_width=True)
    else:
        st.info("No data available for the selected indicator/filters.")

# ==========================================================================
# TAB 3 - DEBT DISTRIBUTION ACROSS INDICATORS
# ==========================================================================
with tab3:
    st.subheader("Debt distribution across different indicators")

    top_k = st.slider("Number of top indicators to display", 5, 25, 10)

    latest_year_all = fdf["Year"].max()
    snap_all = fdf[fdf["Year"] == latest_year_all]

    ind_sum = (
        snap_all.groupby("Series Name", as_index=False)["Value"]
        .sum()
        .sort_values("Value", ascending=False)
        .head(top_k)
    )

    fig_ind = px.bar(
        ind_sum.sort_values("Value"),
        x="Value", y="Series Name", orientation="h",
        title=f"Top {top_k} indicators by total value ({latest_year_all})",
        color="Value", color_continuous_scale="Viridis",
    )
    fig_ind.update_layout(height=500)
    st.plotly_chart(fig_ind, use_container_width=True)

    st.markdown("#### Topic-level breakdown")
    topic_sum = (
        snap_all.groupby("Topic", as_index=False)["Value"]
        .sum()
        .dropna()
        .sort_values("Value", ascending=False)
    )
    fig_topic = px.treemap(
        topic_sum, path=["Topic"], values="Value",
        title=f"Debt value by Topic ({latest_year_all})"
    )
    st.plotly_chart(fig_topic, use_container_width=True)

# ==========================================================================
# TAB 4 - TRENDS OVER TIME
# ==========================================================================
with tab4:
    st.subheader(f"Trends over time — {selected_indicator}")

    trend_by_region = (
        indicator_df.groupby(["Year", "Region"], as_index=False)["Value"].sum()
    )
    fig_trend = px.line(
        trend_by_region, x="Year", y="Value", color="Region",
        markers=True, title=f"{selected_indicator} trend by Region"
    )
    st.plotly_chart(fig_trend, use_container_width=True)

    st.markdown("#### Compare specific countries")
    default_countries = (
        snap_by_country.sort_values("Value", ascending=False)["Country Name"]
        .head(5).tolist() if latest_year is not None else []
    )
    compare_countries = st.multiselect(
        "Select countries to compare",
        sorted(fdf["Country Name"].unique()),
        default=default_countries,
    )
    if compare_countries:
        cc_df = indicator_df[indicator_df["Country Name"].isin(compare_countries)]
        fig_cc = px.line(
            cc_df, x="Year", y="Value", color="Country Name",
            markers=True, title=f"{selected_indicator} — country comparison"
        )
        st.plotly_chart(fig_cc, use_container_width=True)

    st.markdown("#### Year-over-year % change (Total, selected filters)")
    yoy = indicator_df.groupby("Year", as_index=False)["Value"].sum()
    yoy["YoY % Change"] = yoy["Value"].pct_change() * 100
    fig_yoy = px.bar(yoy, x="Year", y="YoY % Change",
                      title="Year-over-year % change in total value",
                      color="YoY % Change", color_continuous_scale="RdYlGn")
    st.plotly_chart(fig_yoy, use_container_width=True)

# ==========================================================================
# TAB 5 - RAW DATA EXPLORER
# ==========================================================================
with tab5:
    st.subheader("Raw / Filtered Data Explorer")
    st.write(f"Showing {len(fdf):,} rows matching current sidebar filters.")
    st.dataframe(fdf.head(5000), use_container_width=True)

    csv = fdf.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download filtered data as CSV",
        data=csv,
        file_name="filtered_debt_data.csv",
        mime="text/csv",
    )

# ------------------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------------------
st.markdown("---")
st.caption(
    "Data source: World Bank International Debt Statistics (IDS). "
    "Dashboard built with Streamlit + Plotly."
)
