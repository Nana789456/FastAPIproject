from fastapi import APIRouter, status, Request

from app.schemas import PaintingResponseGet


router = APIRouter()


@router.get(
        "/painting", 
        status_code=status.HTTP_202_ACCEPTED,
        response_model=PaintingResponseGet,    
    )
async def painting(
        request: Request,
    ):
    return {
        "name": "Name",
        "author": "Name",
        "duration": 100,
        "price": 15000,
    }