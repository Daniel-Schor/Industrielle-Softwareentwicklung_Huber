import os
import re
from turtle import up, update
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Float, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
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


# OUTDATED
@router.get("/average-income")
async def get_average_monthly_income(session: AsyncSession = Depends(get_db)):
    """
        Endpoint to get Average_Monthly_Income for all Countries

    :returns: Das ergebnis der Abfrage
    """

    query = select(CostOfLivingAndIncome.Country,
                   CostOfLivingAndIncome.Average_Monthly_Income)
    result = await session.execute(query)
    data = result.fetchall()

    if not data:
        raise HTTPException(status_code=404, detail="No data found.")

    return [
        {
            "Country": row[0],
            "Average_Monthly_Income": row[1]
        }
        for row in data
    ]


# OUTDATED
@router.get("/country-information", response_model=List[dict])
async def get_country_data(
    country: str,
    session: AsyncSession = Depends(get_db)
):
    """
        Endpoint um alle Daten für ein bestimmtes Land abzufragen

    :param country: Das Land für das die Daten abgefragt werden sollen
    :returns: Das ergebnis der Abfrage
    """
    query = select(
        CostOfLivingAndIncome.Country,
        CostOfLivingAndIncome.Year,
        CostOfLivingAndIncome.Average_Monthly_Income,
        CostOfLivingAndIncome.Net_Income,
        CostOfLivingAndIncome.Cost_of_Living,
        CostOfLivingAndIncome.Housing_Cost_Percentage,
        CostOfLivingAndIncome.Housing_Cost,
        CostOfLivingAndIncome.Tax_Rate,
        CostOfLivingAndIncome.Savings_Percentage,
        CostOfLivingAndIncome.Savings,
        CostOfLivingAndIncome.Healthcare_Cost_Percentage,
        CostOfLivingAndIncome.Healthcare_Cost,
        CostOfLivingAndIncome.Education_Cost_Percentage,
        CostOfLivingAndIncome.Education_Cost,
        CostOfLivingAndIncome.Transportation_Cost_Percentage,
        CostOfLivingAndIncome.Transportation_Cost,
        CostOfLivingAndIncome.Sum_Percentage,
        CostOfLivingAndIncome.Sum,
        CostOfLivingAndIncome.Sum_Costs,
        CostOfLivingAndIncome.Region
    ).where(CostOfLivingAndIncome.Country == country)

    result = await session.execute(query)
    data = result.fetchall()

    if not data:
        raise HTTPException(
            status_code=404, detail=f"No data found for country: {country}")

    return [
        {
            "Country": row[0],
            "Year": row[1],
            "Average_Monthly_Income": row[2],
            "Net_Income": row[3],
            "Cost_of_Living": row[4],
            "Housing_Cost_Percentage": row[5],
            "Housing_Cost": row[6],
            "Tax_Rate": row[7],
            "Savings_Percentage": row[8],
            "Savings": row[9],
            "Healthcare_Cost_Percentage": row[10],
            "Healthcare_Cost": row[11],
            "Education_Cost_Percentage": row[12],
            "Education_Cost": row[13],
            "Transportation_Cost_Percentage": row[14],
            "Transportation_Cost": row[15],
            "Sum_Percentage": row[16],
            "Sum": row[17],
            "Sum_Costs": row[18],
            "Region": row[19]
        }
        for row in data
    ]


