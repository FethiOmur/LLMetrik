"""
LangGraph çoklu ajan yapısı
"""

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from memory.state_manager import MultiAgentState
from graph.nodes import (
    supervisor_node,
    document_retriever_node,
    qa_agent_node,
    cross_document_node,
    source_tracker_node,
    initialize_agents
)

class MultiAgentGraph:
    """LangGraph çoklu ajan sistemi"""
    
    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.graph = None
        self._build_graph()
    
    def _build_graph(self):
        """Graf yapısını oluşturur"""
        # Ajanları başlat
        initialize_agents(self.vector_store)
        
        # StateGraph oluştur
        builder = StateGraph(MultiAgentState)
        
        # Düğümleri ekle
        builder.add_node("supervisor", supervisor_node)
        builder.add_node("document_retriever", document_retriever_node)
        builder.add_node("cross_document", cross_document_node)
        builder.add_node("qa_agent", qa_agent_node)
        builder.add_node("source_tracker", source_tracker_node)
        
        # Graf kenarlarını tanımla
        builder.add_edge(START, "supervisor")
        builder.add_edge("document_retriever", "supervisor")
        builder.add_edge("cross_document", "supervisor")
        builder.add_edge("qa_agent", "supervisor")
        builder.add_edge("source_tracker", "supervisor")
        
        # Memory checkpointer ekle (basit in-memory)
        memory = MemorySaver()
        
        # Graf'ı derle
        self.graph = builder.compile(checkpointer=memory)
    
    def run(self, query: str, session_id: str = "default") -> dict:
        """
        Graf'ı çalıştırır
        
        Args:
            query: Kullanıcı sorgusu
            session_id: Session kimliği
            
        Returns:
            Graf sonucu
        """
        # İlk durumu oluştur
        initial_state = MultiAgentState(
            query=query,
            session_id=session_id
        )
        
        # Graf'ı çalıştır
        config = {"configurable": {"thread_id": session_id}}
        
        result = self.graph.invoke(initial_state, config=config)
        
        return {
            "query": result.get("query", query),
            "qa_response": result.get("qa_response", ""),
            "cited_response": result.get("cited_response", ""),
            "sources": result.get("sources", []),
            "retrieved_documents": result.get("retrieved_documents", []),
            "cross_document_analysis": result.get("cross_document_analysis", {}),
            "detected_language": result.get("detected_language", "tr")
        }
    
    def stream(self, query: str, session_id: str = "default"):
        """
        Graf'ı streaming modunda çalıştırır
        
        Args:
            query: Kullanıcı sorgusu
            session_id: Session kimliği
            
        Yields:
            Graf adımları
        """
        # İlk durumu oluştur
        initial_state = MultiAgentState(
            query=query,
            session_id=session_id
        )
        
        # Graf'ı streaming mode'da çalıştır
        config = {"configurable": {"thread_id": session_id}}
        
        for step in self.graph.stream(initial_state, config=config):
            yield step
    
    def get_graph_image(self) -> bytes:
        """
        Graf görselini döndürür
        
        Returns:
            Graf görseli (PNG bytes)
        """
        try:
            return self.graph.get_graph().draw_mermaid_png()
        except Exception as e:
            print(f"Graf görseli oluşturulamadı: {e}")
            return None 