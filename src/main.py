from fastapi import FastAPI
from .backend import endpoints

app = FastAPI()

app.include_router(endpoints.router)