import os
import sys
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template, request, jsonify

# Ana dizini Python path'ine ekle
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.settings import settings
from ingestion.vector_store import get_vector_store, search_documents, get_collection_info, reset_global_vector_store
from agents.qa_agent import QAAgent

app = Flask(__name__, 
           template_folder='templates',
           static_folder='static')

# Global değişkenler
chat_history = []
db_connected = False
db_info = {}
qa_agent = None

def detect_language(text: str) -> str:
    """
    Basit dil algılama fonksiyonu
    
    Args:
        text: Analiz edilecek metin
        
    Returns:
        str: 'tr' veya 'en'
    """
    # Türkçe karakterler ve kelimeler
    turkish_chars = ['ç', 'ğ', 'ı', 'ö', 'ş', 'ü', 'Ç', 'Ğ', 'İ', 'Ö', 'Ş', 'Ü']
    turkish_words = [
        'nedir', 'nasıl', 'neden', 'nerede', 'ne', 'hangi', 'kim', 'kaç', 'kadar',
        'için', 'ile', 'olan', 'olan', 'bir', 'bu', 'şu', 'o', 'ben', 'sen',
        'biz', 'siz', 'onlar', 'var', 'yok', 'evet', 'hayır', 've', 'veya',
        'ama', 'fakat', 'çünkü', 'eğer', 'ise', 'gibi', 'kadar', 'daha',
        'en', 'çok', 'az', 'hiç', 'her', 'bazı', 'tüm', 'hep', 'bazen',
        'hibeleri', 'başvuru', 'kriterleri', 'maliyetleri', 'hesaplanır',
        'belgeleme', 'gereklilikler', 'uygunluk', 'prosedürler'
    ]
    
    # İngilizce kelimeler
    english_words = [
        'what', 'how', 'why', 'where', 'when', 'which', 'who', 'how many', 'how much',
        'for', 'with', 'that', 'this', 'a', 'an', 'the', 'i', 'you', 'we', 'they',
        'is', 'are', 'was', 'were', 'have', 'has', 'had', 'will', 'would', 'can',
        'could', 'should', 'may', 'might', 'must', 'and', 'or', 'but', 'because',
        'if', 'then', 'like', 'than', 'more', 'most', 'very', 'much', 'many',
        'some', 'all', 'every', 'each', 'any', 'no', 'none', 'yes', 'specific',
        'accounting', 'documentation', 'requirements', 'personnel', 'costs',
        'employees', 'daily', 'rate', 'calculated', 'compliance', 'eligibility',
        'standards', 'declaring', 'ensure'
    ]
    
    text_lower = text.lower()
    
    # Türkçe karakter kontrolü
    turkish_char_count = sum(1 for char in text if char in turkish_chars)
    
    # Türkçe kelime kontrolü
    turkish_word_count = sum(1 for word in turkish_words if word in text_lower)
    
    # İngilizce kelime kontrolü
    english_word_count = sum(1 for word in english_words if word in text_lower)
    
    # Karar verme
    turkish_score = turkish_char_count * 2 + turkish_word_count
    english_score = english_word_count
    
    # Eğer Türkçe karakter varsa, büyük ihtimalle Türkçe
    if turkish_char_count > 0:
        return 'tr'
    
    # Kelime sayısına göre karar ver
    if turkish_score > english_score:
        return 'tr'
    elif english_score > turkish_score:
        return 'en'
    else:
        # Varsayılan olarak Türkçe
        return 'tr'

def check_database_connection():
    """Veritabanı bağlantısını kontrol et"""
    global db_connected, db_info, qa_agent
    try:
        # Global vector store instance'ını sıfırla
        reset_global_vector_store()
        
        vector_store = get_vector_store()
        db_info = get_collection_info()
        db_connected = True
        
        # QA Agent'ı başlat
        qa_agent = QAAgent()
        
        print(f"✅ Veritabanı bağlı: {db_info['document_count']} doküman")
        print(f"🤖 QA Agent başlatıldı")
        return True
    except Exception as e:
        print(f"❌ Veritabanı bağlantı hatası: {e}")
        db_connected = False
        db_info = {}
        qa_agent = None
        return False

