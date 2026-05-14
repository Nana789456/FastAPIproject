from fastapi import FastAPI
from app.api.v1.endpoints import painting, literature


app = FastAPI(title="Course Warehouse")

app.include_router(painting.router, prefix="/v1/creativity", tags=["creativity"])
app.include_router(literature.router, prefix="/v1/creativity", tags=["creativity"])