"""
Streamlit web arayüzü
"""

import streamlit as st
import uuid
from typing import Dict, Any
from graph.multi_agent_graph import MultiAgentGraph
from ingestion.vector_store import VectorStore
from memory.conversation_memory import ConversationMemory

# Sayfa yapılandırması
st.set_page_config(
    page_title="GrantSpider Chatbot",
    page_icon="🕷️",
    layout="wide"
)

@st.cache_resource
def load_multi_agent_system():
    """Çoklu ajan sistemini yükler (cache'li)"""
    vector_store = VectorStore()
    return MultiAgentGraph(vector_store)

def initialize_session_state():
    """Session state'i başlatır"""
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    
    if "conversation_memory" not in st.session_state:
        st.session_state.conversation_memory = ConversationMemory()
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

def main():
    """Ana uygulama"""
    st.title("🕷️ GrantSpider Chatbot")
    st.subheader("Grant Belgeleriniz için AI Asistan")
    
    # Session state başlat
    initialize_session_state()
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Ayarlar")
        
        # Session bilgileri
        st.info(f"Session ID: {st.session_state.session_id[:8]}...")
        
        # Sohbeti temizle butonu
        if st.button("🗑️ Sohbeti Temizle"):
            st.session_state.messages = []
            st.session_state.conversation_memory.clear_history()
            st.rerun()
        
        # Sistem durumu
        st.header("📊 Sistem Durumu")
        try:
            multi_agent_graph = load_multi_agent_system()
            st.success("✅ Sistem hazır")
        except Exception as e:
            st.error(f"❌ Sistem hatası: {e}")
            return
    
    # Ana sohbet alanı
    st.header("💬 Sohbet")
    
    # Sohbet geçmişini göster
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Kaynak bilgilerini göster
            if message["role"] == "assistant" and "sources" in message:
                with st.expander("📚 Kaynaklar"):
                    for i, source in enumerate(message["sources"], 1):
                        st.write(f"{i}. {source.get('filename', 'Bilinmeyen')}")
    
    # Kullanıcı girişi
    if prompt := st.chat_input("Grant belgeleri hakkında sorunuzu yazın..."):
        # Kullanıcı mesajını ekle
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.conversation_memory.add_user_message(prompt)
        
        # Kullanıcı mesajını göster
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Asistan yanıtını oluştur
        with st.chat_message("assistant"):
            with st.spinner("🔍 Belgeler aranıyor ve yanıt oluşturuluyor..."):
                try:
                    # Çoklu ajan sistemini çalıştır
                    result = multi_agent_graph.run(prompt, st.session_state.session_id)
                    
                    # Yanıtı al
                    response = result.get("cited_response", result.get("qa_response", "Yanıt bulunamadı."))
                    sources = result.get("sources", [])
                    
                    # Yanıtı göster
                    st.markdown(response)
                    
                    # Kaynak bilgilerini göster
                    if sources:
                        with st.expander("📚 Kaynaklar"):
                            for i, source in enumerate(sources, 1):
                                filename = source.get('filename', 'Bilinmeyen')
                                similarity_score = source.get('similarity_score', 0.0)
                                st.write(f"{i}. **{filename}** (Benzerlik: {similarity_score:.2f})")
                    
                    # Mesajı session state'e ekle
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": response,
                        "sources": sources
                    })
                    
                    # Conversation memory'ye ekle
                    st.session_state.conversation_memory.add_assistant_message(response)
                    
                except Exception as e:
                    error_msg = f"❌ Hata oluştu: {e}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

def upload_documents_page():
    """Belge yükleme sayfası"""
    st.title("📁 Belge Yükleme")
    st.subheader("PDF dosyalarınızı sisteme yükleyin")
    
    uploaded_files = st.file_uploader(
        "PDF dosyalarını seçin",
        type=['pdf'],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        if st.button("📤 Belgeleri Yükle"):
            try:
                from ingestion.pdf_loader import PDFLoader
                from ingestion.text_processor import TextProcessor
                
                with st.progress(0) as progress_bar:
                    # PDF'leri geçici olarak kaydet ve yükle
                    progress_bar.progress(25)
                    
                    # İlerleme göstergesi ile belgeler işle
                    st.info("📂 PDF dosyaları işleniyor...")
                    progress_bar.progress(50)
                    
                    st.info("✂️ Metinler parçalara bölünüyor...")
                    progress_bar.progress(75)
                    
                    st.info("🗃️ Vektör veritabanına ekleniyor...")
                    progress_bar.progress(100)
                
                st.success("🎉 Belgeler başarıyla yüklendi!")
                
            except Exception as e:
                st.error(f"❌ Hata: {e}")

# Sayfa navigasyonu
pages = {
    "💬 Sohbet": main,
    "📁 Belge Yükleme": upload_documents_page
}

# Sidebar navigasyon
selected_page = st.sidebar.selectbox("Sayfa Seçin", list(pages.keys()))

# Seçilen sayfayı çalıştır
pages[selected_page]()

if __name__ == "__main__":
    main() 