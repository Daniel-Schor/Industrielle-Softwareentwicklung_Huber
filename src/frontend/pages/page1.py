import streamlit as st
import requests
import plotly.graph_objects as go
import pandas as pd


@st.cache_data
def fetch_region_data() -> dict:
    """
        Ruft die Daten für alle Regionen ab

    :return: Die Daten für alle Regionen
    """
    response = requests.get('http://localhost:8000/all-information-for-region')
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error fetching data.")
        return {}


@st.cache_data
def fetch_country_data(country: str) -> dict:
    """
        Ruft die Daten für das angegebene Land ab

    :param country: Das Land, für das die Daten abgerufen werden sollen
    :return: Die Daten für das angegebene Land
    """
    url = f"http://localhost:8000/country-information/?country={country}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error fetching country details")
        return {}


def convert_to_dataframe(data: dict) -> pd.DataFrame:
    """
        Konvertiert Daten in ein DataFrame

    :param data: Die Daten, die in ein DataFrame konvertiert werden sollen
    :return: Ein DataFrame mit den konvertierten Daten
    """
    if not data:
        return pd.DataFrame()
    
    return pd.DataFrame(data)


# Fetch region data
region_data = fetch_region_data()

df_region = convert_to_dataframe(region_data)

y_axis_options = [
    "Average_Monthly_Income", "Net_Income", "Cost_of_Living", "Housing_Cost_Percentage",
    "Housing_Cost", "Tax_Rate", "Savings_Percentage", "Savings", "Healthcare_Cost_Percentage",
    "Healthcare_Cost", "Education_Cost_Percentage", "Education_Cost", "Transportation_Cost_Percentage",
    "Transportation_Cost", "Sum_Percentage", "Sum", "Sum_Costs"
]

country_options = [
    'Australia', 'Brazil', 'Canada', 'China', 'France', 'Germany', 'India', 'Japan', 'Mexico', 'Russia', 'South Africa', 'United States'
]

selected_y_axis = st.sidebar.selectbox("Wähle die Y-Achse", y_axis_options)

fig_region = go.Figure()
if not df_region.empty:
    regions = df_region["Region"].unique()
    for region in regions:
        region_data = df_region[df_region["Region"] == region]
        fig_region.add_trace(go.Scatter(x=region_data["Year"],
                                        y=region_data[selected_y_axis],
                                        mode='lines',
                                        name=region))
    
    fig_region.update_layout(
        title=f"{selected_y_axis} by Year and Region",
        xaxis_title="Year",
        yaxis_title=selected_y_axis,
        template="plotly_dark"
    )

selected_country = st.sidebar.selectbox("Wähle ein Land", country_options)
country_data = fetch_country_data(selected_country)
df_country = convert_to_dataframe(country_data)

fig_country = go.Figure()
if not df_country.empty:
    fig_country.add_trace(go.Scatter(x=df_country["Year"],
                                     y=df_country[selected_y_axis],
                                     mode='lines',
                                     name=selected_country))
    
    fig_country.update_layout(
        title=f"{selected_y_axis} by Year for {selected_country}",
        xaxis_title="Year",
        yaxis_title=selected_y_axis,
        template="plotly_dark"
    )
    
    latest_year = df_country["Year"].max()
    latest_year_data = df_country[df_country["Year"] == latest_year]
    
    pie_columns = [
        "Average_Monthly_Income", "Net_Income", "Cost_of_Living", "Housing_Cost", "Tax_Rate",
        "Savings", "Healthcare_Cost", "Education_Cost", "Transportation_Cost"
    ]
    
    if not latest_year_data.empty:
        pie_data = latest_year_data[pie_columns].iloc[0].to_dict()
        fig_pie = go.Figure(data=[go.Pie(labels=list(pie_data.keys()), values=list(pie_data.values()), hole=0.3)])
        fig_pie.update_layout(title=f"Distribution for {latest_year} in {selected_country}", template="plotly_dark")
    
        col1, col2 = st.columns([1, 1])
        with col1:
            st.plotly_chart(fig_country)
        with col2:
            st.plotly_chart(fig_region)
            st.plotly_chart(fig_pie)
