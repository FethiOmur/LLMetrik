"""
Ana graf derleme modülü
"""

from typing import Dict, Any
from graph.multi_agent_graph import MultiAgentGraph
from ingestion.vector_store import get_vector_store

def compile_graph() -> MultiAgentGraph:
    """
    Ana graf'ı derler ve döndürür
    
    Returns:
        Derlenmiş MultiAgentGraph instance'ı
    """
    try:
        # Vector store'u al
        vector_store = get_vector_store()
        
        # Graf'ı oluştur
        graph = MultiAgentGraph(vector_store)
        
        print("✅ Graf başarıyla derlendi")
        return graph
        
    except Exception as e:
        print(f"❌ Graf derleme hatası: {e}")
        raise e

def get_graph_status() -> Dict[str, Any]:
    """
    Graf durumunu kontrol eder
    
    Returns:
        Graf durum bilgisi
    """
    try:
        graph = compile_graph()
        return {
            "status": "ready",
            "graph_available": True,
            "message": "Graf hazır"
        }
    except Exception as e:
        return {
            "status": "error",
            "graph_available": False,
            "message": f"Graf hatası: {str(e)}"
        } 