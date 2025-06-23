"""
Gelişmiş Mantık Yürütme Zinciri
"""

from typing import Dict, Any, List
from langchain_core.prompts import PromptTemplate
from config.models import get_llm_model

class ReasoningChain:
    """Mantık yürütme zinciri sınıfı - LangGraph ile uyumlu"""
    
    def __init__(self):
        self.llm = get_llm_model()
        self.turkish_prompt = self._create_turkish_prompt()
        self.english_prompt = self._create_english_prompt()
    
    def _create_turkish_prompt(self) -> PromptTemplate:
        """Türkçe mantık yürütme prompt'u oluşturur"""
        template = """Sana AMIF hibe belgeleriyle ilgili bir soru, bu soruyla ilgili belgelerden elde edilen bilgiler ve bir ilk yanıt veriliyor.
Bu bilgileri analiz ederek daha detaylı, mantıklı ve doğru bir yanıt oluştur.

Soru: {question}

İlk Yanıt: {initial_answer}

Belgelerden Elde Edilen Bilgiler:
{context}

Lütfen aşağıdaki adımları takip et:
1. İlk yanıtı analiz et ve doğruluğunu kontrol et
2. Belgelerden elde edilen bilgilerle karşılaştır
3. Eksik, yanlış veya çelişkili bilgileri tespit et
4. Belgelerde bulunan ek bilgileri dahil et
5. Daha kapsamlı, doğru ve faydalı bir yanıt oluştur
6. AMIF hibe süreçleri bağlamında pratik tavsiyeler ekle

Yanıtın Türkçe, net, anlaşılır ve kullanıcıya faydalı olmalıdır.

Geliştirilmiş Yanıt:"""
        
        return PromptTemplate(
            template=template,
            input_variables=["question", "initial_answer", "context"]
        )
    
    def _create_english_prompt(self) -> PromptTemplate:
        """İngilizce mantık yürütme prompt'u oluşturur"""
        template = """You are given a question about AMIF grant documents, information obtained from relevant documents, and an initial answer.
Analyze this information to create a more detailed, logical, and accurate response.

Question: {question}

Initial Answer: {initial_answer}

Information from Documents:
{context}

Please follow these steps:
1. Analyze the initial answer and check its accuracy
2. Compare it with the information obtained from documents
3. Identify missing, incorrect, or contradictory information
4. Include additional information found in the documents
5. Create a more comprehensive, accurate, and helpful response
6. Add practical advice in the context of AMIF grant processes

Your response should be in English, clear, understandable, and helpful to the user.

Enhanced Answer:"""
        
        return PromptTemplate(
            template=template,
            input_variables=["question", "initial_answer", "context"]
        )
    
    def run(self, question: str, initial_answer: str, context: str, language: str = "tr") -> str:
        """
        Mantık yürütme zincirini çalıştırır
        
        Args:
            question: Soru
            initial_answer: İlk yanıt
            context: Belge bağlamı
            language: Dil kodu ('tr' veya 'en')
            
        Returns:
            Geliştirilmiş yanıt
        """
        try:
            # Dile göre prompt seç
            prompt = self.turkish_prompt if language == "tr" else self.english_prompt
            
            # Prompt'u formatla
            formatted_prompt = prompt.format(
                question=question,
                initial_answer=initial_answer,
                context=context
            )
            
            # LLM'den yanıt al
            response = self.llm.invoke(formatted_prompt)
            
            return response.content if hasattr(response, 'content') else str(response)
            
        except Exception as e:
            error_msg = f"Reasoning chain error: {e}"
            return initial_answer  # Hata durumunda orijinal yanıtı döndür
    
    def enhance_answer_with_sources(self, question: str, answer: str, sources: List[Dict[str, Any]], language: str = "tr") -> str:
        """
        Yanıtı kaynaklarla birlikte geliştirir
        
        Args:
            question: Orijinal soru
            answer: Mevcut yanıt
            sources: Kaynak belgeleri
            language: Dil kodu
            
        Returns:
            Kaynaklar dahil edilmiş geliştirilmiş yanıt
        """
        try:
            # Kaynak bilgilerini oluştur
            source_context = self._format_sources_for_reasoning(sources)
            
            # Reasoning chain'i çalıştır
            enhanced_answer = self.run(
                question=question,
                initial_answer=answer,
                context=source_context,
                language=language
            )
            
            return enhanced_answer
            
        except Exception as e:
            return answer  # Hata durumunda orijinal yanıtı döndür
    
    def _format_sources_for_reasoning(self, sources: List[Dict[str, Any]]) -> str:
        """Kaynakları reasoning için formatlar"""
        formatted_sources = []
        
        for i, source in enumerate(sources, 1):
            content = source.get('content', '')
            metadata = source.get('metadata', {})
            filename = metadata.get('filename', 'Unknown document')
            page = metadata.get('page_number', 'Unknown page')
            
            formatted_source = f"Kaynak {i} ({filename}, Sayfa {page}):\n{content}"
            formatted_sources.append(formatted_source)
        
        return "\n\n".join(formatted_sources) 