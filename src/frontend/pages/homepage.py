import streamlit as st
import requests
import plotly.graph_objects as go
import pandas as pd

from api_fetcher import fetch_region_data


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
    "Average_Monthly_Income", "Net_Income",
    "Housing_Cost", "Tax_Rate", "Savings",
    "Healthcare_Cost",  "Education_Cost",
    "Transportation_Cost", "Sum"
]

selected_y_axis = st.sidebar.selectbox("y-axis for region", y_axis_options)

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

st.plotly_chart(fig_region)
