import pandas as pd
import requests
import streamlit as st
import plotly.express as px


st.set_page_config(page_title="yyc-building-energy-benchmarking", page_icon="house")
_, center, _ = st.columns([2, 1, 2])
with center:
    st.image(
        "https://cdn1.iconfinder.com/data/icons/provincial-electricity-authority-2/64/building_construction_urban_power_energy-512.png",
        use_column_width=True,
    )
st.title("yyc-building-energy-benchmarking")
st.caption(
    "A visualization on building energy and greenhouse gas emission performance information of selected properties"
)


@st.cache_data
def load_df():
    yyc_data_url = "https://data.calgary.ca/resource/8twd-upbv.json"
    response = requests.get(yyc_data_url)
    df = pd.DataFrame(response.json())
    df["energy_star_score"] = pd.to_numeric(df["energy_star_score"])
    df["site_eui_gj_m"] = pd.to_numeric(df["site_eui_gj_m"])
    return df


df = load_df()
df


st.subheader("Energy Star Score")
fig = px.histogram(
    df,
    x="energy_star_score",
    labels={
        "energy_star_score": "Energy Star Score",
    },
)
fig

fig = px.scatter(
    df,
    x="energy_star_score",
    y="site_eui_gj_m",
    labels={
        "energy_star_score": "Energy Star Score",
        "site_eui_gj_m": "Site EUI (GJ/m²)",
    },
)
fig


st.subheader("Number of Properties")
fig = px.bar(
    df.groupby("year_ending").count().reset_index(),
    x="year_ending",
    y="property_id",
    color="year_ending",
    labels={
        "property_id": "# of properties",
        "year_ending": "Year",
    },
)
fig.update_layout(
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
    )
)
fig

num_of_records_per_property = (
    df.groupby("property_id").apply(lambda group: group["year_ending"].count()).tolist()
)
if len(set(num_of_records_per_property)) == 1:
    y = set(num_of_records_per_property).pop()
    p = len(num_of_records_per_property)
    st.caption(f"All {p} properties have {y} years of records.")


st.subheader("Total GHG Emissions Intensity")
property_ids = st.multiselect("property", df["property_id"].unique())
if property_ids:
    fig = px.line(
        df[df["property_id"].isin(property_ids)],
        x="year_ending",
        y="total_ghg_emissions_intensity",
        color="property_id",
        labels={
            "total_ghg_emissions_intensity": "Total GHG Emissions Intensity",
            "year_ending": "Year",
        },
    )

    fig
