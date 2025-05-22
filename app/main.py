from fastapi import FastAPI

from app.routers import weather

app = FastAPI(title="Simple Weather API")

app.include_router(weather.router, prefix="/weather", tags=["weather"])
