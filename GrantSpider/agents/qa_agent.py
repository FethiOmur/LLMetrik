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
        self.universal_prompt_template = self._create_universal_prompt_template()
    
    def _create_universal_prompt_template(self) -> PromptTemplate:
        """Evrensel QA prompt template - o4-mini'nin otomatik dil algılamasını kullanır"""
        template = """
You are given the following information from grant documents and a question.
Based on this information, answer the question accurately and in detail.

IMPORTANT: Respond in the same language as the question. If the question is in Turkish, respond in Turkish. If in English, respond in English. If in Italian, respond in Italian.

Given Documents:
{documents}

Question: {question}

When answering:
1. Use only the information obtained from the given documents
2. Specify which document each piece of information comes from
3. If the answer to the question is not in the documents, clearly state this
4. Respond in the SAME LANGUAGE as the question
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
        
        print(f"🤖 QA Agent - Dil: {detected_language}, Sorgu: '{query[:50]}...'")
        
        # Basit relevans kontrolü - sadece çok kısa genel sorular için
        if len(query.strip().split()) < 3:
            simple_greetings = ['hello', 'hi', 'hey', 'merhaba', 'selam', 'ciao', 'salve']
            if any(greeting in query.lower() for greeting in simple_greetings):
                # o4-mini'nin doğal dil algılamasına güven - soru hangi dildeyse o dilde yanıt ver
                state["qa_response"] = "I'm designed to answer questions about AMIF grant documents. Please ask me about grant procedures, eligibility criteria, or application requirements."
                state["qa_performed"] = True
                return state
        
        if not query or not retrieved_documents:
            state["qa_response"] = "I couldn't find sufficient information to answer your question."
            state["qa_performed"] = True
            return state
        
        # Belgeleri formatla - dil algılamasız
        formatted_docs = self._format_documents(retrieved_documents)
        
        # Evrensel prompt kullan - o4-mini otomatik dil algılayacak
        prompt = self.universal_prompt_template
        print(f"🌍 Evrensel prompt kullanılıyor - o4-mini otomatik dil algılaması")
        
        # Prompt oluştur ve LLM'e gönder
        prompt = prompt.format(
            documents=formatted_docs,
            question=query
        )
        
        print(f"📝 Prompt uzunluğu: {len(prompt)} karakter")
        
        response = self.llm.invoke(prompt)
        
        print(f"✅ LLM yanıtı alındı - Uzunluk: {len(response.content)} karakter")
        
        # Yanıtı duruma ekle
        state["qa_response"] = response.content
        state["qa_performed"] = True
        
        return state
    
    def _format_documents(self, documents: List[Dict[str, Any]]) -> str:
        """
        Belgeleri prompt için formatlar - dil algılamasız
        
        Args:
            documents: Formatlanacak belgeler
            
        Returns:
            Formatlanmış belge metni
        """
        formatted = []
        
        for i, doc in enumerate(documents, 1):
            content = doc.get("content", "")
            metadata = doc.get("metadata", {})
            filename = metadata.get("filename", "Unknown Document")
            page_number = metadata.get("page_number", "Unknown page")
            
            header = f"Document {i} - {filename} (Page {page_number}):"
            
            formatted.append(f"""
{header}
{content}
---
""")
        
        return "\n".join(formatted) 