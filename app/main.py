from fastapi import FastAPI

from app.api.calculator import router as calculator_router

from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app = FastAPI(title="Calculator API", description="A simple calculator API built with FastAPI", version="1.0.0")

app.include_router(calculator_router, prefix="/api/v1", tags=["calculator"])
@app.middleware("http")
async def security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    return response