def search_with_qa_agent(query: str, max_results: int = 8):
    """QA Agent ile akıllı arama yap"""
    try:
        if not db_connected or not qa_agent:
            return None
        
        # Dil algılama
        detected_language = detect_language(query)
        print(f"🌐 Dil algılandı: {detected_language} - Sorgu: '{query[:50]}...'")
        
        # Veritabanından dokümanları al
        results = search_documents(query, max_results)
        
        if not results:
            return {
                'answer': f"'{query}' ile ilgili sonuç bulunamadı. Lütfen farklı anahtar kelimeler deneyin.",
                'sources': [],
                'mode': 'no_results',
                'language': detected_language
            }
        
        # QA Agent için state hazırla
        state = {
            "query": query,
            "retrieved_documents": [
                {
                    "content": doc.page_content,
                    "metadata": doc.metadata
                } for doc in results
            ],
            "detected_language": detected_language
        }
        
        print(f"🤖 QA Agent çalıştırılıyor - Dil: {detected_language}")
        
        # QA Agent'ı çalıştır
        result_state = qa_agent.execute(state)
        
        print(f"✅ QA Agent tamamlandı - Yanıt uzunluğu: {len(result_state.get('qa_response', ''))}")
        
        # Kaynakları formatla
        sources = []
        for doc in results:
            source = doc.metadata.get('source', 'Bilinmeyen kaynak')
            if source != 'Bilinmeyen kaynak':
                source_name = Path(source).stem
            else:
                source_name = source
            sources.append(source_name)
        
        return {
            'answer': result_state.get("qa_response", "Yanıt oluşturulamadı."),
            'sources': sources,
            'mode': 'qa_agent',
            'document_count': len(results),
            'language': detected_language
        }
        
    except Exception as e:
        print(f"❌ QA Agent hatası: {e}")
        return None

def get_demo_response(query: str):
    """Demo yanıtı oluştur"""
    query_lower = query.lower()
    
    if any(word in query_lower for word in ['başvuru', 'application', 'apply']):
        return """AMIF hibeleri için başvuru süreci:

1. **Uygunluk Kontrolü**: Projenizin AMIF kriterlerine uygun olduğundan emin olun
2. **Belge Hazırlığı**: Gerekli tüm belgeleri hazırlayın  
3. **Online Başvuru**: Resmi portal üzerinden başvurunuzu yapın
4. **Değerlendirme**: Başvurunuz uzmanlar tarafından değerlendirilir

*Demo modunda detaylı bilgi sınırlıdır.*"""
    
    elif any(word in query_lower for word in ['entegrasyon', 'integration']):
        return """AMIF Entegrasyon Destekleri:

- **Sosyal Entegrasyon**: Toplumsal uyum projeleri
- **Ekonomik Entegrasyon**: İstihdam ve girişimcilik destekleri  
- **Eğitim Entegrasyonu**: Dil öğrenimi ve mesleki eğitim
- **Kültürel Entegrasyon**: Kültürlerarası diyalog projeleri

*Detaylı bilgi için gerçek veritabanı bağlantısı gereklidir.*"""
    
    elif any(word in query_lower for word in ['bütçe', 'budget', 'funding']):
        return """AMIF Finansman Bilgileri:

- **Proje Bütçeleri**: Değişken tutarlarda destek
- **Eş Finansman**: Genellikle %25 eş finansman gerekli
- **Ödeme Planı**: Avans ve ara ödemeler mevcut
- **Raporlama**: Düzenli mali raporlama zorunlu

*Güncel tutarlar için resmi kaynaklara başvurun.*"""
    
    else:
        return f"""Bu bir demo yanıttır. Sorduğunuz soru: '{query}' 

AMIF Grant Assistant sistemi şu anda veritabanı bağlantısı olmadan çalışmaktadır. 
Gerçek doküman araması için veritabanı bağlantısı gereklidir.

**Örnek sorular:**
- AMIF hibeleri için başvuru kriterleri nelerdir?
- Entegrasyon projeleri için hangi destekler var?
- Başvuru süreçleri nasıl işliyor?"""

@app.route('/')
def index():
    """Ana sayfa"""
    return render_template('index.html')

