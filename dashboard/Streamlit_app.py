import streamlit as st
import pandas as pd
import altair as alt

st.title("U.S. Labor Market Dashboard (2020–Present)")
st.write("Trends across unemployment, employment, working hours, and wages.")

# Load dataset from GitHub
df = pd.read_csv("https://raw.githubusercontent.com/YOUR_USERNAME/bls-labor-dashboard/main/data/bls_data.csv")

df["date"] = pd.to_datetime(df["date"])

# User selects which series to view
series_options = df["series_name"].unique()
selected = st.selectbox("Select a labor market indicator:", series_options)

plot_df = df[df["series_name"] == selected]

# Create Altair chart
chart = alt.Chart(plot_df).mark_line().encode(
    x="date:T",
    y="value:Q",
    tooltip=["date:T", "value:Q"]
).properties(height=400)

# Add shaded COVID periods
pandemic_bands = alt.Chart(pd.DataFrame({
    "start": ["2020-03-01", "2022-01-01"],
    "end": ["2021-12-01", "2025-01-01"],
    "label": ["Pandemic", "Post-Pandemic"]
})).mark_rect(opacity=0.15, color="red").encode(
    x="start:T",
    x2="end:T"
)

st.altair_chart(pandemic_bands + chart, use_container_width=True)
