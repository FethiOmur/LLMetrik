"""
Soru-cevap ajanı
"""

from typing import Dict, Any, List
from agents.base_agent import BaseAgent
from config.models import get_llm_model
from langchain_core.prompts import PromptTemplate

class QAAgent(BaseAgent):
    """Soru-cevap işlemlerini gerçekleştiren ajan"""
    
    def __init__(self):
        super().__init__(
            name="qa_agent",
            description="Belgelerden alınan bilgilere dayanarak soruları yanıtlar"
        )
        self.llm = get_llm_model()
        self.turkish_prompt_template = self._create_turkish_prompt_template()
        self.english_prompt_template = self._create_english_prompt_template()
    
    def _create_turkish_prompt_template(self) -> PromptTemplate:
        """Türkçe QA için prompt template oluşturur"""
        template = """
Sana grant belgelerinden alınan aşağıdaki bilgiler ve bir soru veriliyor.
Bu bilgilere dayanarak soruyu doğru ve detaylı bir şekilde yanıtla.

Verilen Belgeler:
{documents}

Soru: {question}

Yanıtlarken:
1. Sadece verilen belgelerden elde edilen bilgileri kullan
2. Her bilgi için hangi belgeden geldiğini belirt
3. Eğer sorunun cevabı belgelerde yoksa, bu durumu açıkça belirt
4. Yanıtını Türkçe ver
5. Detaylı ve anlaşılır bir açıklama yap

Yanıt:
"""
        return PromptTemplate(
            template=template,
            input_variables=["documents", "question"]
        )
    
    def _create_english_prompt_template(self) -> PromptTemplate:
        """İngilizce QA için prompt template oluşturur"""
        template = """
You are given the following information from grant documents and a question.
Based on this information, answer the question accurately and in detail.

Given Documents:
{documents}

Question: {question}

When answering:
1. Use only the information obtained from the given documents
2. Specify which document each piece of information comes from
3. If the answer to the question is not in the documents, clearly state this
4. Respond in English
5. Provide a detailed and clear explanation

Answer:
"""
        return PromptTemplate(
            template=template,
            input_variables=["documents", "question"]
        )
    
    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Soru-cevap işlemini gerçekleştirir
        
        Args:
            state: Mevcut durum (query, retrieved_documents ve detected_language içermeli)
            
        Returns:
            Yanıt ve güncellenmiş durum
        """
        query = state.get("query", "")
        retrieved_documents = state.get("retrieved_documents", [])
        detected_language = state.get("detected_language", "tr")
        
        if not query or not retrieved_documents:
            if detected_language == "en":
                state["qa_response"] = "Insufficient information found to answer the question."
            else:
                state["qa_response"] = "Yanıtlamak için yeterli bilgi bulunamadı."
            return state
        
        # Belgeleri formatla
        formatted_docs = self._format_documents(retrieved_documents, detected_language)
        
        # Dile göre prompt seç
        if detected_language == "en":
            prompt_template = self.english_prompt_template
        else:
            prompt_template = self.turkish_prompt_template
        
        # Prompt oluştur ve LLM'e gönder
        prompt = prompt_template.format(
            documents=formatted_docs,
            question=query
        )
        
        response = self.llm.invoke(prompt)
        
        # Yanıtı duruma ekle
        state["qa_response"] = response.content
        state["qa_performed"] = True
        
        return state
    
    def _format_documents(self, documents: List[Dict[str, Any]], language: str = "tr") -> str:
        """
        Belgeleri prompt için formatlar
        
        Args:
            documents: Formatlanacak belgeler
            language: Dil kodu ('tr' veya 'en')
            
        Returns:
            Formatlanmış belge metni
        """
        formatted = []
        
        for i, doc in enumerate(documents, 1):
            content = doc.get("content", "")
            metadata = doc.get("metadata", {})
            filename = metadata.get("filename", "Unknown Document" if language == "en" else "Bilinmeyen Belge")
            page_number = metadata.get("page_number", "Unknown page" if language == "en" else "Bilinmeyen sayfa")
            
            if language == "en":
                header = f"Document {i} - {filename} (Page {page_number}):"
            else:
                header = f"Belge {i} - {filename} (Sayfa {page_number}):"
            
            formatted.append(f"""
{header}
{content}
---
""")
        
        return "\n".join(formatted) 