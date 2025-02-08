import pandas as pd
import streamlit as st
import plotly.graph_objects as go

from api_fetcher import fetch_recommendation_data, fetch_countries, fetch_regions
from helper import get_country_name_list

# ----------------------------- Constanten/Variablen -----------------------------
# Farben für die Bars
_COLORS = {
    "Housing Cost": "#984ea3",
    "Healthcare Cost": "#ff7f00",
    "Education Cost": "#a65628",
    "Transportation Cost": "#e41a1c",
    "Net Income": "#377eb8",
    "Gross Income": "#4daf4a"
}

# Um später das disposable income zu speichern
_country_disposable_income = {}

# ----------------------------- Charts -----------------------------


def create_stacked_bar_chart(
        data: list[dict]
) -> None:
    """
        Erstellt ein gestapeltes Balkendiagramm, das die Entwicklung der Kosten und Einkommen über die Jahre für jedes Land anzeigt.

    :param data: Die Daten als Liste von Dictionaries, die vom Backend geliefert werden.
    """

    df = pd.DataFrame(data)

    fig = go.Figure()

    country_names = get_country_name_list(data)

    years = df['Year'].unique()

    # -- Definition --
    # Balkenbreite
    width = 0.2
    # Abstand außerhalb der Gruppen
    gap_between_groups = 0.07
    # Abstand innerhalb der Gruppen
    gap_within_group = 0.03

    # Positionstracker für die Balken
    position = 0
    x_labels = []
    x_positions = []

    # -- Durchlaufen der Länder --
    for current_country in country_names:
        # Abstand zwischen den Ländern
        position += 0.3

        # -- Durchlaufen der Jahre --
        for year in sorted(years):

            year_data = df[(df['Country'] == current_country)
                           & (df['Year'] == year)]
            if year_data.empty:
                continue

            # -- Durchlaufen der Balkenarten --
            categories = ['Costs', 'Income']

            for category in categories:
                label = f"{year}<br>{country_names.index(current_country) + 1}"

                x_labels.append(label)
                x_positions.append(position)

                # -- Costs Balken --
                if category == 'Costs':
                    # Housing Cost
                    fig.add_trace(go.Bar(
                        x=[position],
                        y=year_data['Housing_Cost'],
                        name='Housing Cost',
                        marker=dict(color=_COLORS["Housing Cost"]),
                        width=width,
                        hovertemplate=f"<span style='color:{_COLORS["Housing Cost"]};'>Housing Cost</span><br>{year_data['Housing_Cost'].values[0]:.2f}</span><extra></extra>"
                    ))

                    # Healthcare Cost
                    fig.add_trace(go.Bar(
                        x=[position],
                        y=year_data['Healthcare_Cost'],
                        name='Healthcare Cost',
                        marker=dict(color=_COLORS["Healthcare Cost"]),
                        base=year_data['Housing_Cost'],
                        width=width,
                        hovertemplate=f"""<span style='color:{_COLORS["Healthcare Cost"]};'>Healthcare Cost</span>
                            <br>{year_data['Healthcare_Cost'].values[0]:.2f}</span>
                            <br><span style='color:{_COLORS["Healthcare Cost"]};'>Total</span>
                            <br>{(year_data['Healthcare_Cost']+year_data['Housing_Cost']).values[0]:.2f}</span><extra></extra>
                        """
                    ))

                    # Summe der bisherigen Kosten
                    current_costs = year_data['Housing_Cost'] + \
                        year_data['Healthcare_Cost']

                    # Education Cost
                    fig.add_trace(go.Bar(
                        x=[position],
                        y=year_data['Education_Cost'],
                        name='Education Cost',
                        marker=dict(color=_COLORS["Education Cost"]),
                        base=current_costs,
                        width=width,
                        hovertemplate=f"""<span style='color:{_COLORS["Education Cost"]};'>Education Cost</span>
                            <br>{year_data['Education_Cost'].values[0]:.2f}</span>
                            <br><span style='color:{_COLORS["Education Cost"]};'>Total</span>
                            <br>{(year_data['Education_Cost']+current_costs).values[0]:.2f}</span><extra></extra>
                        """
                    ))

                    # Summe der bisherigen Kosten aktualisieren
                    current_costs += year_data['Education_Cost']

                    # Transportation Cost
                    fig.add_trace(go.Bar(
                        x=[position],
                        y=year_data['Transportation_Cost'],
                        name='Transportation Cost',
                        marker=dict(color=_COLORS["Transportation Cost"]),
                        base=current_costs,
                        width=width,
                        hovertemplate=f"""<span style='color:{_COLORS["Transportation Cost"]};'>Transportation Cost</span>
                            <br>{year_data['Transportation_Cost'].values[0]:.2f}</span>
                            <br><span style='color:{_COLORS["Transportation Cost"]};'>Total</span>
                            <br>{(year_data['Transportation_Cost']+current_costs).values[0]:.2f}</span><extra></extra>
                        """
                    ))

                    # Summe der bisherigen Kosten aktualisieren
                    current_costs += year_data['Transportation_Cost']

                # -- Income Balken --
                elif category == 'Income':
                    # Speichern des disposable incomes für die spätere Anzeige
                    if (year_data['Year'] == 2023).values[0]:
                        _country_disposable_income[current_country] = (
                            year_data['Net_Income']-current_costs).values[0]

                    # Nettoeinkommen
                    fig.add_trace(go.Bar(
                        x=[position],
                        y=year_data['Net_Income'],
                        name='Net Income',
                        marker=dict(color=_COLORS["Net Income"]),
                        width=width,
                        hovertemplate=f"""<span style='color:{_COLORS["Net Income"]};'>Net Income</span>
                            <br>{year_data['Net_Income'].values[0]:.2f}
                            <br><span style='color:{_COLORS["Net Income"]};'>Disposable income</span>
                            <br>{(year_data['Net_Income']-current_costs).values[0]:.2f}</span><extra></extra>
                        """
                    ))

                    # Bruttoeinkommen
                    fig.add_trace(go.Bar(
                        x=[position],
                        y=year_data['Average_Monthly_Income'] -
                        year_data['Net_Income'],
                        name='Gross Income',
                        marker=dict(color=_COLORS["Gross Income"]),
                        width=width,
                        hovertemplate=f"""<span style='color:{_COLORS["Gross Income"]};'>Gross Income</span>
                            <br>{year_data['Average_Monthly_Income'].values[0]:.2f}
                            <br><span style='color:{_COLORS["Gross Income"]};'>Tax</span>
                            <br>{(year_data['Average_Monthly_Income']-year_data['Net_Income']).values[0]:.2f}</span><extra></extra>
                        """
                    ))

                # Abstand Balken innerhalb einer Gruppe
                position += gap_within_group + width

            # Abstand von Gruppen
            position += gap_between_groups

    # Anpassen der x-Achse
    new_x_positions = []
    new_x_labels = []
    for i in range(0, len(x_positions)-1, 2):
        new_x_positions.append((x_positions[i] + x_positions[i+1]) / 2)
        new_x_labels.append(x_labels[i].split("<br>")[0])

    # Position für die Ländernamen
    for index, i in enumerate(range(0, len(new_x_positions), len(years))):
        avg_pos = sum(new_x_positions[i:i + len(years)]) / len(years)

        new_x_positions.append(avg_pos - 0.001)

        country_name = f"{index + 1}. {country_names[index]}"

        new_x_labels.append(f"<br>{country_name}")

    # -- Layout --
    fig.update_layout(
        barmode='stack',
        title='Development of Costs and Income',
        # xaxis_title='Country - Year',
        yaxis_title='Amount in $',
        showlegend=False,
        height=800,
        width=1200,
        xaxis=dict(
            tickvals=new_x_positions,
            ticktext=new_x_labels,
        )
    )

    st.plotly_chart(fig)


