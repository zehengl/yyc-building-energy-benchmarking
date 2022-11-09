import pandas as pd
import requests
import streamlit as st
import plotly.express as px


st.set_page_config(page_title="yyc-building-energy-benchmarking", page_icon="random")
st.title("yyc-building-energy-benchmarking")
st.caption(
    "A visualization on building energy and greenhouse gas emission performance information of selected properties"
)


@st.cache
def load_df():
    yyc_data_url = "https://data.calgary.ca/resource/8twd-upbv.json"
    response = requests.get(yyc_data_url)
    df = pd.DataFrame(response.json())
    df["energy_star_score"] = pd.to_numeric(df["energy_star_score"])
    return df


df = load_df()
df

st.subheader("Energy Star Score")
fig = px.histogram(df, x="energy_star_score")
fig
