#  ITMO University llm агент 

Сервис для автоматического ответа на вопросы об Университете ИТМО с использованием LLM и поиска информации
в рамках Мегашколы 2025
## ⭐ Ключевые особенности

⭐⭐⭐ **Интеграция с AwanLLM API**  
- Особенность сервиса в наличии хороших тарифов для доступа к LLaMA, а также
хорошие условия для free-to-use (20 req/min, 200 req/day)
- Использую Meta-Llama-3.1-70B-Instruct (есть модели и поменьше)

⭐⭐ **Безопасность и Prompt Injection Protection**  
Вдохновился выступлением AI Security Lab и попытался сделать следующее:
- защита от prompt injection 
- валидация и санитизация вх. данных 
- обработка ответов модели

⭐ **Умный поиск информации**
- Интеграция с Google Custom Search (на мой взгляд достаточно было удобно)
- RSS лента новостей ИТМО (для учета актуальных событий)
- Контекстно-зависимый выбор источников
- Автоматическая валидация релевантности (проверка наличия ключевых слов)

⚠️ Важные моменты
- У awanllm есть ограничение 10 req/day у большой модели (наш случай).Но я пользовался продвинутой версей (pro) с 2000 req/min.
Если это ⚠️⚠️ сильно повлияет на проверку ⚠️⚠️,
 достаточно поменять название на маленькую модель или написать в ЛС мне по поводу api ключа к про версии.
- К сожалению, не успел разобраться с ошибками с развертыванием на vercel. Поэтому только локальный запуск
- Curl на винде не работал у меня (но и это было вроде необязательным критерием)

## Быстрый старт
Ссылки на сервисы:
1) https://www.awanllm.com
2) 2)https://programmablesearchengine.google.com/about/

### Предварительные требования
Нужно следующее для запуска:
1. Docker и Docker Compose
2. Python 3.9+
3. API ключи:
   - AWANLLM API key
   - Google API key
   - Google Custom Search Engine ID

### Подробная инструкция

1. Клонируем репозиторий:
```bash
git clone <repository-url>
cd <project-directory>
```

2. Создайте файл .env, чтобы вставить ключи (в проекте есть example)
```env
# API Keys
AWANLLM_API_KEY=your_awanllm_api_key
GOOGLE_API_KEY=your_google_api_key
GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id

# API URLs
AWAN_API_URL=https://api.awanllm.com/v1/completions
GOOGLE_SEARCH_URL=https://www.googleapis.com/customsearch/v1
```

3. Запускаем сервис:
```bash
docker-compose up --build
```

### Использование агента

1. Для проверки работы агента (содержит в себе базвоый вопрос)
```bash
python test_api.py
```

### Как записывается (форма) ответа и запроса?

**Запрос выглядит так:**
```json
{
  "query": "Текст вопроса\n1. Вариант 1\n2. Вариант 2\n...",
  "id": 1
}
```

**Сам ответ (информация о модели пишется в начале):**
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

