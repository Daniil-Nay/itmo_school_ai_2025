import requests
import time
from typing import List, Tuple
from app.core.config import GOOGLE_API_KEY, SEARCH_ENGINE_ID, GOOGLE_SEARCH_URL
from app.services.news import get_itmo_news

def search_info(query: str) -> Tuple[str, List[str]]:
    """сделал поиск инфы через гугл апи и новости итмо"""
    try:
        if any(word in query.lower() for word in ['новости', 'недавно', '2023', '2024']):
            news_results, news_sources = get_itmo_news()
            if news_results:
                return news_results, news_sources

        all_snippets = []
        all_sources = []
        base_query = query.replace('\n', ' ').split('1.')[0].strip()
        
        primary_sources = [
            f'site:itmo.ru "{base_query}"',
            f'site:news.itmo.ru "{base_query}"',
            f'site:abit.itmo.ru "{base_query}"',
            f'site:student.itmo.ru "{base_query}"',
            f'site:research.itmo.ru "{base_query}"',
            f'site:museum.itmo.ru "{base_query}"',
            f'site:library.itmo.ru "{base_query}"',
            f'site:en.itmo.ru "{base_query}"'
        ]
        
        secondary_sources = [
            f'site:minobrnauki.gov.ru ИТМО {base_query}',
            f'site:ria.ru ИТМО {base_query}',
            f'site:tass.ru ИТМО {base_query}'
        ]
        
        for search_query in primary_sources + secondary_sources:
            try:
                params = {
                    'key': GOOGLE_API_KEY,
                    'cx': SEARCH_ENGINE_ID,
                    'q': search_query,
                    'num': 3,
                    'gl': 'ru',
                    'hl': 'ru',
                    'sort': 'date'
                }
                
                time.sleep(1)
                response = requests.get(GOOGLE_SEARCH_URL, params=params, timeout=10)
                
                if response.status_code == 200:
                    results = response.json()
                    if 'items' in results:
                        for item in results['items']:
                            snippet = item.get('snippet', '')
                            link = item['link']
                            if any(keyword.lower() in snippet.lower() for keyword in base_query.split()):
                                if link not in all_sources:
                                    all_sources.append(link)
                                    all_snippets.append(snippet)
                
            except Exception as e:
                print(f'не могу найти инфу: {str(e)}')
                continue
        
        if all_snippets:
            return "\n".join(all_snippets[:5]), list(set(all_sources))[:3]
        
        return "", ["https://itmo.ru"]
        
    except Exception as e:
        print(f'что-то сломалось: {str(e)}')
        return "", ["https://itmo.ru"] 