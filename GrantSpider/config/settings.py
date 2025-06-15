"""
Yapılandırma ayarları - DeepSeek R1 için OpenRouter entegrasyonu
"""

import os
from typing import Dict, Any
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

class Settings:
    """Uygulama yapılandırma ayarları"""
    
    # API Keys - OpenAI Direct API
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_BASE_URL: str = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    

    
    # Model ayarları - OpenAI
    DEFAULT_LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-4")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-4")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    
    # Vektör veritabanı ayarları
    VECTOR_DB_TYPE: str = "chromadb"  # chromadb, faiss
    VECTOR_DB_PATH: str = os.getenv("VECTOR_DB_PATH", "data/db")
    
    # PDF işleme ayarları
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "200"))
    
    # Uygulama ayarları
    MAX_CHAT_HISTORY: int = 50
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # OpenRouter için ek ayarlar
    OPENROUTER_APP_NAME: str = os.getenv("OPENROUTER_APP_NAME", "GrantSpider")
    OPENROUTER_SITE_URL: str = os.getenv("OPENROUTER_SITE_URL", "https://github.com/your-username/GrantSpider")

settings = Settings() 