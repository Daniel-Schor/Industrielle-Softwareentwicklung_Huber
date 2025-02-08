import math
import os
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import Column, Integer, String, Float, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select, distinct
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from typing import List

# Absolute path to the database file
DATABASE_PATH = os.path.join(
    os.getcwd(), 'src', 'database', 'CostOfLivingAndIncome.db'
)

# database URL to the absolute path
DATABASE_URL = f"sqlite+aiosqlite:///{DATABASE_PATH}"

# Set up the database connection
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)
Base = declarative_base()

# Define the model for your table


class CostOfLivingAndIncome(Base):
    """
        Definition der Tabelle CostOfLivingAndIncome

    """

    __tablename__ = "CostOfLivingAndIncome"

    # Country als Primärschlüssel
    Country = Column(String, primary_key=True, index=True)
    Year = Column(Integer)
    Average_Monthly_Income = Column(Float)
    Net_Income = Column(Float)
    Cost_of_Living = Column(Float)
    Housing_Cost_Percentage = Column(Float)
    Housing_Cost = Column(Float)
    Tax_Rate = Column(Float)
    Savings_Percentage = Column(Float)
    Savings = Column(Float)
    Healthcare_Cost_Percentage = Column(Float)
    Healthcare_Cost = Column(Float)
    Education_Cost_Percentage = Column(Float)
    Education_Cost = Column(Float)
    Transportation_Cost_Percentage = Column(Float)
    Transportation_Cost = Column(Float)
    Sum_Percentage = Column(Float)
    Sum = Column(Float)
    Sum_Costs = Column(Float)
    Region = Column(String)


# Initialize the router for FastAPI
router = APIRouter()

# Dependency to get the DB session


async def get_db():
    """
        Dependency um die Datenbankverbindung zu erhalten

    :yield: die Datenbankverbindung
    """

    async with SessionLocal() as session:
        yield session


@router.get("/all-information-for-region")
async def get_all_data_for_region(session: AsyncSession = Depends(get_db)) -> List[dict]:
    """
        Endpoint um alle Daten gruppiert nach Regionen abzufragen
    :returns: Das Ergebnis der Abfrage
    """
    query = select(
        CostOfLivingAndIncome.Region,
        CostOfLivingAndIncome.Year,
        func.avg(CostOfLivingAndIncome.Average_Monthly_Income).label(
            "Average_Monthly_Income"),
        func.avg(CostOfLivingAndIncome.Net_Income).label("Net_Income"),
        func.avg(CostOfLivingAndIncome.Cost_of_Living).label("Cost_of_Living"),
        func.avg(CostOfLivingAndIncome.Housing_Cost_Percentage).label(
            "Housing_Cost_Percentage"),
        func.avg(CostOfLivingAndIncome.Housing_Cost).label("Housing_Cost"),
        func.avg(CostOfLivingAndIncome.Savings).label("Savings"),
        func.avg(CostOfLivingAndIncome.Healthcare_Cost).label(
            "Healthcare_Cost"),
        func.avg(CostOfLivingAndIncome.Education_Cost).label("Education_Cost"),
        func.avg(CostOfLivingAndIncome.Transportation_Cost).label(
            "Transportation_Cost"),
        func.avg(CostOfLivingAndIncome.Sum_Costs).label("Sum_Costs"),
        func.avg(CostOfLivingAndIncome.Tax_Rate).label("Tax_Rate")
    ).group_by(CostOfLivingAndIncome.Region, CostOfLivingAndIncome.Year)

    result = await session.execute(query)
    data = result.fetchall()

    if not data:
        raise HTTPException(status_code=404, detail="No data found.")

    return [
        {key: value for key, value in row._mapping.items()}
        for row in data
    ]


