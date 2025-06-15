"""
Kaynak takip ajanı
"""

from typing import Dict, Any, List
from agents.base_agent import BaseAgent

class SourceTrackerAgent(BaseAgent):
    """Kaynak atıflarını takip eden ajan"""
    
    def __init__(self):
        super().__init__(
            name="source_tracker",
            description="Yanıtlarda kullanılan kaynakları takip eder ve atıfları yönetir"
        )
    
    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Kaynak takibi yapar
        
        Args:
            state: Mevcut durum
            
        Returns:
            Kaynak bilgileri ve güncellenmiş durum
        """
        retrieved_documents = state.get("retrieved_documents", [])
        qa_response = state.get("qa_response", "")
        
        if not retrieved_documents:
            return state
        
        # Kaynak bilgilerini çıkar
        sources = self._extract_sources(retrieved_documents)
        
        # Kaynak atıflı yanıt oluştur
        cited_response = self._add_citations(qa_response, sources)
        
        # Durumu güncelle
        state["sources"] = sources
        state["cited_response"] = cited_response
        state["source_tracking_performed"] = True
        
        return state
    
    def _extract_sources(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Belgelerden kaynak bilgilerini çıkarır
        
        Args:
            documents: Belgeler listesi
            
        Returns:
            Kaynak bilgileri listesi
        """
        sources = []
        seen_sources = set()
        
        for doc in documents:
            metadata = doc.get("metadata", {})
            filename = metadata.get("filename", "")
            source_path = metadata.get("source", "")
            
            # Aynı kaynağı tekrar ekleme
            source_key = (filename, source_path)
            if source_key in seen_sources:
                continue
            
            seen_sources.add(source_key)
            
            sources.append({
                "filename": filename,
                "source_path": source_path,
                "chunk_index": metadata.get("chunk_index", 0),
                "similarity_score": doc.get("similarity_score", 0.0)
            })
        
        return sources
    
    def _add_citations(self, response: str, sources: List[Dict[str, Any]]) -> str:
        """
        Yanıta kaynak atıfları ekler
        
        Args:
            response: Orijinal yanıt
            sources: Kaynak listesi
            
        Returns:
            Kaynak atıflı yanıt
        """
        if not sources:
            return response
        
        citation_text = "\n\n**Kaynaklar:**\n"
        for i, source in enumerate(sources, 1):
            filename = source.get("filename", "Bilinmeyen")
            citation_text += f"{i}. {filename}\n"
        
        return response + citation_text
    
    def get_source_summary(self, sources: List[Dict[str, Any]]) -> str:
        """
        Kaynak özetini döndürür
        
        Args:
            sources: Kaynak listesi
            
        Returns:
            Kaynak özeti
        """
        if not sources:
            return "Hiç kaynak bulunamadı."
        
        unique_files = set(source.get("filename", "") for source in sources)
        return f"Toplam {len(sources)} chunk, {len(unique_files)} farklı belgeden kullanıldı." 