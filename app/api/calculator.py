from fastapi import APIRouter, HTTPException

from app.services.calculator import calculate

from app.schemas.calculator import CalculationRequest, CalculationResponse 

router =APIRouter()

@router.post("/calculate", response_model=CalculationResponse)
async def calculate_endpoint(request: CalculationRequest):
    try:
        result =calculate(request.a, request.b, request.operation)
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Invalid calculation input")
    
    return CalculationResponse(result=result)