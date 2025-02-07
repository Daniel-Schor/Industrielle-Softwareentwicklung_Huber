import pandas as pd
import requests
import streamlit as st


@st.cache_data
def fetch_recommendation_data(extra_country: str, healthcare_multiplicator: int, education_multiplicator: int, income_multiplicator: int, region: str, start_year: int = 2021) -> dict:
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
