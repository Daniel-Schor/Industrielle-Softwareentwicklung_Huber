from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Float, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from databases import Database
from typing import List
import asyncio
import os

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
    async with SessionLocal() as session:
        yield session

# Endpoint to get Average_Monthly_Income for all Countries


@router.get("/average-income")
async def get_average_monthly_income(session: AsyncSession = Depends(get_db)):
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


@router.get("/country-information", response_model=List[dict])
async def get_country_data(
    country: str,
    session: AsyncSession = Depends(get_db)
):
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


@router.get("/all-information-for-region")
async def get_all_data(session: AsyncSession = Depends(get_db)):
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


# Endpoint to get all columns for all rows
@router.get("/all-information")
async def get_all_data(session: AsyncSession = Depends(get_db)):
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


def get_xxx_query() -> select:
    query = select(
        CostOfLivingAndIncome.Country,
        CostOfLivingAndIncome.Year,
        (CostOfLivingAndIncome.Net_Income -
         CostOfLivingAndIncome.Sum_Costs).label("Remaining_Income")
    )

    return query


@router.get("/xxx", response_model=List[dict])
async def xxx(
    method: int,
    session: AsyncSession = Depends(get_db)
):
    query = None

    match method:
        case 1:
            query = get_xxx_query()
        case 2:
            return "You chose Option 2"
        case 3:
            return "You chose Option 3"
        case _:
            return "Invalid choice"

    result = await session.execute(query)
    data = result.fetchall()

    if not data:
        raise HTTPException(
            status_code=404, detail=f"No data found for country: {country}")

    return [
        {
            "Country": row[0],
            "Year": row[1],
            "Value": row[2]
        }
        for row in data
    ]
