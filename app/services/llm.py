import json
import requests
import re
from typing import Optional, Tuple
from app.core.config import AWANLLM_API_KEY, AWAN_API_URL
from app.api.models import QuestionRequest, AnswerResponse

def clean_and_validate_llm_response(text: str) -> Tuple[Optional[int], str]:
    """чистим и проверяем ответ от модели"""
    text = text.replace('\n', ' ').replace('\r', ' ')
    text = ' '.join(text.split())
    text = text.replace('\\', '')
    
    json_start = text.find('{')
    json_end = text.rfind('}') + 1
    
    if json_start != -1 and json_end != -1:
        json_str = text[json_start:json_end]
        try:
            parsed = json.loads(json_str)
            if isinstance(parsed, dict):
                answer = parsed.get('answer')
                reasoning = parsed.get('reasoning', '')
                
                if isinstance(answer, (int, str)) and str(answer).isdigit():
                    answer = int(answer)
                    if 1 <= answer <= 10:
                        return answer, reasoning
                
                return None, reasoning
        except json.JSONDecodeError:
            pass
    
    answer = None
    reasoning = text
    
    answer_match = re.search(r'(?:answer"?\s*:?\s*|ответ\s*:?\s*)(\d+)', text.lower())
    if answer_match:
        try:
            answer = int(answer_match.group(1))
            if not (1 <= answer <= 10):
                answer = None
        except:
            pass
    
    reasoning = re.sub(r'(\{|\}|"answer"?\s*:?\s*\d+\s*,?\s*|"reasoning"?\s*:?\s*"?)', '', reasoning)
    reasoning = reasoning.strip(' "\'')
    
    return answer, reasoning

async def process_llm_request(question: QuestionRequest, search_results: str, found_sources: list) -> AnswerResponse:
    """обработка запроса через лламу"""
    system_prompt = """Ты - информационный агент Университета ИТМО. Твоя задача - найти точный ответ в предоставленной информации.

    Важно:
    1. Всегда отвечай на русском языке
    2. Используй конкретные факты из найденных источников
    3. Цитируй найденную информацию в своих рассуждениях
    4. Добавляй живые комментарии в процессе поиска
    5. Если находишь противоречивую информацию, укажи все источники
    6. Если не находишь точного ответа, честно скажи об этом
    7. Не делай предположений - используй только найденные факты
    
    Формат ответа должен быть строго в формате JSON:
    {
        "answer": [номер ответа (1-10) или null, если нет точной информации],
        "reasoning": [рассуждение на русском языке с цитированием найденных фактов]
    }

    Найденная информация:
    {search_results}
    """

    full_prompt = f"{system_prompt}\n\nВопрос:\n{question.query}"

    payload = {
        "model": "Meta-Llama-3.1-70B-Instruct",
        "prompt": full_prompt,
        "temperature": 0.7,
        "max_tokens": 800,
        "response_format": {"type": "json_object"}
    }

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {AWANLLM_API_KEY}"
    }

    response = requests.post(
        AWAN_API_URL, 
        headers=headers, 
        data=json.dumps(payload)
    )

    if response.status_code != 200:
        raise Exception(f'ошибка апи лламы: {response.text}')

    llm_response = response.json()
    text_response = llm_response['choices'][0]['text']
    
    answer, reasoning = clean_and_validate_llm_response(text_response)
    
    return AnswerResponse(
        id=question.id,
        answer=answer,
        reasoning=f"[Meta-Llama-3.1-70B-Instruct] {reasoning}",
        sources=found_sources[:3]
    ) 