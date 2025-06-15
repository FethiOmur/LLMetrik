"""
Mantık yürütme zinciri
"""

from typing import Dict, Any, List
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from config.models import get_llm_model

class ReasoningChain:
    """Mantık yürütme zinciri sınıfı"""
    
    def __init__(self):
        self.llm = get_llm_model()
        self.reasoning_chain = self._create_reasoning_chain()
    
    def _create_reasoning_chain(self) -> LLMChain:
        """Mantık yürütme zinciri oluşturur"""
        template = """
Sana bir soru, bu soruyla ilgili belgelerden elde edilen bilgiler ve bir ilk yanıt veriliyor.
Bu bilgileri analiz ederek daha detaylı ve mantıklı bir yanıt oluştur.

Soru: {question}

İlk Yanıt: {initial_answer}

Belgelerden Elde Edilen Bilgiler:
{context}

Lütfen aşağıdaki adımlari takip et:
1. İlk yanıtı analiz et
2. Belgelerden elde edilen bilgilerle karşılaştır
3. Eksik veya yanlış bilgileri tespit et
4. Daha kapsamlı ve doğru bir yanıt oluştur
5. Yanıtını Türkçe ver

Geliştirilmiş Yanıt:
"""
        
        prompt = PromptTemplate(
            template=template,
            input_variables=["question", "initial_answer", "context"]
        )
        
        return LLMChain(llm=self.llm, prompt=prompt)
    
    def run(self, question: str, initial_answer: str, context: str) -> str:
        """
        Mantık yürütme zincirini çalıştırır
        
        Args:
            question: Soru
            initial_answer: İlk yanıt
            context: Belge bağlamı
            
        Returns:
            Geliştirilmiş yanıt
        """
        result = self.reasoning_chain.run(
            question=question,
            initial_answer=initial_answer,
            context=context
        )
        
        return result 