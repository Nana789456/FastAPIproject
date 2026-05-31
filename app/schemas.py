from pydantic import BaseModel, Field, field_validator
    

# --- Схема для запроса от клиента (тело POST-запроса) ---
class CourseCreate(BaseModel):
    name: str = Field(..., example="Название курса")
    author: str = Field(..., example="Автор курса")
    duration: int = Field(..., example=120, description="Длительность в минутах")
    price: float = Field(..., example=4990.00)
    discount: int = Field(0, example=10, description="Скидка в процентах")

# --- Схема для ответа сервера ---
class CourseResponse(BaseModel):
    name: str
    author: str
    duration: int
    price: float
    discount: int

    model_config = {"from_attributes": True}
