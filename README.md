#  ITMO University llm агент 

Сервис для автоматического ответа на вопросы об Университете ИТМО с использованием LLM и поиска информации.

## ⭐ Ключевые особенности

⭐⭐⭐⭐ **Интеграция с AwanLLM API**  
- Особенность сервиса в наличии хороших тарифов для доступа к LLaMA, а также
хорошие условия для free-to-use (20 req/min, 200 req/day)
- Использую Meta-Llama-3.1-70B-Instruct (есть модели и поменьше)

⭐⭐⭐ **Безопасность и Prompt Injection Protection**
Вдохновился выступлением AI Security Lab и попытался сделать следующее:
- защита от prompt injection 
- валидация и санитизация вх. данных 
- обработка ответов модели

⭐⭐ **Умный поиск информации**
- Интеграция с Google Custom Search (на мой взгляд достаточно было удобно)
- RSS лента новостей ИТМО (а также)
- Контекстно-зависимый выбор источников
- Автоматическая валидация релевантности


## Функциональность

- Автоматические ответы на вопросы с вариантами ответов
- Поиск информации через Google Custom Search
- Интеграция с RSS лентой новостей ИТМО
- Использование LLM для анализа
- Docker контейнеризация

## Быстрый старт

### Предварительные требования

1. Docker и Docker Compose
2. Python 3.9+
3. API ключи:
   - AWANLLM API key
   - Google API key
   - Google Custom Search Engine ID

### Установка

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd <project-directory>
```

2. Создайте файл .env:
```env
# API Keys
AWANLLM_API_KEY=your_awanllm_api_key
GOOGLE_API_KEY=your_google_api_key
GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id

# API URLs
AWAN_API_URL=https://api.awanllm.com/v1/completions
GOOGLE_SEARCH_URL=https://www.googleapis.com/customsearch/v1
```

3. Запустите сервис:
```bash
docker-compose up --build
```

### Использование

1. Проверка работы сервиса:
```bash
python test_api.py
```

2. Отправка запроса через curl:
```bash
curl -X POST http://localhost:8080/api/request \
  -H "Content-Type: application/json" \
  -d '{
    "query": "В каком городе находится главный кампус Университета ИТМО?\n1. Москва\n2. Санкт-Петербург\n3. Екатеринбург\n4. Нижний Новгород",
    "id": 1
  }'
```

### Формат запросов и ответов

**Запрос:**
```json
{
  "query": "Текст вопроса\n1. Вариант 1\n2. Вариант 2\n...",
  "id": 1
}
```

**Ответ:**
```json
{
  "id": 1,
  "answer": 2,
  "reasoning": "[Meta-Llama-3.1-70B-Instruct] Объяснение ответа...",
  "sources": [
    "https://itmo.ru/ru/",
    "https://abit.itmo.ru/"
  ]
}
```

## Разработка

### Структура проекта
```
.
├── main.py           # Основной FastAPI сервер
├── test_api.py       # Тесты API
├── start.sh          # Скрипт запуска
├── Dockerfile        # Конфигурация Docker
├── docker-compose.yml
├── requirements.txt
└── README.md
```

### Локальный запуск без Docker

1. Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Запустите сервер:
```bash
python main.py
```

### Резервное копирование

Создание резервной копии:
```bash
python backup.py
```

## Безопасность

- Реализована защита от prompt injection
- Валидация входных данных
- Очистка ответов LLM
- Ограничение количества запросов

## Поддержка

При возникновении проблем:
1. Проверьте логи: `docker-compose logs`
2. Убедитесь в правильности API ключей
3. Создайте issue в репозитории

## Лицензия

MIT
