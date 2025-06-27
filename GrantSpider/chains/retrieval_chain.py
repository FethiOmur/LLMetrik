"""
Modern RAG (Retrieval Augmented Generation) Chain
"""

from typing import Dict, Any, List
from langchain_core.prompts import PromptTemplate
from ingestion.vector_store import VectorStore
from config.models import get_llm_model

class RetrievalChain:
    """Modern RAG chain class - compatible with LangGraph"""
    
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
        self.llm = get_llm_model()
        self.turkish_prompt = self._create_turkish_prompt()
        self.english_prompt = self._create_english_prompt()
    
    def _create_turkish_prompt(self) -> PromptTemplate:
        """Türkçe RAG prompt'u oluşturur"""
        template = """Sen AMIF (Asylum, Migration and Integration Fund) hibe programı konusunda uzman bir asistansın.
Aşağıda AMIF hibe belgelerinden alınan bilgiler ve kullanıcı sorusu veriliyor.
Bu bilgilere dayanarak soruyu doğru, detaylı ve kullanıcıya faydalı bir şekilde yanıtla.

Belge Bilgileri:
{context}

Kullanıcı Sorusu: {question}

Yanıtlarken:
1. Sadece verilen belgelerden elde edilen bilgileri kullan
2. Bilgileri AMIF hibe süreçleri bağlamında açıkla
3. Pratik öneriler ve açıklamalar ekle
4. Eğer sorunun cevabı belgelerde yoksa, bunu açıkça belirt
5. Yanıtın net, anlaşılır ve Türkçe olsun
6. Mümkünse adım adım yönergeler ver

Yanıt:"""
        
        return PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )
    
    def _create_english_prompt(self) -> PromptTemplate:
        """İngilizce RAG prompt'u oluşturur"""
        template = """You are an expert assistant for AMIF (Asylum, Migration and Integration Fund) grant programs.
Below you will find information from AMIF grant documents and a user question.
Based on this information, answer the question accurately, in detail, and in a way that is helpful to the user.

Document Information:
{context}

User Question: {question}

When answering:
1. Use only the information obtained from the provided documents
2. Explain the information in the context of AMIF grant processes
3. Add practical recommendations and explanations
4. If the answer to the question is not in the documents, clearly state this
5. Make your answer clear, understandable, and in English
6. Provide step-by-step instructions when possible

Answer:"""
        
        return PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )
    
    def run(self, query: str, k: int = 5, language: str = "tr") -> Dict[str, Any]:
        """
        RAG zincirini çalıştırır
        
        Args:
            query: Kullanıcı sorgusu
            k: Döndürülecek belge sayısı
            language: Dil kodu ('tr' veya 'en')
            
        Returns:
            RAG sonucu (answer ve source_documents içerir)
        """
        try:
            # Belgeleri arama yap
            documents, detected_lang = self.vector_store.search_with_sources(query, k=k)
            
            if not documents:
                no_result_msg = "Sorunuzla ilgili bilgi bulunamadı." if language == "tr" else "No relevant information found for your question."
                return {
                    "answer": no_result_msg,
                    "source_documents": [],
                    "detected_language": detected_lang
                }
            
            # Context oluştur
            context = self._format_documents_for_context(documents)
            
            # Dile göre prompt seç
            prompt = self.turkish_prompt if language == "tr" else self.english_prompt
            
            # Prompt'u formatla
            formatted_prompt = prompt.format(
                context=context,
                question=query
            )
            
            # LLM'den yanıt al
            response = self.llm.invoke(formatted_prompt)
            answer = response.content if hasattr(response, 'content') else str(response)
            
            return {
                "answer": answer,
                "source_documents": documents,
                "detected_language": detected_lang
            }
            
        except Exception as e:
            error_msg = f"RAG chain error: {e}"
            fallback_msg = "Bir hata oluştu, lütfen tekrar deneyin." if language == "tr" else "An error occurred, please try again."
            
            return {
                "answer": fallback_msg,
                "source_documents": [],
                "detected_language": language,
                "error": error_msg
            }
    
    def run_with_custom_context(self, query: str, context: str, language: str = "tr") -> str:
        """
        Özel context ile RAG zincirini çalıştırır
        
        Args:
            query: Kullanıcı sorgusu
            context: Özel belge bağlamı
            language: Dil kodu
            
        Returns:
            LLM yanıtı
        """
        try:
            # Dile göre prompt seç
            prompt = self.turkish_prompt if language == "tr" else self.english_prompt
            
            # Prompt'u formatla
            formatted_prompt = prompt.format(
                context=context,
                question=query
            )
            
            # LLM'den yanıt al
            response = self.llm.invoke(formatted_prompt)
            return response.content if hasattr(response, 'content') else str(response)
            
        except Exception as e:
            fallback_msg = "Yanıt oluşturulamadı." if language == "tr" else "Could not generate response."
            return fallback_msg
    
    def _format_documents_for_context(self, documents: List[Any]) -> str:
        """Belgeleri context için formatlar"""
        formatted_docs = []
        
        for i, doc in enumerate(documents, 1):
            content = doc.page_content if hasattr(doc, 'page_content') else str(doc)
            metadata = doc.metadata if hasattr(doc, 'metadata') else {}
            
            filename = metadata.get('filename', 'Unknown document')
            page = metadata.get('page_number', 'Unknown page')
            
            formatted_doc = f"Belge {i} ({filename}, Sayfa {page}):\n{content}"
            formatted_docs.append(formatted_doc)
        
        return "\n\n".join(formatted_docs)
    
    def get_relevant_documents(self, query: str, k: int = 5) -> List[Any]:
        """
        Sorguya ilgili belgeleri döndürür
        
        Args:
            query: Arama sorgusu
            k: Döndürülecek belge sayısı
            
        Returns:
            İlgili belgeler listesi
        """
        try:
            documents, _ = self.vector_store.search_with_sources(query, k=k)
            return documents
        except Exception:
            return [] 