"""
Sohbet bellek yönetimi
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from config.settings import settings

class ConversationMemory:
    """Sohbet geçmişini yöneten sınıf"""
    
    def __init__(self, max_history: int = None):
        self.max_history = max_history or settings.MAX_CHAT_HISTORY
        self.conversation_history: List[Dict[str, Any]] = []
        self.session_id: Optional[str] = None
    
    def add_user_message(self, message: str, metadata: Dict[str, Any] = None):
        """
        Kullanıcı mesajı ekler
        
        Args:
            message: Kullanıcı mesajı
            metadata: Ek bilgiler
        """
        self._add_message("user", message, metadata)
    
    def add_assistant_message(self, message: str, metadata: Dict[str, Any] = None):
        """
        Asistan mesajı ekler
        
        Args:
            message: Asistan mesajı
            metadata: Ek bilgiler
        """
        self._add_message("assistant", message, metadata)
    
    def _add_message(self, role: str, content: str, metadata: Dict[str, Any] = None):
        """
        Mesaj ekler ve geçmişi yönetir
        
        Args:
            role: Mesaj rolü (user/assistant)
            content: Mesaj içeriği
            metadata: Ek bilgiler
        """
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        
        self.conversation_history.append(message)
        
        # Maksimum geçmiş sınırını kontrol et
        if len(self.conversation_history) > self.max_history:
            self.conversation_history = self.conversation_history[-self.max_history:]
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """
        Sohbet geçmişini döndürür
        
        Returns:
            Sohbet geçmişi listesi
        """
        return self.conversation_history.copy()
    
    def get_recent_messages(self, count: int = 5) -> List[Dict[str, Any]]:
        """
        Son N mesajı döndürür
        
        Args:
            count: Döndürülecek mesaj sayısı
            
        Returns:
            Son mesajlar listesi
        """
        return self.conversation_history[-count:] if self.conversation_history else []
    
    def get_context_string(self, include_metadata: bool = False) -> str:
        """
        Sohbet geçmişini string formatında döndürür
        
        Args:
            include_metadata: Metadata'ları dahil et
            
        Returns:
            Formatlanmış sohbet geçmişi
        """
        context_parts = []
        
        for message in self.conversation_history:
            role = message["role"]
            content = message["content"]
            timestamp = message["timestamp"]
            
            part = f"[{timestamp}] {role.upper()}: {content}"
            
            if include_metadata and message.get("metadata"):
                part += f" (Metadata: {message['metadata']})"
            
            context_parts.append(part)
        
        return "\n".join(context_parts)
    
    def clear_history(self):
        """Sohbet geçmişini temizler"""
        self.conversation_history.clear()
    
    def set_session_id(self, session_id: str):
        """
        Session ID belirler
        
        Args:
            session_id: Session kimliği
        """
        self.session_id = session_id
    
    def get_session_id(self) -> Optional[str]:
        """
        Session ID döndürür
        
        Returns:
            Session kimliği
        """
        return self.session_id 