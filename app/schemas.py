from pydantic import BaseModel, Field, field_validator


class PaintingResponseGet(BaseModel):
    name: str = Field(..., json_schema_extra={"example": "Название"})
    author: str = Field(..., json_schema_extra={"example": "Автор"})
    duration: int = Field(..., json_schema_extra={"example": "Продолжительность в часах"})
    price: float = Field(..., json_schema_extra={"example": "Стоимость"})


class LiteratureResponseGet(BaseModel):
    name: str = Field(..., json_schema_extra={"example": "Название"})
    author: str = Field(..., json_schema_extra={"example": "Автор"})
    duration: int = Field(..., json_schema_extra={"example": "Продолжительность в часах"})
    price: float = Field(..., json_schema_extra={"example": "Стоимость"})