@app.route('/api/query', methods=['POST'])
def handle_query():
    """Kullanıcı sorgusunu işle"""
    global chat_history
    
    try:
        data = request.get_json()
        user_query = data.get('query', '').strip()
        
        if not user_query:
            return jsonify({
                'success': False,
                'error': 'Boş sorgu gönderilemez'
            })
        
        # QA Agent ile akıllı arama yap
        if db_connected and qa_agent:
            qa_result = search_with_qa_agent(user_query)
            
            if qa_result is None:
                # Hata durumunda demo moda geç
                response = get_demo_response(user_query)
                sources = ["Demo Modu - QA Agent Hatası"]
                mode = 'demo'
                language = 'tr'
            else:
                response = qa_result['answer']
                sources = qa_result['sources']
                mode = qa_result['mode']
                language = qa_result['language']
        else:
            # Demo modu
            response = get_demo_response(user_query)
            sources = [
                "AMIF Programme Manual v1.2 (Demo)",
                "Eligibility Guidelines Document (Demo)",
                "Budget Preparation Instructions (Demo)"
            ]
            mode = 'demo'
            language = detect_language(user_query)
        
        # Chat geçmişine ekle
        chat_entry = {
            'timestamp': datetime.now().isoformat(),
            'query': user_query,
            'response': response,
            'sources': sources,
            'mode': mode,
            'language': language
        }
        chat_history.append(chat_entry)
        
        # Son 50 mesajı tut
        if len(chat_history) > 50:
            chat_history = chat_history[-50:]
        
        return jsonify({
            'success': True,
            'response': response,
            'sources': sources,
            'timestamp': chat_entry['timestamp'],
            'mode': mode,
            'language': language
        })
        
    except Exception as e:
        print(f"❌ Sorgu işleme hatası: {e}")
        return jsonify({
            'success': False,
            'error': f'Sorgu işlenirken hata oluştu: {str(e)}'
        })

@app.route('/api/history')
def get_history():
    """Chat geçmişini getir"""
    return jsonify({
        'success': True,
        'history': chat_history[-20:]  # Son 20 mesajı gönder
    })

@app.route('/api/clear_history', methods=['POST'])
def clear_history():
    """Chat geçmişini temizle"""
    global chat_history
    chat_history = []
    return jsonify({
        'success': True,
        'message': 'Geçmiş temizlendi'
    })

@app.route('/api/status')
def get_status():
    """Sistem durumunu kontrol et"""
    # Güncel veritabanı bilgisini al
    current_db_info = {}
    current_document_count = 0
    
    if db_connected:
        try:
            current_db_info = get_collection_info()
            current_document_count = current_db_info.get('document_count', 0)
        except Exception as e:
            print(f"⚠️  Status kontrolünde veritabanı bilgisi alınamadı: {e}")
            current_document_count = db_info.get('document_count', 0)
    
    return jsonify({
        'success': True,
        'status': {
            'system_ready': True,
            'vector_db_ready': db_connected,
            'qa_agent_ready': qa_agent is not None,
            'document_count': current_document_count,
            'chat_history_count': len(chat_history),
            'database_mode': 'connected' if db_connected else 'demo',
            'embedding_model': current_db_info.get('embedding_model', db_info.get('embedding_model', 'N/A')) if db_connected else 'N/A'
        }
    })

if __name__ == '__main__':
    print(f"\n🌐 AMIF Grant Assistant Web Arayüzü başlatılıyor...")
    
    # Veritabanı bağlantısını kontrol et
    check_database_connection()
    
    print(f"📍 Adres: http://localhost:3000")
    print(f"🚀 Web Arayüzü Hazır!")
    print(f"📊 Veritabanı durumu: {'Bağlı' if db_connected else 'Demo Modu'}")
    print(f"🤖 QA Agent durumu: {'Aktif' if qa_agent else 'Pasif'}")
    print(f"🌐 Dil algılama: Aktif")
    
    if db_connected:
        print(f"📄 Toplam doküman: {db_info.get('document_count', 'Bilinmiyor')}")
        print(f"🤖 Embedding modeli: {db_info.get('embedding_model', 'N/A')}")
    
    print(f"⚪ Siyah-Gri-Beyaz tema aktif")
    print(f"\nTarayıcınızda http://localhost:3000 adresini açın")
    
    app.run(
        host='0.0.0.0',
        port=3000,
        debug=False,
        threaded=True
    )