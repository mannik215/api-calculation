from fastapi import FastAPI

from app.api.calculator import router as calculator_router

app = FastAPI(title="Calculator API", description="A simple calculator API built with FastAPI", version="1.0.0")

app.include_router(calculator_router, prefix="/api/v1", tags=["calculator"])
