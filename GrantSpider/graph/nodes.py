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
from agents.cross_document_agent import CrossDocumentAgent

# Global ajan instanceları
document_retriever_agent = None
qa_agent = None
source_tracker_agent = None
cross_document_agent = None
supervisor_agent = None

def initialize_agents(vector_store):
    """Ajanları başlatır"""
    global document_retriever_agent, qa_agent, source_tracker_agent, cross_document_agent, supervisor_agent
    
    document_retriever_agent = DocumentRetrieverAgent(vector_store)
    qa_agent = QAAgent()
    source_tracker_agent = SourceTrackerAgent()
    cross_document_agent = CrossDocumentAgent()
    supervisor_agent = SupervisorAgent()

def supervisor_node(state: MultiAgentState) -> Command[Literal["document_retriever", "qa_agent", "cross_document", "source_tracker", "__end__"]]:
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
        "cross_document_performed": state.cross_document_performed,
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
        "retrieval_performed": state.retrieval_performed,
        "detected_language": state.detected_language
    }
    
    updated_state = document_retriever_agent.execute(state_dict)
    
    # Durumu güncelle
    state.retrieved_documents = updated_state.get("retrieved_documents", [])
    state.retrieval_performed = updated_state.get("retrieval_performed", False)
    state.detected_language = updated_state.get("detected_language", "tr")
    
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
        "qa_performed": state.qa_performed,
        "detected_language": state.detected_language
    }
    
    updated_state = qa_agent.execute(state_dict)
    
    # Durumu güncelle
    state.qa_response = updated_state.get("qa_response", "")
    state.qa_performed = updated_state.get("qa_performed", False)
    
    return state

def cross_document_node(state: MultiAgentState) -> MultiAgentState:
    """
    Cross-document analiz düğümü
    
    Args:
        state: Mevcut durum
        
    Returns:
        Güncellenmiş durum
    """
    state_dict = {
        "query": state.query,
        "retrieved_documents": state.retrieved_documents,
        "cross_document_analysis": state.cross_document_analysis,
        "cross_document_performed": state.cross_document_performed
    }
    
    updated_state = cross_document_agent.execute(state_dict)
    
    # Durumu güncelle
    state.cross_document_analysis = updated_state.get("cross_document_analysis", {})
    state.cross_document_performed = updated_state.get("cross_document_performed", False)
    
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