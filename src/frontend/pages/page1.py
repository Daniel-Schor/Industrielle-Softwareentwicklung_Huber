import streamlit as st
import requests
import plotly.graph_objects as go
import pandas as pd


@st.cache_data
def fetch_recommendation_data(extra_country: str, healthcare_multiplicator: int, education_multiplicator: int, income_multiplicator: int, region: str) -> dict:
    start_year = 2021

    url = f"http://localhost:8000/recommended-countries?healthcare_multiplicator={healthcare_multiplicator}&education_multiplicator={education_multiplicator}&income_multiplicator={income_multiplicator}&start_year={start_year}"
    if extra_country:
        url += f"&extra_country={extra_country}"
    if region:
        url += f"&region={region}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error fetching country details")
        return {}


@st.cache_data
def fetch_countries() -> list:

    url = f"http://localhost:8000/countries"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error fetching country details")
        return {}


@st.cache_data
def fetch_regions() -> list:

    url = f"http://localhost:8000/regions"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error fetching region details")
        return {}


def create_stacked_bar_chart(data):
    df = pd.DataFrame(data)
    df = df.sort_values(by=['Country', 'Year'])  # Sortierung nach Country, Year und Category

    fig = go.Figure()

    countries = df['Country'].unique()
    years = df['Year'].unique()
    width = 0.2  # schmalere Balken für bessere Übersicht
    gap_between_groups = 0.6  # größerer Abstand zwischen den Gruppen
    gap_within_group = 0.05   # kleinerer Abstand innerhalb der Gruppen

    colors = ['#984ea3', '#ff7f00', '#a65628', '#e41a1c', '#377eb8', '#4daf4a']

    position = 0  # Positionstracker für die Balken
    x_labels = []  # Liste für die Beschriftungen der x-Achse
    x_positions = []  # Numerische Positionen für die Balken

    for country in sorted(countries):
        for year in sorted(years):
            year_data = df[(df['Country'] == country) & (df['Year'] == year)]
            if year_data.empty:
                continue

            # Balken in 3er-Gruppen (Costs, Income, Net Income)
            categories = ['Costs', 'Income', 'Net Income']

            for i, category in enumerate(categories):
                label = f"{country} - {year} - {category}"
                x_labels.append(label)
                x_positions.append(position)

                if category == 'Costs':
                    fig.add_trace(go.Bar(
                        x=[position],
                        y=year_data['Housing_Cost'],
                        name='Housing Cost',
                        marker=dict(color=colors[0]),
                        width=width,
                        hovertemplate=f"<span style='color:{colors[0]};'>Housing Cost</span><br>{year_data['Housing_Cost'].values[0]:.2f}</span><extra></extra>"
                    ))

                    fig.add_trace(go.Bar(
                        x=[position],
                        y=year_data['Healthcare_Cost'],
                        name='Healthcare Cost',
                        marker=dict(color=colors[1]),
                        base=year_data['Housing_Cost'],
                        width=width,
                        hovertemplate=f"<span style='color:{colors[1]};'>Healthcare Cost</span><br>{year_data['Healthcare_Cost'].values[0]:.2f}</span><extra></extra>"
                    ))

                    fig.add_trace(go.Bar(
                        x=[position],
                        y=year_data['Education_Cost'],
                        name='Education Cost',
                        marker=dict(color=colors[2]),
                        base=year_data['Housing_Cost'] + year_data['Healthcare_Cost'],
                        width=width,
                        hovertemplate=f"<span style='color:{colors[2]};'>Education Cost</span><br>{year_data['Education_Cost'].values[0]:.2f}</span><extra></extra>"
                    ))

                    fig.add_trace(go.Bar(
                        x=[position],
                        y=year_data['Transportation_Cost'],
                        name='Transportation Cost',
                        marker=dict(color=colors[3]),
                        base=year_data['Housing_Cost'] + year_data['Healthcare_Cost'] + year_data['Education_Cost'],
                        width=width,
                        hovertemplate=f"<span style='color:{colors[3]};'>Transportation Cost</span><br>{year_data['Transportation_Cost'].values[0]:.2f}</span><extra></extra>"
                    ))
                elif category == 'Income':
                    fig.add_trace(go.Bar(
                        x=[position],
                        y=year_data['Average_Monthly_Income'],
                        name='Average Monthly Income',
                        marker=dict(color=colors[4]),
                        width=width,
                        hovertemplate=f"<span style='color:{colors[4]};'>Average Monthly Income</span><br>{year_data['Average_Monthly_Income'].values[0]:.2f}</span><extra></extra>"
                    ))
                else:  # Net Income
                    fig.add_trace(go.Bar(
                        x=[position],
                        y=year_data['Net_Income'],
                        name='Net Income',
                        marker=dict(color=colors[5]),
                        width=width,
                        hovertemplate=f"<span style='color:{colors[5]};'>Net Income</span><br>{year_data['Net_Income'].values[0]:.2f}</span><extra></extra>"
                    ))

                # Abstand zwischen Balken derselben Gruppe
                position += gap_within_group + width

            # Größerer Abstand nach jeder 3er-Gruppe
            position += gap_between_groups

    fig.update_layout(
        barmode='stack',
        title='Stacked Bar Chart of Costs, Average Income, and Net Income by Country, Year, and Category',
        xaxis_title='Country - Year - Category',
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


healthcare_multiplicator = st.sidebar.number_input(
    "People", min_value=0.0, value=1.0, step=1.0,
    format="%.0f",
    help="Number of people in the household.")
education_multiplicator = st.sidebar.number_input(
    "Students", min_value=0.0, max_value=healthcare_multiplicator, value=1.0, step=1.0,
    format="%.0f",
    help="Number of students in the household. Cannot be higher than the number of people in the household.")
income_multiplicator = st.sidebar.number_input(
    "Workforce", min_value=0.0, max_value=healthcare_multiplicator, value=1.0, step=0.5,
    format="%.1f",
    help="Number of people working in the Houshold (1 = Full time, 0.5 = Half time).")
region = st.sidebar.selectbox(
    "Desired Region", [None] + fetch_regions(), index=0,
    help="Region of most interest.")
extra_country = st.sidebar.selectbox(
    "Comparison Country", [None] + fetch_countries(), index=0,
    help="Add an extra country for comparison.")

# Validierung der Eingabe
if education_multiplicator > healthcare_multiplicator or income_multiplicator > healthcare_multiplicator:
    st.warning(
        "Education and Income Multiplicator must be smaller or equal to Healthcare Multiplicator")
else:
    data = fetch_recommendation_data(
        extra_country, healthcare_multiplicator, education_multiplicator, income_multiplicator, region)
    if data:
        create_stacked_bar_chart(data)
