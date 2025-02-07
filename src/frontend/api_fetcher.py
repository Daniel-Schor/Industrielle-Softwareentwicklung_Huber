import requests
import streamlit as st


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
