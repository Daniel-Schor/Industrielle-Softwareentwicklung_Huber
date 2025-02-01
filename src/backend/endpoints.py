from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from databases import Database
import asyncio
import os

# Absolute path to the database file
DATABASE_PATH = os.path.join(
    os.getcwd(), 'src', 'database', 'CostOfLivingAndIncome.db'
)

#database URL to the absolute path
DATABASE_URL = f"sqlite+aiosqlite:///{DATABASE_PATH}"

# Set up the database connection
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)
Base = declarative_base()

# Define the model for your table
class CostOfLivingAndIncome(Base):
    __tablename__ = "CostOfLivingAndIncome"

    id = Column(Integer, primary_key=True, index=True)
    Country = Column(String, index=True)
    Average_Monthly_Income = Column(Float)

# Initialize the router for FastAPI
router = APIRouter()

# Dependency to get the DB session
async def get_db():
    async with SessionLocal() as session:
        yield session

# Endpoint to get Average_Monthly_Income for all Countries
@router.get("/average-income")
async def get_average_monthly_income(session: AsyncSession = Depends(get_db)):
    query = select(CostOfLivingAndIncome.Country, CostOfLivingAndIncome.Average_Monthly_Income)
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
