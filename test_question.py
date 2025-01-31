import requests
import json
from dotenv import load_dotenv

load_dotenv()

def test_basic_question():
    """проверяю базовый вопрос про итмо"""
    base_url = "http://localhost:8080"
    
    question = {
        "query": "В каком городе находится главный кампус Университета ИТМО?\n1. Москва\n2. Санкт-Петербург\n3. Екатеринбург\n4. Нижний Новгород",
        "id": 1
    }
    
    print('\nзапускаю тест...')
    try:
        print(f'отправляю запрос: {json.dumps(question, indent=2, ensure_ascii=False)}')
        
        response = requests.post(f"{base_url}/api/request", json=question)
        print(f'статус: {response.status_code}')
        
        if response.status_code == 200:
            result = response.json()
            print('получил ответ:')
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f'ошибка: {response.text}')
            
    except Exception as e:
        print(f'что-то сломалось: {str(e)}')

if __name__ == "__main__":
    print('начинаю тест...')
    test_basic_question()