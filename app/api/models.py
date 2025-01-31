from pydantic import BaseModel, Field
from typing import Optional, List

class QuestionRequest(BaseModel):
    query: str
    id: int

class AnswerResponse(BaseModel):
    id: int
    answer: Optional[int] = Field(description="Номер выбранного варианта ответа (1-10)")
    reasoning: str = Field(description="Объяснение выбранного ответа")
    sources: List[str] = Field(description="Список использованных источников")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "answer": 2,
                "reasoning": "Главный кампус Университета ИТМО расположен в Санкт-Петербурге",
                "sources": ["https://itmo.ru/ru/", "https://abit.itmo.ru/"]
            }
        } 