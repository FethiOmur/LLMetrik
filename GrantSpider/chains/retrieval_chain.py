"""
RAG (Retrieval Augmented Generation) zinciri
"""

from typing import Dict, Any, List
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from ingestion.vector_store import VectorStore
from config.models import get_llm_model

class RetrievalChain:
    """RAG zinciri sınıfı"""
    
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
        self.llm = get_llm_model()
        self.retrieval_qa = self._create_retrieval_qa()
    
    def _create_retrieval_qa(self) -> RetrievalQA:
        """RAG zinciri oluşturur"""
        retriever = self.vector_store.get_retriever(
            search_kwargs={"k": 5}
        )
        
        prompt_template = """
Sana grant belgelerinden alınan aşağıdaki bilgiler ve bir soru veriliyor.
Bu bilgilere dayanarak soruyu doğru ve detaylı bir şekilde yanıtla.

Verilen Belgeler:
{context}

Soru: {question}

Yanıtlarken:
1. Sadece verilen belgelerden elde edilen bilgileri kullan
2. Eğer sorunun cevabı belgelerde yoksa, bu durumu açıkça belirt
3. Yanıtını Türkçe ver

Yanıt:
"""
        
        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        
        return RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": prompt}
        )
    
    def run(self, query: str) -> Dict[str, Any]:
        """
        RAG zincirini çalıştırır
        
        Args:
            query: Kullanıcı sorgusu
            
        Returns:
            RAG sonucu
        """
        result = self.retrieval_qa({"query": query})
        
        return {
            "answer": result["result"],
            "source_documents": result["source_documents"]
        } 