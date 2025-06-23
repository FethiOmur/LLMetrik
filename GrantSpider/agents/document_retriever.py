"""
Belge arama ajanı
"""

from typing import Dict, Any, List
from agents.base_agent import BaseAgent
from ingestion.vector_store import search_documents, get_collection_info

class DocumentRetrieverAgent(BaseAgent):
    """Belge arama işlemlerini gerçekleştiren ajan"""
    
    def __init__(self, vector_store=None):
        super().__init__(
            name="document_retriever",
            description="Soruya uygun belgeleri vektör veritabanından arar"
        )
        # vector_store parametresi compatibility için, ama kullanmıyoruz
    
    def _detect_language(self, text: str) -> str:
        """
        Basit dil algılama
        
        Args:
            text: Analiz edilecek metin
            
        Returns:
            Dil kodu ('tr', 'en', 'it')
        """
        text_lower = text.lower()
        
        # Türkçe belirteçler
        turkish_indicators = [
            'nedir', 'nelerdir', 'nasıl', 'ne', 'hangi', 'için', 'ile', 'bir', 'bu', 'şu',
            'mı', 'mi', 'mu', 'mü', 'da', 'de', 'ta', 'te', 'la', 'le', 'ın', 'in', 'un', 'ün',
            'hibe', 'başvuru', 'proje', 'belgeler', 'kriterler', 'süreç'
        ]
        
        # İngilizce belirteçler  
        english_indicators = [
            'what', 'how', 'which', 'where', 'when', 'why', 'is', 'are', 'the', 'and', 'or',
            'in', 'on', 'at', 'for', 'with', 'by', 'from', 'to', 'of', 'grant', 'application',
            'project', 'documents', 'criteria', 'process', 'requirements', 'eligibility', 
            'personnel', 'costs', 'budget', 'funding', 'can', 'should', 'must', 'will',
            'this', 'that', 'these', 'those', 'do', 'does', 'did', 'have', 'has', 'had'
        ]
        
        # İtalyanca belirteçler
        italian_indicators = [
            'che', 'cosa', 'come', 'quale', 'dove', 'quando', 'perché', 'è', 'sono', 'il', 'la',
            'di', 'a', 'da', 'in', 'con', 'su', 'per', 'tra', 'fra', 'sovvenzioni', 'domanda',
            'progetto', 'documenti', 'criteri', 'processo'
        ]
        
        # Kelimeleri ayır
        words = text_lower.split()
        
        # Her dil için sayaç - exact match kullan
        tr_score = sum(1 for word in words if word in turkish_indicators)
        en_score = sum(1 for word in words if word in english_indicators)
        it_score = sum(1 for word in words if word in italian_indicators)
        
        print(f"🔍 Dil skorları - TR: {tr_score}, EN: {en_score}, IT: {it_score}")
        print(f"📝 Kelimeler: {words}")
        
        # En yüksek skoru bulan dili döndür
        if tr_score >= en_score and tr_score >= it_score:
            return 'turkish'
        elif en_score >= it_score:
            return 'english' 
        else:
            return 'italian'
    
    def _is_query_relevant(self, query: str, language: str) -> bool:
        """
        Sorgunun grant belgeleri ile ilgili olup olmadığını kontrol eder
        
        Args:
            query: Soru metni
            language: Dil kodu ('tr' veya 'en')
            
        Returns:
            True eğer belge araması yapılması gerekiyorsa, False aksi halde
        """
        # Kişisel selamlaşma ve genel sohbet ifadeleri
        irrelevant_patterns_tr = [
            'merhaba', 'hey', 'selam', 'nasılsın', 'nasıl gidiyor', 
            'günaydın', 'iyi akşamlar', 'teşekkürler', 'sağol',
            'hoşça kal', 'görüşürüz', 'naber', 'ne var ne yok'
        ]
        
        irrelevant_patterns_en = [
            'hello', 'hi', 'hey', 'how are you', 'how is it going',
            'good morning', 'good evening', 'thank you', 'thanks',
            'goodbye', 'see you', 'what\'s up', 'how\'s life'
        ]
        
        query_lower = query.lower().strip()
        
        # Dile göre pattern kontrolü
        if language == 'tr':
            patterns = irrelevant_patterns_tr
        else:
            patterns = irrelevant_patterns_en
        
        # Kısa ve genel sorular (5 kelimeden az)
        words = query_lower.split()
        if len(words) < 3:
            for pattern in patterns:
                if pattern in query_lower:
                    return False
        
        # Grant ile ilgili anahtar kelimeler
        grant_keywords_tr = [
            'grant', 'hibe', 'amif', 'proje', 'başvuru', 'finansman',
            'bütçe', 'maliyet', 'personel', 'eligibility', 'uygunluk',
            'criteria', 'kriter', 'application', 'document', 'belge'
        ]
        
        grant_keywords_en = [
            'grant', 'amif', 'project', 'application', 'funding',
            'budget', 'cost', 'personnel', 'eligibility', 'criteria',
            'documentation', 'requirement', 'guideline', 'procedure'
        ]
        
        all_keywords = grant_keywords_tr + grant_keywords_en
        
        # Grant ile ilgili kelime varlığı kontrolü
        has_grant_keyword = any(keyword in query_lower for keyword in all_keywords)
        
        # Eğer grant kelimesi varsa, kesinlikle ilgili
        if has_grant_keyword:
            return True
        
        # Eğer hiç grant kelimesi yoksa ve kısa ise, büyük ihtimalle ilgisiz
        if len(words) < 5 and not has_grant_keyword:
            return False
        
        # Uzun sorular için varsayılan olarak ilgili kabul et
        return len(words) >= 5

    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Belge arama işlemini gerçekleştirir
        
        Args:
            state: Mevcut durum (query içermeli)
            
        Returns:
            Bulunan belgeler ve güncellenmiş durum
        """
        query = state.get("query", "")
        
        if not query:
            state["retrieved_documents"] = []
            state["retrieval_performed"] = True
            state["detected_language"] = "tr"
            return state
        
        # Basit dil algılama
        detected_language = self._detect_language(query)
        state["detected_language"] = detected_language
        
        # Sorgunun relevansını kontrol et
        if not self._is_query_relevant(query, detected_language):
            print(f"🚫 '{query}' sorgusu grant belgeleri ile ilgili değil, retrieval atlanıyor")
            state["retrieved_documents"] = []
            state["retrieval_performed"] = True
            return state
        
        try:
            # Arama yap
            documents = search_documents(query, k=8)
            
            # Belgeleri dict formatına çevir
            doc_dicts = []
            for doc in documents:
                doc_dict = {
                    "content": doc.page_content,
                    "metadata": doc.metadata
                }
                doc_dicts.append(doc_dict)
            
            # Durumu güncelle
            state["retrieved_documents"] = doc_dicts
            state["retrieval_performed"] = True
            state["detected_language"] = detected_language
            
            print(f"🔍 '{query}' için {len(doc_dicts)} sonuç bulundu")
            print(f"🌐 Algılanan dil: {detected_language}")
            
        except Exception as e:
            print(f"❌ Belge arama hatası: {e}")
            state["retrieved_documents"] = []
            state["retrieval_performed"] = True
            state["detected_language"] = detected_language
        
        return state 