# OUTDATED
@router.get("/all-information-for-region")
async def get_all_data_for_region(session: AsyncSession = Depends(get_db)) -> List[dict]:
    """
        Endpoint um alle Daten gruppiert nach Regionen abzufragen

    :returns: Das ergebnis der Abfrage
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
        func.avg(CostOfLivingAndIncome.Tax_Rate).label("Tax_Rate"),
        func.avg(CostOfLivingAndIncome.Savings_Percentage).label(
            "Savings_Percentage"),
        func.avg(CostOfLivingAndIncome.Savings).label("Savings"),
        func.avg(CostOfLivingAndIncome.Healthcare_Cost_Percentage).label(
            "Healthcare_Cost_Percentage"),
        func.avg(CostOfLivingAndIncome.Healthcare_Cost).label(
            "Healthcare_Cost"),
        func.avg(CostOfLivingAndIncome.Education_Cost_Percentage).label(
            "Education_Cost_Percentage"),
        func.avg(CostOfLivingAndIncome.Education_Cost).label("Education_Cost"),
        func.avg(CostOfLivingAndIncome.Transportation_Cost_Percentage).label(
            "Transportation_Cost_Percentage"),
        func.avg(CostOfLivingAndIncome.Transportation_Cost).label(
            "Transportation_Cost"),
        func.avg(CostOfLivingAndIncome.Sum_Percentage).label("Sum_Percentage"),
        func.avg(CostOfLivingAndIncome.Sum).label("Sum"),
        func.avg(CostOfLivingAndIncome.Sum_Costs).label("Sum_Costs")
    ).group_by(CostOfLivingAndIncome.Region, CostOfLivingAndIncome.Year)

    result = await session.execute(query)
    data = result.fetchall()

    if not data:
        raise HTTPException(status_code=404, detail="No data found.")

    return [
        {
            "Region": row[0],
            "Year": row[1],
            "Average_Monthly_Income": row[2],
            "Net_Income": row[3],
            "Cost_of_Living": row[4],
            "Housing_Cost_Percentage": row[5],
            "Housing_Cost": row[6],
            "Tax_Rate": row[7],
            "Savings_Percentage": row[8],
            "Savings": row[9],
            "Healthcare_Cost_Percentage": row[10],
            "Healthcare_Cost": row[11],
            "Education_Cost_Percentage": row[12],
            "Education_Cost": row[13],
            "Transportation_Cost_Percentage": row[14],
            "Transportation_Cost": row[15],
            "Sum_Percentage": row[16],
            "Sum": row[17],
            "Sum_Costs": row[18]
        }
        for row in data
    ]


# OUTDATED
@router.get("/all-information")
async def get_all_data(session: AsyncSession = Depends(get_db)) -> List[dict]:
    """
        Endpoint um alle Daten abzufragen

    :returns: Das ergebnis der Abfrage
    """
    query = select(
        CostOfLivingAndIncome.Country,
        CostOfLivingAndIncome.Year,
        CostOfLivingAndIncome.Average_Monthly_Income,
        CostOfLivingAndIncome.Net_Income,
        CostOfLivingAndIncome.Cost_of_Living,
        CostOfLivingAndIncome.Housing_Cost_Percentage,
        CostOfLivingAndIncome.Housing_Cost,
        CostOfLivingAndIncome.Tax_Rate,
        CostOfLivingAndIncome.Savings_Percentage,
        CostOfLivingAndIncome.Savings,
        CostOfLivingAndIncome.Healthcare_Cost_Percentage,
        CostOfLivingAndIncome.Healthcare_Cost,
        CostOfLivingAndIncome.Education_Cost_Percentage,
        CostOfLivingAndIncome.Education_Cost,
        CostOfLivingAndIncome.Transportation_Cost_Percentage,
        CostOfLivingAndIncome.Transportation_Cost,
        CostOfLivingAndIncome.Sum_Percentage,
        CostOfLivingAndIncome.Sum,
        CostOfLivingAndIncome.Sum_Costs,
        CostOfLivingAndIncome.Region
    )

    result = await session.execute(query)
    data = result.fetchall()

    if not data:
        raise HTTPException(status_code=404, detail="No data found.")

    return [
        {
            "Country": row[0],
            "Year": row[1],
            "Average_Monthly_Income": row[2],
            "Net_Income": row[3],
            "Cost_of_Living": row[4],
            "Housing_Cost_Percentage": row[5],
            "Housing_Cost": row[6],
            "Tax_Rate": row[7],
            "Savings_Percentage": row[8],
            "Savings": row[9],
            "Healthcare_Cost_Percentage": row[10],
            "Healthcare_Cost": row[11],
            "Education_Cost_Percentage": row[12],
            "Education_Cost": row[13],
            "Transportation_Cost_Percentage": row[14],
            "Transportation_Cost": row[15],
            "Sum_Percentage": row[16],
            "Sum": row[17],
            "Sum_Costs": row[18],
            "Region": row[19]
        }
        for row in data
    ]

# -------------------------------------

# OUTDATED
def get_disposable_income_query() -> select:
    """
        Query für die Berechnung des verfügbaren Einkommens

    :return: sqlalchemy Query
    """
    query = select(
        CostOfLivingAndIncome.Country,
        CostOfLivingAndIncome.Year,
        (CostOfLivingAndIncome.Net_Income -
         CostOfLivingAndIncome.Sum_Costs).label("Remaining_Income")
    )

    return query

# OUTDATED
def get_disposable_income_query_REGION() -> select:
    """
        Query für die Berechnung des verfügbaren Einkommens gruppiert nach Regionen

    :return: sqlalchemy Query
    """

    query = select(
        CostOfLivingAndIncome.Region,
        CostOfLivingAndIncome.Year,
        (func.avg(CostOfLivingAndIncome.Net_Income) -
         func.avg(CostOfLivingAndIncome.Sum_Costs)).label("Remaining_Income")
    ).group_by(CostOfLivingAndIncome.Region, CostOfLivingAndIncome.Year)

    return query


# ---


# OUTDATED
def get_x_query() -> select:
    """
        Query für XXX

    :return: XXX
    """
    query = select(
        CostOfLivingAndIncome.Country,
        CostOfLivingAndIncome.Year,
        (CostOfLivingAndIncome.Net_Income -
         CostOfLivingAndIncome.Sum_Costs).label("Remaining_Income")
    )

    return query


# -------------------------------------

# OUTDATED
@router.get("/financial-development", response_model=List[dict])
async def financial_development(
    method: str,
    session: AsyncSession = Depends(get_db)
) -> List[dict]:
    """
        Endoint um die finanzielle Entwicklung in verschiedenen Ländern anhand verschiedener Methoden abzufragen.
        Methoden:
        - remaining_income
        - x
        - xx

    :param method: XXX

    :return: A list of dictionaries containing the data
    """
    query = None

    match method:
        case "remaining_income":
            query = get_disposable_income_query()
        case "x":
            query = ""
        case "xx":
            query = ""
        case _:
            raise HTTPException(
                status_code=404, detail=f"No method: '{method}' found.")

    result = await session.execute(query)
    data = result.fetchall()

    if not data:
        raise HTTPException(
            status_code=404, detail=f"No data found for method: {method}.")

    return [
        {
            "Country": row[0],
            "Year": row[1],
            "Value": row[2],
            "Method": method
        }
        for row in data
    ]

# OUTDATED
@router.get("/financial_development_region", response_model=List[dict])
async def financial_development_region(
    method: str,
    session: AsyncSession = Depends(get_db)
) -> List[dict]:
    """
        Endoint um die finanzielle Entwicklung in verschiedenen Regionen anhand verschiedener Methoden abzufragen.
        Methoden:
        - remaining_income
        - x
        - xx

    :param method: XXX

    :return: A list of dictionaries containing the data
    """
    query = None

    match method:
        case "remaining_income":
            query = get_disposable_income_query_REGION()
        case "x":
            query = ""
        case "xx":
            query = ""
        case _:
            raise HTTPException(
                status_code=404, detail=f"No method: '{method}' found.")

    result = await session.execute(query)
    data = result.fetchall()

    if not data:
        raise HTTPException(
            status_code=404, detail=f"No data found for method: {method}.")

    return [
        {
            "Country": row[0],
            "Year": row[1],
            "Value": row[2],
            "Method": method
        }
        for row in data
    ]



# -------------------------------------

# TODO replicate with multiple years
@router.get("/recommended-countries", response_model=List[dict])
async def recommended_countries(
    healthcare_multiplicator: int,
    education_multiplicator: int,
    income_multiplicator: float,
    extra_country: str = None,
    start_year: int = 2021,
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



    :param healthcare_multiplicator: XXX
    :param education_multiplicator: XXX
    :param income_multiplicator: XXX
    :param extra_country: XXX
    :param start_year: XXX

    :return: A list of dictionaries containing the data
    """

    if healthcare_multiplicator < 0 or education_multiplicator < 0 or income_multiplicator < 0:
        raise HTTPException(
            status_code=400, detail="Multiplicators must be greater than 0.")

    query = select(
        CostOfLivingAndIncome.Country,
        CostOfLivingAndIncome.Average_Monthly_Income,
        CostOfLivingAndIncome.Net_Income,
        CostOfLivingAndIncome.Housing_Cost,
        CostOfLivingAndIncome.Tax_Rate,
        CostOfLivingAndIncome.Healthcare_Cost,
        CostOfLivingAndIncome.Education_Cost,
        CostOfLivingAndIncome.Transportation_Cost,
        CostOfLivingAndIncome.Year
    ).where(CostOfLivingAndIncome.Year >= start_year)


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
            "Year": row[8]
                  }

        current_country["Average_Monthly_Income"] = current_country["Average_Monthly_Income"] * income_multiplicator
        current_country["Net_Income"] = current_country["Net_Income"] * income_multiplicator
        current_country["Healthcare_Cost"] = current_country["Healthcare_Cost"] * healthcare_multiplicator
        current_country["Education_Cost"] = current_country["Education_Cost"] * education_multiplicator
        current_country["Savings"] = current_country["Net_Income"] - current_country["Housing_Cost"] - current_country["Healthcare_Cost"] - current_country["Education_Cost"] - current_country["Transportation_Cost"]

        if extra_country and extra_country == current_country["Country"]:
            current_country["Country"] = f'{current_country["Country"]} (Selected)'
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
            [c for c in missing_country_years_sorted.get(top_country["Country"], []) if c["Year"] != 2023],
            key=lambda x: -x["Year"]
        )

        # Sucht den Index des aktuellen Landes
        insert_index = new_countries.index(top_country) + 1
        # Fügt die Länder/Jahre in die Liste ein
        new_countries[insert_index:insert_index] = previous_years

    return new_countries


