import streamlit as st
import plotly.graph_objects as go
import pandas as pd

from api_fetcher import fetch_recommendation_data, fetch_countries, fetch_regions

colors = {
    "Housing Cost": "#984ea3",
    "Healthcare Cost": "#ff7f00",
    "Education Cost": "#a65628",
    "Transportation Cost": "#e41a1c",
    "Net Income": "#377eb8",
    "Gross Income": "#4daf4a"
}


def create_stacked_bar_chart(data):
    df = pd.DataFrame(data)
    # Sortierung nach Country, Year und Category
    df = df.sort_values(by=['Country', 'Year'])

    fig = go.Figure()

    country_names = get_country_name_list(data)

    years = df['Year'].unique()
    width = 0.2  # schmalere Balken für bessere Übersicht
    gap_between_groups = 0.07  # größerer Abstand zwischen den Gruppen
    gap_within_group = 0.03   # kleinerer Abstand innerhalb der Gruppen

    position = 0  # Positionstracker für die Balken
    x_labels = []  # Liste für die Beschriftungen der x-Achse
    x_positions = []  # Numerische Positionen für die Balken

    for country in country_names:
        # Abstand zwischen den Ländern
        position += 0.3

        for year in sorted(years):
            year_data = df[(df['Country'] == country) & (df['Year'] == year)]
            if year_data.empty:
                continue

            # Balken in 3er-Gruppen (Costs, Income, Net Income)
            categories = ['Costs', 'Income']

            for category in categories:
                label = f"{country_names.index(country) + 1} - {year}"

                x_labels.append(label)
                x_positions.append(position)

                if category == 'Costs':
                    fig.add_trace(go.Bar(
                        x=[position],
                        y=year_data['Housing_Cost'],
                        name='Housing Cost',
                        marker=dict(color=colors["Housing Cost"]),
                        width=width,
                        hovertemplate=f"<span style='color:{colors["Housing Cost"]};'>Housing Cost</span><br>{year_data['Housing_Cost'].values[0]:.2f}</span><extra></extra>"
                    ))

                    fig.add_trace(go.Bar(
                        x=[position],
                        y=year_data['Healthcare_Cost'],
                        name='Healthcare Cost',
                        marker=dict(color=colors["Healthcare Cost"]),
                        base=year_data['Housing_Cost'],
                        width=width,
                        hovertemplate=f"""<span style='color:{colors["Healthcare Cost"]};'>Healthcare Cost</span>
                            <br>{year_data['Healthcare_Cost'].values[0]:.2f}</span>
                            <br><span style='color:{colors["Healthcare Cost"]};'>Total</span>
                            <br>{(year_data['Healthcare_Cost']+year_data['Housing_Cost']).values[0]:.2f}</span><extra></extra>
                        """
                    ))

                    current_costs = year_data['Housing_Cost'] + \
                        year_data['Healthcare_Cost']

                    fig.add_trace(go.Bar(
                        x=[position],
                        y=year_data['Education_Cost'],
                        name='Education Cost',
                        marker=dict(color=colors["Education Cost"]),
                        base=current_costs,
                        width=width,
                        hovertemplate=f"""<span style='color:{colors["Education Cost"]};'>Education Cost</span>
                            <br>{year_data['Education_Cost'].values[0]:.2f}</span>
                            <br><span style='color:{colors["Education Cost"]};'>Total</span>
                            <br>{(year_data['Education_Cost']+current_costs).values[0]:.2f}</span><extra></extra>
                        """
                    ))

                    current_costs += year_data['Education_Cost']

                    fig.add_trace(go.Bar(
                        x=[position],
                        y=year_data['Transportation_Cost'],
                        name='Transportation Cost',
                        marker=dict(color=colors["Transportation Cost"]),
                        base=current_costs,
                        width=width,
                        hovertemplate=f"""<span style='color:{colors["Transportation Cost"]};'>Transportation Cost</span>
                            <br>{year_data['Transportation_Cost'].values[0]:.2f}</span>
                            <br><span style='color:{colors["Transportation Cost"]};'>Total</span>
                            <br>{(year_data['Transportation_Cost']+current_costs).values[0]:.2f}</span><extra></extra>
                        """
                    ))

                    current_costs += year_data['Transportation_Cost']
                else:
                    # fig.add_trace(go.Bar(
                    #    x=[position],
                    #    y=current_costs,
                    #    name='Net Income',
                    #    marker=dict(color=colors[4]),
                    #    width=width,
                    #    hovertemplate=f"<span style='color:{colors[4]};'>Total Costs</span><br>{current_costs.values[0]:.2f}</span><extra></extra>"
                    # ))

                    fig.add_trace(go.Bar(
                        x=[position],
                        y=year_data['Net_Income'],  # - current_costs,
                        name='Net Income',
                        marker=dict(color=colors["Net Income"]),
                        width=width,
                        hovertemplate=f"""<span style='color:{colors["Net Income"]};'>Net Income</span>
                            <br>{year_data['Net_Income'].values[0]:.2f}
                            <br><span style='color:{colors["Net Income"]};'>Disposable income</span>
                            <br>{(year_data['Net_Income']-current_costs).values[0]:.2f}</span><extra></extra>
                        """
                    ))

                    fig.add_trace(go.Bar(
                        x=[position],
                        y=year_data['Average_Monthly_Income'] -
                        year_data['Net_Income'],
                        name='Gross Income',
                        marker=dict(color=colors["Gross Income"]),
                        width=width,
                        hovertemplate=f"""<span style='color:{colors["Gross Income"]};'>Gross Income</span>
                            <br>{year_data['Average_Monthly_Income'].values[0]:.2f}
                            <br><span style='color:{colors["Gross Income"]};'>Tax</span>
                            <br>{(year_data['Average_Monthly_Income']-year_data['Net_Income']).values[0]:.2f}</span><extra></extra>
                        """
                    ))

                # Abstand zwischen Balken derselben Gruppe
                position += gap_within_group + width

            # Größerer Abstand nach jeder 3er-Gruppe
            position += gap_between_groups

    fig.update_layout(
        barmode='stack',
        title='Stacked Bar Chart of Costs, Average Income, and Net Income by Country, Year, and Category',
        xaxis_title='Country - Year',
        yaxis_title='Amount in $',
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


st.sidebar.title("Demographics")
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

st.sidebar.title("Preferences")
region = st.sidebar.selectbox(
    "Desired Region", [None] + fetch_regions(), index=0,
    help="Region of most interest.")
extra_country = st.sidebar.selectbox(
    "Comparison Country", [None] + fetch_countries(), index=0,
    help="Add an extra country for comparison.")
years = st.sidebar.number_input(
    "Years", min_value=1.0, value=3.0, max_value=5.0, step=1.0,
    format="%.0f",
    help="Number of Years to look at.")


def get_country_name_list(
        data: dict
) -> list:
    """
        _summary_

    :param data: _description_

    :return: _description_
    """

    countries = []

    for row in data:
        if row["Country"] not in countries:
            countries.append(row["Country"])

    return countries


st.title("Recommendations")

# Validierung der Eingabe
if education_multiplicator > healthcare_multiplicator or income_multiplicator > healthcare_multiplicator:
    st.warning(
        "Education and Income Multiplicator must be smaller or equal to Healthcare Multiplicator")
else:
    data = fetch_recommendation_data(
        extra_country, healthcare_multiplicator, education_multiplicator, income_multiplicator, region, 2023 - (years - 1))
    if data:
        col1, col2 = st.columns([3, 1])

        with col1:
            create_stacked_bar_chart(data)

        with col2:
            st.markdown("### Legend")
            st.text(
                "List of recommended countries based on your preferences and demografic data."
            )

            recommendations = "\n".join(
                [f"{i + 1}. {country}" for i, country in enumerate(get_country_name_list(data))])

            st.markdown(recommendations)

            # Colored legend
            st.markdown("#### Color Meaning")

            # TODO auf kategorie kosten und einkommen anpassen
            for label, color in colors.items():
                st.markdown(
                    f"<div style='display: flex; align-items: center;'>"
                    f"<div style='width: 15px; height: 15px; background-color: {color}; margin-right: 10px;'></div>"
                    f"<span>{label}</span>"
                    f"</div>",
                    unsafe_allow_html=True
                )

            st.info(
                "INFO")
