"""
Model configurations - DeepSeek R1 and OpenRouter integration
"""

from typing import Optional
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_anthropic import ChatAnthropic
from config.settings import settings

def get_llm_model(model_name: Optional[str] = None):
    """
    Returns LLM model - OpenRouter support for DeepSeek R1
    
    Args:
        model_name: Model name, uses default model if None
        
    Returns:
        LLM model instance
    """
    model_name = model_name or settings.DEFAULT_LLM_MODEL
    
    if model_name.startswith("gpt"):
        # Use OpenAI direct API
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
        # Use OpenAI as default
        return ChatOpenAI(
            model=model_name,
            api_key=settings.OPENAI_API_KEY,
            base_url="https://api.openai.com/v1/",
            temperature=0.7
        )

def get_embedding_model():
    """
    Returns embedding model - OpenAI Direct Client Wrapper
    
    Returns:
        Embedding model instance
    """
    import openai
    import os
    
    class OpenAIDirectEmbeddings:
        """Wrapper that directly uses OpenAI client"""
        
        def __init__(self):
            self.api_key = settings.OPENAI_API_KEY
            # Explicitly specify Base URL - this is very important!
            self.client = openai.OpenAI(
                api_key=self.api_key,
                base_url="https://api.openai.com/v1/"
            )
            self.model = "text-embedding-3-small"
        
        def embed_documents(self, texts):
            """Create embeddings for document list"""
            try:
                response = self.client.embeddings.create(
                    model=self.model,
                    input=texts
                )
                return [data.embedding for data in response.data]
            except Exception as e:
                print(f"❌ Embedding error: {e}")
                raise
        
        def embed_query(self, text):
            """Create embedding for a single query"""
            try:
                response = self.client.embeddings.create(
                    model=self.model,
                    input=[text]
                )
                return response.data[0].embedding
            except Exception as e:
                print(f"❌ Embedding error: {e}")
                raise
    
    return OpenAIDirectEmbeddings() 