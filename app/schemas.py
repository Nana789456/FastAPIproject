from pydantic import BaseModel, Field, field_validator
    

# --- Схема для запроса от клиента (тело POST-запроса) ---
class CourseCreate(BaseModel):
    name: str = Field(..., example="Название курса")
    author: str = Field(..., example="Автор курса")
    duration: int = Field(..., example=120, description="Длительность в минутах")
    price: float = Field(..., example=4990.00, description="Стоимость")
    discount: int = Field(0, example=10, description="Скидка в процентах")

# --- Схема для ответа сервера ---
class CourseResponse(BaseModel):
    name: str
    author: str
    duration: int
    price: float
    discount: int

    model_config = {"from_attributes": True}

class VideoCreate(BaseModel):
    title: str = Field(..., example="Название видео")
    author: str = Field(..., example="Автор видео")
    course: str = Field(..., example="Название курса")

class VideoResponse(BaseModel):
    title: str
    author: str
    course: str
    course_id: int

    model_config = {"from_attributes": True}