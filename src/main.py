from fastapi import FastAPI
from .routers import backend

app = FastAPI()

app.include_router(backend.router)