import streamlit as st
import plotly.graph_objects as go

from api_fetcher import fetch_region_data, convert_to_dataframe


region_data = fetch_region_data()

df_region = convert_to_dataframe(region_data)

numerical_columns = [
    col for col in df_region.select_dtypes(include=["number"]).columns if col != "Year"
]

options = {col.replace("_", " ").title(): col for col in numerical_columns}

selected_y_axis = st.sidebar.selectbox("Metric Selection", options.keys())

# TODO finish header
st.title("MoveSmart")
st.text("Whether you're planning to move abroad or are simply curious about the \
        financial conditions in other countries, our platform provides \
        a data-driven and personalized solution to help you make informed \
        decisions. With our user-friendly dashboard, you can analyze cost \
        and income ratios worldwide, find the best country for your needs, \
        and gain detailed insights into the financial conditions of your desired destinations. \
        ")


fig_region = go.Figure()
if not df_region.empty:
    regions = df_region["Region"].unique()
    for region in regions:
        region_data = df_region[df_region["Region"] == region]
        fig_region.add_trace(go.Scatter(
            x=region_data["Year"],
            y=region_data[options[selected_y_axis]],
            mode='lines',
            name=region
        ))

    unique_years = sorted(df_region["Year"].unique())

    fig_region.update_layout(
        title=f"<span>Overview of <u>{selected_y_axis}</u> by Regions per year</span>",
        xaxis_title="Year",
        yaxis_title=selected_y_axis,
        template="plotly_dark",
        xaxis=dict(
            tickmode='array',
            tickvals=unique_years,
            tickformat=".0f"
        )
    )

st.plotly_chart(fig_region)

# TODO finish footer
st.markdown(
    """
        <p style='text-align: center; color: gray; font-size: 0.8em;'>
            Created by Team 6<br>
            Industrielle Softwareentwicklung - Huber<br>
            Frankfurt University of Applied Sciences<br>
            Esrom J. - Daniel S. - Mavin M. S. - Davide P.
        </p>
    """,
    unsafe_allow_html=True
)
