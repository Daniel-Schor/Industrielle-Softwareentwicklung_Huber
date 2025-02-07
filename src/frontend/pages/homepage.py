import streamlit as st
import plotly.graph_objects as go

from api_fetcher import fetch_region_data, convert_to_dataframe


region_data = fetch_region_data()

df_region = convert_to_dataframe(region_data)

options = {
    "Average Monthly Income": "Average_Monthly_Income",
    "Net Income": "Net_Income",
    "Housing Cost": "Housing_Cost",
    "Tax Rate": "Tax_Rate",
    "Savings": "Savings",
    "Healthcare Cost": "Healthcare_Cost",
    "Education Cost": "Education_Cost",
    "Transportation Cost": "Transportation_Cost",
    "Sum": "Sum"
}
selected_y_axis = st.sidebar.selectbox("y-axis for region", options.keys())

# TODO
st.title("Problemstatement")
st.text("""
        Menschen, die einen mittel- bis langfristigen Aufenthalt im Ausland planen für z.B. Work and Travel, ein Studium oder für eine Auswanderung, haben das Problem, realistische Kosten- und Einkommensprognosen für ihr Zielland zu erstellen. Wichtige Informationen zu den Lebenshaltungskosten, Wohnkosten, Gesundheitsausgaben, Bildungskosten, Transportkosten sowie den dazugehörigen durchschnittlichen Einkommensverhältnissen und Steuersätzen sind oft unübersichtlich, intransparent oder schwer zu vergleichen. Basierend auf genannten Daten aus über 10 Ländern soll unser Tool mit individuellen Angaben des Verbrauchers aufzeigen, welche Länder für den möglichen Abschnittswechel die besten Voraussetzungen bieten.
        """)


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

# TODO
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
