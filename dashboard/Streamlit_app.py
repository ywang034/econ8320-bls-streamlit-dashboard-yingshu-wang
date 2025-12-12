import streamlit as st
import pandas as pd
import altair as alt

# Dashboard Title
st.title("📈U.S. Labor Market Dashboard (2020–Present)")
st.markdown("""
This dashboard visualizes selected labor statistics from the **US Bureau of Labor Statistics (BLS)**, 
focusing on trends since the COVID-19 pandemic and the subsequent recovery period.
""")

# Load dataset
df = pd.read_csv("data/bls_data.csv")
df["date"] = pd.to_datetime(df["date"])

# Year range slider

min_year = df["date"].dt.year.min()
max_year = df["date"].dt.year.max()

year_range = st.slider(
    "📅 Select Year Range:",
    min_year, max_year, (min_year, max_year)
)

# Filter dataframe by year range
df_filtered = df[(df["date"].dt.year >= year_range[0]) &
                 (df["date"].dt.year <= year_range[1])]


# Series selector

series_options = df_filtered["series_name"].unique()
selected = st.selectbox("🔍 Select a Series to Visualize:", series_options)

plot_df = df_filtered[df_filtered["series_name"] == selected]


# Create Altair chart

chart = (
    alt.Chart(plot_df)
    .mark_line()
    .encode(
        x=alt.X("date:T", title="Date"),
        y=alt.Y("value:Q", title=selected),
        tooltip=["date:T", "value:Q"]
    )
    .properties(
        height=400,
        title=f"{selected} ({year_range[0]}–{year_range[1]})"
    )
)


# Shaded pandemic periods


pandemic_periods = pd.DataFrame({
    "start": ["2020-03-01", "2022-01-01"],
    "end":   ["2021-12-01", "2025-01-01"],
    "label": ["Pandemic", "Post-Pandemic"],
    "color": ["#ff9999", "#b3ffcc"]  # Light red, light green
})

pandemic_bands = (
    alt.Chart(pandemic_periods)
    .mark_rect(opacity=0.25)
    .encode(
        x="start:T",
        x2="end:T",
        color=alt.Color("label:N", scale=alt.Scale(
            domain=["Pandemic", "Post-Pandemic"],
            range=["#ff9999", "#b3ffcc"]
        ))
    )
)

# Display chart

st.altair_chart(pandemic_bands + chart, use_container_width=True)