# ----------------------------- Aufbau -----------------------------
# ---- Sidebar ----
st.sidebar.title("Demographics")

number_people = st.sidebar.number_input(
    "People",
    min_value=0.0,
    step=1.0,
    value=1.0,
    format="%.0f",
    help="Number of people in the household."
)

number_students = st.sidebar.number_input(
    "Students",
    min_value=0.0,
    max_value=number_people,
    step=1.0,
    value=1.0,
    format="%.0f",
    help="Number of students in the household. Cannot be higher than the number of people in the household."
)

number_workforce = st.sidebar.number_input(
    "Workforce",
    min_value=0.0,
    max_value=number_people,
    step=0.5,
    value=1.0,
    format="%.1f",
    help="Number of people working in the Houshold (1 = Full time, 0.5 = Half time)."
)

st.sidebar.title("Preferences")
region = st.sidebar.selectbox(
    "Preferred Region",
    [None] + fetch_regions(),
    index=0,
    help="Region of most interest."
)
extra_country = st.sidebar.selectbox(
    "Comparison Country",
    [None] + fetch_countries(),
    index=0,
    help="Add an extra country for comparison."
)
years = st.sidebar.number_input(
    "Years",
    min_value=1.0,
    max_value=5.0,
    step=1.0,
    value=3.0,
    format="%.0f",
    help="Number of Years to look at."
)

# ---- Titel ----
st.title("Top Matches")

# ---- Data fetching ----

data = fetch_recommendation_data(
    number_people=number_people,
    number_students=number_students,
    number_workforce=number_workforce,
    extra_country=extra_country,
    start_year=2023 - (years - 1),
    region=region
)

if not data:
    st.error("No data available for the selected parameters.")
    st.stop()

# ---- Spalten definition ----

col1, col2 = st.columns([3, 1])

# ---- 1. Spalte - Balkendiagramm ----
with col1:
    create_stacked_bar_chart(data)

# ---- 2. Spalte - Beschreibung, Legende, etc. ----
with col2:
    # ---- Beschreibung ----
    st.markdown("## Summary")

    st.text("Based on your preferences and household details, \
            we have identified the following countries that best \
            match your criteria. These recommendations are ranked \
            by the disposable income available in 2023 after deducting \
            housing, healthcare, education, and transportation costs from \
            the net income. The diagram illustrates the changes over the \
            past years. The countries listed below offer the best balance \
            between income and essential expenses, maximizing your savings \
            potential.")

    recommendations = "\n".join(
        [f"{i + 1}. {country} | {_country_disposable_income[country]:.2f}$" for i,
            country in enumerate(get_country_name_list(data))]
    )

    # ---- Top Matches ----
    st.markdown(f"### Top Matches")
    st.markdown(recommendations)

    # ---- Legende ----
    legend_categories = {
        "Costs": [
            "Transportation Cost",
            "Education Cost",
            "Healthcare Cost",
            "Housing Cost"
        ],
        "Income": [
            "Gross Income",
            "Net Income"
        ]
    }

    st.markdown("### Data Categories")
    for category, items in legend_categories.items():
        st.markdown(
            f"<div style='margin-bottom: 5px; margin-top: 10px; font-weight: bold;'>{category}</div>",
            unsafe_allow_html=True
        )
        for label in items:
            color = _COLORS[label]
            st.markdown(
                f"""
                <div style='display: flex; align-items: center; margin-bottom: 3px;'>
                    <div style='width: 15px; height: 15px; background-color: {color}; margin-right: 10px; border-radius: 2px;'></div>
                    <span style='font-size: 14px;'>{label}</span>
                </div>
                """,
                unsafe_allow_html=True
            )