@router.get("/country-information", response_model=List[dict])
async def get_country_data(
    country: str,
    start_year: int = None,
    session: AsyncSession = Depends(get_db)
):
    """
        Endpoint um alle relevanten Daten für ein bestimmtes Land abzufragen

    :param country: Das Land für das die Daten abgefragt werden sollen
    :returns: Das ergebnis der Abfrage
    """

    where = (CostOfLivingAndIncome.Country == country)
    if start_year:
        where &= (CostOfLivingAndIncome.Year >= start_year)

    query = select(
        CostOfLivingAndIncome.Country,
        CostOfLivingAndIncome.Year,
        CostOfLivingAndIncome.Average_Monthly_Income,
        CostOfLivingAndIncome.Net_Income,
        CostOfLivingAndIncome.Housing_Cost,
        CostOfLivingAndIncome.Healthcare_Cost,
        CostOfLivingAndIncome.Education_Cost,
        CostOfLivingAndIncome.Transportation_Cost,
        CostOfLivingAndIncome.Region,
        CostOfLivingAndIncome.Savings
    ).where(where)

    result = await session.execute(query)
    data = result.fetchall()

    if not data:
        raise HTTPException(
            status_code=404, detail=f"No data found for country: {country}")

    return [
        {key: value for key, value in row._mapping.items()}
        for row in data
    ]


@router.get("/regions", response_model=List[str])
async def get_regions(
    session: AsyncSession = Depends(get_db)
) -> List[str]:
    """

    :return: 
    """

    query = select(distinct(CostOfLivingAndIncome.Region))

    result = await session.execute(query)
    data = result.fetchall()

    if not data:
        raise HTTPException(
            status_code=404, detail="No data found.")

    return [row[0] for row in data]


@router.get("/countries", response_model=List[str])
async def get_countries(
    session: AsyncSession = Depends(get_db)
) -> List[str]:
    """

    :return: 
    """

    query = select(distinct(CostOfLivingAndIncome.Country))

    result = await session.execute(query)
    data = result.fetchall()

    if not data:
        raise HTTPException(
            status_code=404, detail="No data found.")

    return [row[0] for row in data]


