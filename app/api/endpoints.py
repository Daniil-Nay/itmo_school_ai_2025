from fastapi import APIRouter, HTTPException
from app.api.models import QuestionRequest, AnswerResponse
from app.services.search import search_info
from app.services.llm import process_llm_request

router = APIRouter()

@router.post("/request", response_model=AnswerResponse)
async def process_question(question: QuestionRequest) -> AnswerResponse:
    """основной обработчик запросов"""
    try:
        search_results, found_sources = search_info(question.query)
        response = await process_llm_request(question, search_results, found_sources)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 