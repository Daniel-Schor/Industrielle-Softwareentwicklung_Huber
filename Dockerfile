# Base image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy files
COPY . /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Run ETL once to set up the database
RUN python src/database/ETL/ETL.py

# Expose ports (FastAPI: 8000, Streamlit: 8501)
EXPOSE 8000 8501
