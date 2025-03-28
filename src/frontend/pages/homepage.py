import streamlit as st
import plotly.graph_objects as go

from api_fetcher import fetch_region_data
from helper import convert_to_dataframe

_df_region = convert_to_dataframe(fetch_region_data())

# Esrom.J | Daniel.S | Mavin-M.S | Davide.P

# -- Sidebar --
_numerical_columns = [
    col for col in _df_region.select_dtypes(include=["number"]).columns if col != "Year"
]

_options = {col.replace("_", " ").title(): col for col in _numerical_columns}

_selected_y_axis = st.sidebar.selectbox(
    "Metric Selection",
    _options.keys(),
    help="Select the metric you want to analyze and compare the Regions with."
)

# -- Header --
st.title("MoveSmart")

st.text("Whether you're planning a long-term stay abroad, considering a move \
        to another country, or simply curious about the financial conditions \
        in different parts of the world, our platform provides the tools you \
        need to make informed decisions. With our user-friendly dashboard, you \
        can analyze cost and income ratios worldwide, find the ideal country for \
        your needs, and gain detailed insights into the financial conditions of \
        your desired destinations. Our data-driven and personalized solution \
        helps you create realistic forecasts, compare countries effortlessly, \
        and make the best choice for your future. Whether you're traveling solo, \
        with a group, or planning to start a family abroad, we’re here to help \
        you navigate the financial challenges of living in a new country.")


# -- Chart --
fig_region = go.Figure()
if not _df_region.empty:
    regions = _df_region["Region"].unique()
    for region in regions:
        region_data = _df_region[_df_region["Region"] == region]
        fig_region.add_trace(go.Scatter(
            x=region_data["Year"],
            y=region_data[_options[_selected_y_axis]],
            mode='lines',
            name=region
        ))

    unique_years = sorted(_df_region["Year"].unique())

    fig_region.update_layout(
        title=f"<span>Overview of <u>{_selected_y_axis}</u> by Regions per year</span>",
        xaxis_title="Year",
        yaxis_title=_selected_y_axis,
        template="plotly_dark",
        height=520,
        xaxis=dict(
            tickmode='array',
            tickvals=unique_years,
            tickformat=".0f"
        )
    )

st.plotly_chart(fig_region)

# -- Footer --
st.markdown(
    """
        <p style='text-align: center; color: gray; font-size: 0.8em;'>
            Created by Team 6<br>
            Industrielle Softwareentwicklung - Huber<br>
            Frankfurt University of Applied Sciences<br>
            Esrom J. | Daniel S. | Mavin-M. S. | Davide P.
        </p>
    """,
    unsafe_allow_html=True
)
