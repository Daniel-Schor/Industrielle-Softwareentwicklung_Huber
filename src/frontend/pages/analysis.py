import streamlit as st
import plotly.graph_objects as go

from api_fetcher import fetch_country_data, fetch_countries
from helper import convert_to_dataframe

# -- Sidebar --
selected_country = st.sidebar.selectbox(
    "Country",
    fetch_countries(),
    help="Select the Country you want to analyze and take a closer look at."
)

# -- Data Fetching --
df_country = convert_to_dataframe(fetch_country_data(selected_country))
unique_years = sorted(df_country["Year"].unique())

# -- Page Title --
st.title(f"Analysis for {selected_country}")

# -- Income over time --
fig_country = go.Figure()
if not df_country.empty:
    fig_country.add_trace(go.Scatter(
        x=df_country["Year"], y=df_country["Average_Monthly_Income"], mode='lines', name="Average Monthly Income"))
    fig_country.add_trace(go.Scatter(
        x=df_country["Year"], y=df_country["Net_Income"], mode='lines', name="Net Income"))
    fig_country.add_trace(go.Scatter(
        x=df_country["Year"], y=df_country["Savings"], mode='lines', name="Savings"))

    fig_country.update_layout(
        title=f"Average Monthly Income, Net Income, and Savings by Year for {selected_country}",
        xaxis_title="Year",
        yaxis_title="Amount ($)",
        template="plotly_dark",
        height=400,
        xaxis=dict(
            tickmode='array',
            tickvals=unique_years,
            tickformat=".0f"
        )
    )

    latest_year = df_country["Year"].max()
    latest_year_data = df_country[df_country["Year"] == latest_year]

    pie_columns = [
        "Housing_Cost", "Healthcare_Cost", "Education_Cost", "Transportation_Cost"
    ]

# -- Costs over Time --
fig_costs = go.Figure()
if not df_country.empty:
    fig_costs.add_trace(go.Scatter(
        x=df_country["Year"], y=df_country["Housing_Cost"], mode='lines', name="Housing Cost"))
    fig_costs.add_trace(go.Scatter(
        x=df_country["Year"], y=df_country["Healthcare_Cost"], mode='lines', name="Healthcare Cost"))
    fig_costs.add_trace(go.Scatter(
        x=df_country["Year"], y=df_country["Education_Cost"], mode='lines', name="Education Cost"))
    fig_costs.add_trace(go.Scatter(
        x=df_country["Year"], y=df_country["Transportation_Cost"], mode='lines', name="Transportation Cost"))

    fig_costs.update_layout(
        title=f"Various Costs over Time for {selected_country}",
        xaxis_title="Year",
        yaxis_title="Amount ($)",
        template="plotly_dark",
        height=400,
        xaxis=dict(
            tickmode='array',
            tickvals=unique_years,
            tickformat=".0f"
        )
    )

# -- Pie Chart --
if not latest_year_data.empty:
    pie_data = latest_year_data[pie_columns].iloc[0].to_dict()
    fig_pie = go.Figure(data=[go.Pie(labels=list(
        pie_data.keys()), values=list(pie_data.values()), hole=0.3)])
    fig_pie.update_layout(
        title=f"Distribution for {latest_year} in {selected_country}", template="plotly_dark")

# -- Display --
col1, col2 = st.columns([1, 0.5])
with col1:
    st.plotly_chart(fig_country)
    st.plotly_chart(fig_costs)
with col2:
    st.plotly_chart(fig_pie)
