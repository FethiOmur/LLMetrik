"""
Main graph compilation module
"""

from typing import Dict, Any
from graph.multi_agent_graph import MultiAgentGraph
from ingestion.vector_store import get_vector_store

def compile_graph() -> MultiAgentGraph:
    """
    Compiles and returns the main graph
    
    Returns:
        Compiled MultiAgentGraph instance
    """
    try:
        # Get vector store
        vector_store = get_vector_store()
        
        # Create graph
        graph = MultiAgentGraph(vector_store)
        
        print("✅ Graph compiled successfully")
        return graph
        
    except Exception as e:
        print(f"❌ Graph compilation error: {e}")
        raise e

def get_graph_status() -> Dict[str, Any]:
    """
    Checks graph status
    
    Returns:
        Graph status information
    """
    try:
        graph = compile_graph()
        return {
            "status": "ready",
            "graph_available": True,
            "message": "Graph ready"
        }
    except Exception as e:
        return {
            "status": "error",
            "graph_available": False,
            "message": f"Graph error: {str(e)}"
        } 