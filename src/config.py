import os
import sys
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import logging
from src.semantic_cache import SemanticCacheManager

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()

if not os.getenv("OPENROUTER_API_KEY"):
    raise ValueError("A chave OPENROUTER_API_KEY não foi encontrada. Verifique o arquivo .env.")

llm_juiz = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    temperature=0, 
    model="openrouter/free"
) 

llm_principal = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    temperature=0.3, 
    model="openrouter/free"
)

try:
    cache_manager = SemanticCacheManager()
except Exception as e:
    logging.warning(f"Não foi possível conectar ao DB. Cache semântico desativado. Erro: {e}")
    cache_manager = None