@router.get("/recommended-countries", response_model=List[dict])
async def recommended_countries(
    healthcare_multiplicator: int = 1,
    education_multiplicator: int = 0,
    income_multiplicator: float = 1,
    extra_country: str = None,
    start_year: int = 2021,
    region: str = None,
    session: AsyncSession = Depends(get_db)
) -> List[dict]:
    """
        Überprüft anhand von verschiedenen Faktoren, 
        bei welchen Ländern für ein Leben im Ausland das meiste Geld vom Einkommen übrig bleibt.
        Ermöglicht ein weiteres Land auszuwählen, um zu sehen, wie es im Vergleich abschneidet.

        Faktoren:
        - healthcare_multiplicator
        - education_multiplicator
        - income_multiplicator

        Regionen:
        - Africa
        - Asia
        - Europe
        - North America
        - Oceania
        - South America

    :param healthcare_multiplicator: XXX
    :param education_multiplicator: XXX
    :param income_multiplicator: XXX
    :param extra_country: XXX
    :param start_year: XXX
    :param region: XXX

    :return: A list of dictionaries containing the data
    """

    if healthcare_multiplicator < 1:
        raise HTTPException(
            status_code=400, detail="Healthcare Multiplicator must be greater or equal to 1.")
    if education_multiplicator < 0 or income_multiplicator < 0:
        raise HTTPException(
            status_code=400, detail="Multiplicators must be greater than 0.")
    if education_multiplicator > healthcare_multiplicator or income_multiplicator > healthcare_multiplicator:
        raise HTTPException(
            status_code=400, detail="Education and Income Multiplicator must be smaller or equal to Healthcare Multiplicator.")

    where = (CostOfLivingAndIncome.Year >= start_year)
    if region:
        if extra_country:
            where &= ((CostOfLivingAndIncome.Region == region) |
                      (CostOfLivingAndIncome.Country == extra_country))
        else:
            where &= (CostOfLivingAndIncome.Region == region)

    query = select(
        CostOfLivingAndIncome.Country,
        CostOfLivingAndIncome.Average_Monthly_Income,
        CostOfLivingAndIncome.Net_Income,
        CostOfLivingAndIncome.Housing_Cost,
        CostOfLivingAndIncome.Tax_Rate,
        CostOfLivingAndIncome.Healthcare_Cost,
        CostOfLivingAndIncome.Education_Cost,
        CostOfLivingAndIncome.Transportation_Cost,
        CostOfLivingAndIncome.Year,
        CostOfLivingAndIncome.Region
    ).where(where)

    result = await session.execute(query)
    data = result.fetchall()

    if not data:
        raise HTTPException(
            status_code=404, detail=f"No data found for {query}.")

    selected_country = None
    all_countries = []
    for row in data:
        current_country = {
            "Country": row[0],
            "Average_Monthly_Income": row[1],
            "Net_Income": row[2],
            "Housing_Cost": row[3],
            "Tax_Rate": row[4],
            "Healthcare_Cost": row[5],
            "Education_Cost": row[6],
            "Transportation_Cost": row[7],
            "Year": row[8],
            "Region": row[9]
        }

        current_country["Average_Monthly_Income"] = current_country["Average_Monthly_Income"] * \
            income_multiplicator
        current_country["Net_Income"] = current_country["Net_Income"] * \
            income_multiplicator
        current_country["Healthcare_Cost"] = current_country["Healthcare_Cost"] * \
            healthcare_multiplicator
        # Ab 3 Leuten wird Transportation doppelt so teurer
        current_country["Transportation_Cost"] = current_country["Transportation_Cost"] * \
            1 + (math.floor(healthcare_multiplicator / 3))
        # Ab 5 Leuten wird Housing 25% teurer
        current_country["Housing_Cost"] = current_country["Housing_Cost"] * \
            1 + (math.floor(healthcare_multiplicator / 6) * 0.25)
        current_country["Education_Cost"] = current_country["Education_Cost"] * \
            education_multiplicator
        current_country["Savings"] = current_country["Net_Income"] - current_country["Housing_Cost"] - \
            current_country["Healthcare_Cost"] - current_country["Education_Cost"] - \
            current_country["Transportation_Cost"]

        if extra_country and extra_country == current_country["Country"]:
            current_country["Country"] = f'{
                current_country["Country"]} (Selected)'
            if current_country["Year"] == 2023:
                selected_country = current_country

        all_countries.append(current_country)

    # Filtert länder nach Jahr 2023
    top_countries = [x for x in all_countries if x["Year"] == 2023]

    # Sortiert die Länder nach Savings
    top_countries.sort(key=lambda x: x["Savings"], reverse=True)

    # Wählt die Top 4 Länder aus
    top_countries = top_countries[:4]
    # Wenn keins der Länder ausgewählt wurde...
    for i in top_countries:
        if i["Country"].endswith("(Selected)"):
            break
    # ...wird das letzte Land...
    else:
        # ... mit dem ausgewählten ersezt
        if selected_country:
            top_countries[-1] = selected_country
        # ... oder entfernt wenn kein Land ausgewählt wurde
        else:
            top_countries = top_countries[:3]

# TODO komplexität reduzieren!
# -- Hinzufügen der anderen Jahre --

    new_countries = top_countries.copy()

    # Dict was Country als Key hat und eine Liste von Countries als Value
    missing_country_years_sorted = {}
    for country in all_countries:
        if country["Country"] not in missing_country_years_sorted:
            missing_country_years_sorted[country["Country"]] = []
        missing_country_years_sorted[country["Country"]].append(country)

    for top_country in top_countries:
        # Sortiert die Länder nach jahr für jeden Dict eintrag und speichert diese als Liste
        previous_years = sorted(
            [c for c in missing_country_years_sorted.get(
                top_country["Country"], []) if c["Year"] != 2023],
            key=lambda x: -x["Year"]
        )

        # Sucht den Index des aktuellen Landes
        insert_index = new_countries.index(top_country) + 1
        # Fügt die Länder/Jahre in die Liste ein
        new_countries[insert_index:insert_index] = previous_years

    return new_countries
