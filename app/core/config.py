from dotenv import load_dotenv
import os

load_dotenv()

AWANLLM_API_KEY = os.getenv('AWANLLM_API_KEY')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
SEARCH_ENGINE_ID = os.getenv('GOOGLE_SEARCH_ENGINE_ID')

AWAN_API_URL = os.getenv('AWAN_API_URL')
GOOGLE_SEARCH_URL = os.getenv('GOOGLE_SEARCH_URL') 