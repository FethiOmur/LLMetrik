#!/usr/bin/env python3
"""
Streamlit Web Arayüzü - AMIF Grant Assistant
"""

import streamlit as st
import os
import sys
from datetime import datetime
from typing import List, Dict, Any

# Proje kök dizinini Python path'ine ekle
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from ingestion.vector_store import get_vector_store, get_collection_info, search_documents
from agents.qa_agent import QAAgent

# Sayfa konfigürasyonu
st.set_page_config(
    page_title="AMIF Grant Assistant",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS stilleri
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .source-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
    }
    .question-box {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .answer-box {
        background-color: #f0f9ff;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #10b981;
        margin: 1rem 0;
    }
    .metric-card {
        background-color: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def initialize_system():
    """Sistemi başlatır ve cache'ler"""
    try:
        # Vector store'u başlat
        vector_store = get_vector_store()
        
        # QA Agent'ı başlat
        qa_agent = QAAgent()
        
        # Collection bilgilerini al
        info = get_collection_info()
        document_count = info.get("document_count", 0)
        
        return vector_store, qa_agent, document_count
    except Exception as e:
        st.error(f"Sistem başlatılırken hata: {e}")
        return None, None, 0

def format_sources(documents: List[Any]) -> str:
    """Kaynakları HTML formatında formatlar"""
    if not documents:
        return "<p>Kaynak bulunamadı</p>"
    
    sources_html = ""
    for i, doc in enumerate(documents, 1):
        metadata = doc.metadata if hasattr(doc, 'metadata') else {}
        filename = metadata.get('filename', 'Bilinmeyen kaynak')
        page_number = metadata.get('page_number', 'Bilinmeyen sayfa')
        
        # Dosya adını kısalt
        if len(filename) > 60:
            filename = filename[:57] + "..."
        
        sources_html += f"""
        <div class="source-box">
            <strong>[{i}]</strong> {filename}<br>
            <small>📄 Sayfa: {page_number}</small>
        </div>
        """
    
    return sources_html

def process_question(vector_store, qa_agent, question: str) -> Dict[str, Any]:
    """Soruyu işler ve yanıt döndürür"""
    try:
        # Vector store'dan arama yap
        documents = search_documents(question, k=8)
        detected_language = "tr"  # Varsayılan Türkçe
        
        if not documents:
            return {
                "answer": "Sorunuzla ilgili bilgi bulunamadı. Lütfen farklı kelimeler kullanarak tekrar deneyin.",
                "sources": [],
                "language": detected_language,
                "document_count": 0
            }
        
        # QA Agent ile yanıt oluştur
        state = {
            "query": question,
            "retrieved_documents": [
                {
                    "content": doc.page_content,
                    "metadata": doc.metadata
                } for doc in documents
            ],
            "detected_language": detected_language
        }
        
        # QA Agent'ı çalıştır
        result_state = qa_agent.execute(state)
        
        return {
            "answer": result_state.get("qa_response", "Yanıt oluşturulamadı."),
            "sources": documents,
            "language": detected_language,
            "document_count": len(documents)
        }
        
    except Exception as e:
        return {
            "answer": f"Hata oluştu: {e}",
            "sources": [],
            "language": "tr",
            "document_count": 0
        }

def main():
    """Ana uygulama"""
    
    # Başlık
    st.markdown("""
    <div class="main-header">
        <h1>🚀 AMIF Grant Assistant</h1>
        <p>Akıllı Hibe Danışman Sistemi</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sistem başlatma
    vector_store, qa_agent, total_documents = initialize_system()
    
    if not vector_store or not qa_agent:
        st.error("❌ Sistem başlatılamadı. Lütfen sayfayı yenileyin.")
        return
    
    # Sidebar
    with st.sidebar:
        st.header("📊 Sistem Durumu")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>{total_documents:,}</h3>
                <p>Toplam Belge</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3>8</h3>
                <p>Kaynak Sayısı</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.header("💡 Örnek Sorular")
        
        example_questions = [
            "AMIF hibesi nedir?",
            "What are the eligibility criteria?",
            "Personel maliyetleri nasıl hesaplanır?",
            "How to calculate daily rates?",
            "Proje süresi ne kadar olabilir?",
            "What is the maximum grant amount?",
            "Başvuru süreci nasıl işler?",
            "Required documentation for application?"
        ]
        
        for question in example_questions:
            if st.button(question, key=f"example_{question}", use_container_width=True):
                st.session_state.example_question = question
        
        st.markdown("---")
        st.markdown("### 🔧 Özellikler")
        st.markdown("""
        - 🌍 **Çok dilli**: Türkçe ve İngilizce
        - 🎯 **Akıllı arama**: 8 kaynak ile detaylı yanıtlar
        - 📄 **Sayfa referansları**: Her kaynak için sayfa numarası
        - ⚡ **Hızlı yanıt**: ~2-3 saniye
        """)
    
    # Ana içerik alanı
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🤔 Sorunuzu Sorun")
        
        # Örnek sorudan gelen input'u kontrol et
        default_question = ""
        if hasattr(st.session_state, 'example_question'):
            default_question = st.session_state.example_question
            del st.session_state.example_question
        
        # Soru input alanı
        question = st.text_area(
            "Sorunuzu buraya yazın:",
            value=default_question,
            height=100,
            placeholder="Örnek: AMIF hibesi için uygunluk kriterleri nelerdir?"
        )
        
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
        
        with col_btn1:
            ask_button = st.button("🔍 Sor", type="primary", use_container_width=True)
        
        with col_btn2:
            clear_button = st.button("🗑️ Temizle", use_container_width=True)
        
        if clear_button:
            st.rerun()
        
        # Soru işleme
        if ask_button and question.strip():
            with st.spinner("🔍 Aranıyor ve yanıt hazırlanıyor..."):
                result = process_question(vector_store, qa_agent, question.strip())
            
            # Soruyu göster
            st.markdown(f"""
            <div class="question-box">
                <strong>❓ Soru:</strong> {question}
            </div>
            """, unsafe_allow_html=True)
            
            # Yanıtı göster
            st.markdown(f"""
            <div class="answer-box">
                <strong>💡 Yanıt:</strong><br><br>
                {result['answer']}
            </div>
            """, unsafe_allow_html=True)
            
            # Dil bilgisi
            language_flag = "🇹🇷" if result['language'] == 'tr' else "🇺🇸"
            st.info(f"{language_flag} Algılanan dil: {'Türkçe' if result['language'] == 'tr' else 'İngilizce'}")
            
            # Kaynakları göster
            if result['sources']:
                st.markdown("### 📚 Kaynaklar")
                st.markdown(f"**{result['document_count']} kaynak bulundu:**")
                
                sources_html = format_sources(result['sources'])
                st.markdown(sources_html, unsafe_allow_html=True)
            else:
                st.warning("📭 Bu soru için kaynak bulunamadı.")
    
    with col2:
        st.header("📈 İstatistikler")
        
        # Session state'te soru sayacı
        if 'question_count' not in st.session_state:
            st.session_state.question_count = 0
        
        if ask_button and question.strip():
            st.session_state.question_count += 1
        
        st.metric("Sorulan Soru", st.session_state.question_count)
        st.metric("Aktif Belge", f"{total_documents:,}")
        st.metric("Sistem Durumu", "🟢 Aktif")
        
        st.markdown("---")
        
        st.header("ℹ️ Bilgi")
        st.info("""
        **AMIF Grant Assistant**, Avrupa Birliği'nin Asylum, Migration and Integration Fund (AMIF) 
        hibe programı hakkında sorularınızı yanıtlayan akıllı bir asistan sistemidir.
        
        Sistem, 49 resmi AMIF belgesini analiz ederek size en doğru ve güncel bilgileri sunar.
        """)
        
        st.markdown("---")
        
        st.header("🚀 Nasıl Kullanılır?")
        st.markdown("""
        1. **Soru sorun**: Sol taraftaki alana sorunuzu yazın
        2. **Dil seçin**: Türkçe veya İngilizce sorabilirsiniz
        3. **Yanıt alın**: Sistem otomatik olarak en uygun yanıtı bulur
        4. **Kaynakları inceleyin**: Her yanıt için kaynak belgeleri gösterilir
        """)

if __name__ == "__main__":
    main() 