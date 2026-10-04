"""
Главная точка входа Calculator API.

В этом модуле создаётся приложение FastAPI,
подключаются маршруты и определяется служебный
endpoint для проверки состояния приложения.
"""

from pathlib import Path

from fastapi import FastAPI

from app.api.calculator import router as calculator_router

PROJECT_ROOT = Path(__file__).resolve().parent.parent

VERSION_FILE = PROJECT_ROOT / "VERSION"


def get_version() -> str:
    """
    Возвращает текущую версию приложения.
    """

    if VERSION_FILE.exists():
        return VERSION_FILE.read_text(
            encoding="utf-8"
        ).strip()


    return "unknown"


app = FastAPI(
    title="Calculator API",
    version=get_version(),
    docs_url="/docs", 
)


@app.get("/health")
def health():

    return {
        "status": "ok",
        "version": get_version(),
    }



app.include_router(
    calculator_router,
    prefix="/api/v1",
    tags=["calculator"],
)