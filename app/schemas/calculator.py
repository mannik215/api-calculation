from enum import Enum

from pydantic import BaseModel, Field

class Operation(str, Enum):
    add="add"
    subtract="subtract"
    multiply="multiply" 
    divide="divide"

class CalculationRequest(BaseModel):
    a: float = Field(
        ge=-1_000_000_000,
        le=1_000_000_000,
        allow_inf_nan=False,
    )

    b: float = Field(
        ge=-1_000_000_000,
        le=1_000_000_000,
        allow_inf_nan=False,
    )

    operation: Operation

class CalculationResponse(BaseModel):
    result: float
    