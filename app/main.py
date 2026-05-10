from fastapi import FastAPI
from app.api.v1.endpoints import painting


app = FastAPI(title="Course Warehouse")

app.include_router(painting.router, prefix="/v1/creativity", tags=["creativity"])
