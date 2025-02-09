from typing import List

import requests
import streamlit as st

# Eingeführt durch Esrom Johannes und ergänzt durch Davide Pedergnana
@st.cache_data
def fetch_recommendation_data(
    number_people: int,
    number_students: int,
    number_workforce: int,
    extra_country: str,
    start_year: int,
    region: str
) -> List[dict]:
    """
        Ruft die Empfehlungen für die Top 3 Länder ab.

    :param number_people: Anzahl der Personen
    :param number_students: Anzahl der Studenten/Schüler
    :param number_workforce: Anzahl der Berufstätigen (1 = Vollzeit, 0.5 = Teilzeit)
    :param extra_country: Zusätzliches Land
    :param start_year: Startjahr
    :param region: Regionsfilter

    :return: Liste der Top 3(+1) Länder
    """

    url = f"http://localhost:8000/recommended-countries?number_people={number_people}&number_students={number_students}&number_workforce={number_workforce}&start_year={start_year}"
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
    """
        Ruft alle Länder ab

    :return: Die Liste aller Länder
    """

    url = f"http://localhost:8000/countries"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error fetching country details")
        return {}


@st.cache_data
def fetch_regions() -> list:
    """
        Ruft alle Regionen ab

    :return: Die Liste aller Regionen
    """

    url = f"http://localhost:8000/regions"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error fetching region details")
        return {}


@st.cache_data
def fetch_region_data() -> dict:
    """
        Ruft die Daten für alle Regionen ab

    :return: Die Daten für alle Regionen
    """

    response = requests.get('http://localhost:8000/region-information')
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error fetching data.")
        return {}


@st.cache_data
def fetch_country_data(
    country: str
) -> dict:
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
