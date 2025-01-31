import feedparser
from typing import List, Tuple

def get_itmo_news() -> Tuple[str, List[str]]:
    """получаю новости итмо через рсс"""
    news_snippets = []
    news_sources = []
    
    try:
        rss_url = "https://news.itmo.ru/ru/news/rss/"
        feed = feedparser.parse(rss_url)
        
        for entry in feed.entries[:3]:
            news_snippets.append(f"[{entry.title}] {entry.description}")
            news_sources.append(entry.link)
            
    except Exception as e:
        print(f'не могу получить рсс: {str(e)}')
    
    return "\n\n".join(news_snippets), news_sources 