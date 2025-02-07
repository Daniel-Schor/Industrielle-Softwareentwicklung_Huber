import streamlit as st
import requests
import plotly.graph_objects as go
import pandas as pd

country_options = [
    'Australia', 'Brazil', 'Canada', 'China', 'France', 'Germany', 'India', 'Japan', 'Mexico', 'Russia', 'South Africa', 'United States'
]

@st.cache_data
def fetch_recommendation_data(extra_country: str, healthcare_multiplicator: float, education_multiplicator: float, income_multiplicator: float) -> dict:
    start_year = 2021

    url = f"http://localhost:8000/recommended-countries?healthcare_multiplicator={healthcare_multiplicator}&education_multiplicator={education_multiplicator}&income_multiplicator={income_multiplicator}&extra_country={extra_country}&start_year={start_year}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error fetching country details")
        return {}

def create_stacked_bar_chart(data):
    df = pd.DataFrame(data)

    fig = go.Figure()

    countries = df['Country'].unique()
    years = df['Year'].unique()
    width = 0.2  # schmalere Balken für bessere Übersicht
    gap_between_groups = 0.6  # größerer Abstand zwischen den Gruppen
    gap_within_group = 0.05   # kleinerer Abstand innerhalb der Gruppen

    position = 0  # Positionstracker für die Balken
    x_labels = []  # Liste für die Beschriftungen der x-Achse
    x_positions = []  # Numerische Positionen für die Balken

    for year in sorted(years):
        for country in countries:
            year_data = df[(df['Country'] == country) & (df['Year'] == year)]
            if year_data.empty:
                continue

            # Balken in 3er-Gruppen (Costs, Income, Net Income)
            categories = ['Costs', 'Income', 'Net Income']

            for i, category in enumerate(categories):
                label = f"{year} - {country} - {category}"
                x_labels.append(label)
                x_positions.append(position)

                if category == 'Costs':
                    fig.add_trace(go.Bar(
                        x=[position],
                        y=year_data['Housing_Cost'],
                        name='Housing Cost',
                        marker=dict(color='blue'),
                        width=width
                    ))

                    fig.add_trace(go.Bar(
                        x=[position],
                        y=year_data['Healthcare_Cost'],
                        name='Healthcare Cost',
                        marker=dict(color='green'),
                        base=year_data['Housing_Cost'],
                        width=width
                    ))

                    fig.add_trace(go.Bar(
                        x=[position],
                        y=year_data['Education_Cost'],
                        name='Education Cost',
                        marker=dict(color='orange'),
                        base=year_data['Housing_Cost'] + year_data['Healthcare_Cost'],
                        width=width
                    ))

                    fig.add_trace(go.Bar(
                        x=[position],
                        y=year_data['Transportation_Cost'],
                        name='Transportation Cost',
                        marker=dict(color='red'),
                        base=year_data['Housing_Cost'] + year_data['Healthcare_Cost'] + year_data['Education_Cost'],
                        width=width
                    ))
                elif category == 'Income':
                    fig.add_trace(go.Bar(
                        x=[position],
                        y=year_data['Average_Monthly_Income'],
                        name='Average Monthly Income',
                        marker=dict(color='purple'),
                        width=width
                    ))
                else:  # Net Income
                    fig.add_trace(go.Bar(
                        x=[position],
                        y=year_data['Net_Income'],
                        name='Net Income',
                        marker=dict(color='cyan'),
                        width=width
                    ))

                # Abstand zwischen Balken derselben Gruppe
                position += gap_within_group + width

            # Größerer Abstand nach jeder 3er-Gruppe
            position += gap_between_groups

    fig.update_layout(
        barmode='stack',
        title='Stacked Bar Chart of Costs, Average Income, and Net Income by Year, Country, and Category',
        xaxis_title='Year - Country - Category',
        yaxis_title='Amount ($)',
        showlegend=False,  # Legende ausblenden
        height=800,        # Erhöht die Höhe des Diagramms
        width=1200,        # Erweitert die Breite des Diagramms
        xaxis=dict(
            tickangle=-90,  # Vertikale Beschriftung
            tickvals=x_positions,  # Positionen für die Ticks
            ticktext=x_labels       # Beschriftung der Ticks
        )
    )

    st.plotly_chart(fig)


st.title("Stacked Bar Chart Visualization")
extra_country = st.sidebar.selectbox("Select Extra Country", country_options, index=country_options.index("Germany"))
healthcare_multiplicator = st.sidebar.number_input("Healthcare Multiplicator", min_value=0.0, value=1.0, step=0.1)
education_multiplicator = st.sidebar.number_input("Education Multiplicator", min_value=0.0, value=1.0, step=0.1)
income_multiplicator = st.sidebar.number_input("Income Multiplicator", min_value=0.0, value=1.0, step=0.1)

data = fetch_recommendation_data(extra_country, healthcare_multiplicator, education_multiplicator, income_multiplicator)
if data:
    create_stacked_bar_chart(data)