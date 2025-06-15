"""
Model yapılandırmaları - DeepSeek R1 ve OpenRouter entegrasyonu
"""

from typing import Optional
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_anthropic import ChatAnthropic
from config.settings import settings

def get_llm_model(model_name: Optional[str] = None):
    """
    LLM modelini döndürür - DeepSeek R1 için OpenRouter desteği
    
    Args:
        model_name: Model adı, None ise default model kullanılır
        
    Returns:
        LLM model instance
    """
    model_name = model_name or settings.DEFAULT_LLM_MODEL
    
    if model_name.startswith("gpt"):
        # OpenAI direct API kullan
        return ChatOpenAI(
            model=model_name,
            api_key=settings.OPENAI_API_KEY,
            base_url="https://api.openai.com/v1/",
            temperature=0.7
        )
    elif model_name.startswith("claude"):
        return ChatAnthropic(
            model=model_name,
            api_key=settings.ANTHROPIC_API_KEY,
            temperature=0.7
        )
    else:
        # Default olarak OpenAI kullan
        return ChatOpenAI(
            model=model_name,
            api_key=settings.OPENAI_API_KEY,
            base_url="https://api.openai.com/v1/",
            temperature=0.7
        )

def get_embedding_model():
    """
    Embedding modelini döndürür - OpenAI Direct Client Wrapper
    
    Returns:
        Embedding model instance
    """
    import openai
    import os
    
    class OpenAIDirectEmbeddings:
        """OpenAI client'ını doğrudan kullanan wrapper"""
        
        def __init__(self):
            self.api_key = settings.OPENAI_API_KEY
            # Base URL'i explicit olarak belirt - bu çok önemli!
            self.client = openai.OpenAI(
                api_key=self.api_key,
                base_url="https://api.openai.com/v1/"
            )
            self.model = "text-embedding-3-small"
        
        def embed_documents(self, texts):
            """Belge listesi için embedding oluştur"""
            try:
                response = self.client.embeddings.create(
                    model=self.model,
                    input=texts
                )
                return [data.embedding for data in response.data]
            except Exception as e:
                print(f"❌ Embedding hatası: {e}")
                raise
        
        def embed_query(self, text):
            """Tek bir sorgu için embedding oluştur"""
            try:
                response = self.client.embeddings.create(
                    model=self.model,
                    input=[text]
                )
                return response.data[0].embedding
            except Exception as e:
                print(f"❌ Embedding hatası: {e}")
                raise
    
    return OpenAIDirectEmbeddings() 