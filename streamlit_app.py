import pandas as pd
import plotly.express as px
import requests
import streamlit as st

st.set_page_config(page_title="yyc-building-energy-benchmarking", page_icon="house")
st.title("yyc-building-energy-benchmarking")
st.caption(
    "A visualization on building energy and greenhouse gas emission performance information of selected properties"
)


@st.cache_data
def load_df():
    yyc_data_url = "https://data.calgary.ca/resource/r5x7-cju4.json"
    response = requests.get(yyc_data_url)
    df = pd.DataFrame(response.json())
    df["energy_star_score"] = pd.to_numeric(df["energy_star_score"])
    df["site_eui_gj_m"] = pd.to_numeric(df["site_eui_gj_m"])
    df["year_ending"] = pd.to_datetime(df["year_ending"]).dt.year
    df = df.sort_values(["year_ending", "property_name"])
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
    y="property_name",
    color="year_ending",
    labels={
        "property_name": "# of properties",
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
fig.update_xaxes(type="category")
fig

num_of_records_per_property = (
    df.groupby("property_name")
    .apply(lambda group: group["year_ending"].count())
    .tolist()
)
if len(set(num_of_records_per_property)) == 1:
    y = set(num_of_records_per_property).pop()
    p = len(num_of_records_per_property)
    st.caption(f"All {p} properties have {y} years of records.")


st.subheader("Total Location Based GHG")
property_names = st.multiselect("property", df["property_name"].unique())
if property_names:
    fig = px.line(
        df[df["property_name"].isin(property_names)],
        x="year_ending",
        y="total_location_based_ghg",
        color="property_name",
        labels={
            "total_location_based_ghg": "Total Location Based GHG",
            "year_ending": "Year",
        },
    )
    fig.update_xaxes(type="category")
    fig
