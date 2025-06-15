"""
LangGraph düğümlerinin tanımları
"""

from typing import Dict, Any, Literal
from langgraph.types import Command
from memory.state_manager import MultiAgentState
from agents.document_retriever import DocumentRetrieverAgent
from agents.qa_agent import QAAgent
from agents.source_tracker import SourceTrackerAgent
from agents.supervisor import SupervisorAgent

# Global ajan instanceları
document_retriever_agent = None
qa_agent = None
source_tracker_agent = None
supervisor_agent = None

def initialize_agents(vector_store):
    """Ajanları başlatır"""
    global document_retriever_agent, qa_agent, source_tracker_agent, supervisor_agent
    
    document_retriever_agent = DocumentRetrieverAgent(vector_store)
    qa_agent = QAAgent()
    source_tracker_agent = SourceTrackerAgent()
    supervisor_agent = SupervisorAgent()

def supervisor_node(state: MultiAgentState) -> Command[Literal["document_retriever", "qa_agent", "source_tracker", "__end__"]]:
    """
    Supervisor düğümü - Diğer ajanları koordine eder
    
    Args:
        state: Mevcut durum
        
    Returns:
        Sonraki ajanı gösteren Command
    """
    state_dict = {
        "query": state.query,
        "retrieval_performed": state.retrieval_performed,
        "qa_performed": state.qa_performed,
        "source_tracking_performed": state.source_tracking_performed
    }
    
    command = supervisor_agent.execute(state_dict)
    return command

def document_retriever_node(state: MultiAgentState) -> MultiAgentState:
    """
    Belge arama düğümü
    
    Args:
        state: Mevcut durum
        
    Returns:
        Güncellenmiş durum
    """
    state_dict = {
        "query": state.query,
        "retrieved_documents": state.retrieved_documents,
        "retrieval_performed": state.retrieval_performed
    }
    
    updated_state = document_retriever_agent.execute(state_dict)
    
    # Durumu güncelle
    state.retrieved_documents = updated_state.get("retrieved_documents", [])
    state.retrieval_performed = updated_state.get("retrieval_performed", False)
    
    return state

def qa_agent_node(state: MultiAgentState) -> MultiAgentState:
    """
    QA düğümü
    
    Args:
        state: Mevcut durum
        
    Returns:
        Güncellenmiş durum
    """
    state_dict = {
        "query": state.query,
        "retrieved_documents": state.retrieved_documents,
        "qa_response": state.qa_response,
        "qa_performed": state.qa_performed
    }
    
    updated_state = qa_agent.execute(state_dict)
    
    # Durumu güncelle
    state.qa_response = updated_state.get("qa_response", "")
    state.qa_performed = updated_state.get("qa_performed", False)
    
    return state

def source_tracker_node(state: MultiAgentState) -> MultiAgentState:
    """
    Kaynak takip düğümü
    
    Args:
        state: Mevcut durum
        
    Returns:
        Güncellenmiş durum
    """
    state_dict = {
        "retrieved_documents": state.retrieved_documents,
        "qa_response": state.qa_response,
        "sources": state.sources,
        "cited_response": state.cited_response,
        "source_tracking_performed": state.source_tracking_performed
    }
    
    updated_state = source_tracker_agent.execute(state_dict)
    
    # Durumu güncelle
    state.sources = updated_state.get("sources", [])
    state.cited_response = updated_state.get("cited_response", "")
    state.source_tracking_performed = updated_state.get("source_tracking_performed", False)
    
    return state 