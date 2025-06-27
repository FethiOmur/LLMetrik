"""
LangGraph multi-agent structure
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
    """LangGraph multi-agent system"""
    
    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.graph = None
        self._build_graph()
    
    def _build_graph(self):
        """Builds graph structure"""
        # Initialize agents
        initialize_agents(self.vector_store)
        
        # Create StateGraph
        builder = StateGraph(MultiAgentState)
        
        # Add nodes
        builder.add_node("supervisor", supervisor_node)
        builder.add_node("document_retriever", document_retriever_node)
        builder.add_node("cross_document", cross_document_node)
        builder.add_node("qa_agent", qa_agent_node)
        builder.add_node("source_tracker", source_tracker_node)
        
        # Define graph edges
        builder.add_edge(START, "supervisor")
        builder.add_edge("document_retriever", "supervisor")
        builder.add_edge("cross_document", "supervisor")
        builder.add_edge("qa_agent", "supervisor")
        builder.add_edge("source_tracker", "supervisor")
        
        # Add memory checkpointer (simple in-memory)
        memory = MemorySaver()
        
        # Compile graph
        self.graph = builder.compile(checkpointer=memory)
    
    def run(self, query: str, session_id: str = "default") -> dict:
        """
        Runs the graph
        
        Args:
            query: User query
            session_id: Session identifier
            
        Returns:
            Graph result
        """
        # Create initial state
        initial_state = MultiAgentState(
            query=query,
            session_id=session_id
        )
        
        # Run graph
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
        Runs graph in streaming mode
        
        Args:
            query: User query
            session_id: Session identifier
            
        Yields:
            Graph steps
        """
        # Create initial state
        initial_state = MultiAgentState(
            query=query,
            session_id=session_id
        )
        
        # Run graph in streaming mode
        config = {"configurable": {"thread_id": session_id}}
        
        for step in self.graph.stream(initial_state, config=config):
            yield step
    
    def get_graph_image(self) -> bytes:
        """
        Returns graph visualization
        
        Returns:
            Graph visualization (PNG bytes)
        """
        try:
            return self.graph.get_graph().draw_mermaid_png()
        except Exception as e:
            print(f"Could not create graph visualization: {e}")
            return None 