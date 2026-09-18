from enum import Enum

from pydantic import BaseModel, Field

class Operation(str, Enum):
    add="add"
    subtract="subtract"
    multiply="multiply" 
    divide="divide"

class CalculationRequest(BaseModel):
    a:float
    b:float
    operation: Operation

class CalculationResponse(BaseModel):
    result: float
    