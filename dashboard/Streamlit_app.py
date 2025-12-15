import streamlit as st
import pandas as pd
import altair as alt

# Dashboard Title
st.title("📈U.S. Labor Market Dashboard (2020–Present)")

# Load dataset
df = pd.read_csv("data/bls_data.csv")
df["date"] = pd.to_datetime(df["date"])

# Add sidebar
st.sidebar.title("📊 Project Information")

st.sidebar.markdown("### Data Source")
st.sidebar.markdown("""
The data comes directly from the BLS API and is automatically updated using GitHub Actions.
U.S. Bureau of Labor Statistics (BLS)  
https://www.bls.gov/
""")

st.sidebar.markdown("### Data Series Included")
st.sidebar.markdown("""
- **Unemployment Rate**  
- **Total Nonfarm Employment**  
- **Avg Weekly Hours (Private)**  
- **Avg Hourly Earnings (Private)**
""")
# Calculate time range dynamically from data
start_date = df["date"].min().strftime("%B %Y")
end_date = df["date"].max().strftime("%B %Y")

st.sidebar.markdown("### Time Range")
st.sidebar.markdown(f"""
{start_date} – {end_date}
""")

st.sidebar.markdown("### About This Dashboard")
st.sidebar.markdown("""
This dashboard visualizes key U.S. labor market indicators
to illustrate changes during the COVID-19 pandemic and the
subsequent recovery period.
""")

# Year range slider

min_year = df["date"].dt.year.min()
max_year = df["date"].dt.year.max()

st.subheader("📅 Select Year Range")
year_range = st.slider(
    "Year Range:",
    min_year, max_year, (min_year, max_year)
)


# Filter dataframe by year range
df_filtered = df[(df["date"].dt.year >= year_range[0]) &
                 (df["date"].dt.year <= year_range[1])]


# Series selector

st.subheader("🔍 Select a Series to Visualize")
series_options = df_filtered["series_name"].unique()
selected = st.selectbox("Labor Statistic Series:", series_options)

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
        title=f"Trends for {selected} ({year_range[0]}–{year_range[1]})"
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

# Add data download button

st.subheader("📥 Download Raw Data")

csv_data = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download BLS Data (CSV)",
    data=csv_data,
    file_name="bls_data.csv",
    mime="text/csv"
)
