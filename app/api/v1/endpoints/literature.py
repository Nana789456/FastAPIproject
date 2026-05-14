from fastapi import APIRouter, status, Request

from app.schemas import LiteratureResponseGet


router = APIRouter()


@router.get(
        "/literature", 
        status_code=status.HTTP_202_ACCEPTED,
        response_model=LiteratureResponseGet,    
    )
async def literature(
        request: Request,
    ):
    return {
        "name": "Name",
        "author": "Name",
        "duration": 100,
        "price": 15000,
    }