"""
AMIF Grant Assistant - Web Arayüzü
Flask tabanlı kullanıcı arayüzü
"""

import sys
import os
from pathlib import Path

# Ana dizini Python path'ine ekle
sys.path.insert(0, str(Path(__file__).parent.parent))

from flask import Flask, render_template, request, jsonify
from config.settings import settings
from ingestion.vector_store import get_vector_store, search_documents, get_collection_info

app = Flask(__name__, 
           template_folder='../templates',
           static_folder='../static')

# Global değişkenler
db_connected = False
db_info = {}

def check_database_connection():
    """Veritabanı bağlantısını kontrol et"""
    global db_connected, db_info
    try:
        # Vector store'u test et
        vector_store = get_vector_store()
        db_info = get_collection_info()
        db_connected = True
        print(f"✅ Veritabanı bağlantısı başarılı: {db_info['document_count']} doküman")
        return True
    except Exception as e:
        print(f"❌ Veritabanı bağlantı hatası: {e}")
        db_connected = False
        db_info = {}
        return False

def search_in_database(query: str, max_results: int = 5):
    """Veritabanında arama yap"""
    try:
        if not db_connected:
            return None
        
        results = search_documents(query, max_results)
        
        if not results:
            return []
        
        formatted_results = []
        for i, result in enumerate(results, 1):
            content = result.page_content[:500] + "..." if len(result.page_content) > 500 else result.page_content
            source = result.metadata.get('source', 'Bilinmeyen kaynak')
            
            formatted_results.append({
                'rank': i,
                'content': content,
                'source': source,
                'metadata': result.metadata
            })
        
        return formatted_results
        
    except Exception as e:
        print(f"❌ Arama hatası: {e}")
        return None

def get_demo_response(query: str):
    """Demo yanıtı döndür"""
    demo_responses = {
        "default": """
        🤖 **AMIF Grant Assistant (Demo Modu)**
        
        Merhaba! Ben AMIF hibelerle ilgili sorularınızı yanıtlayabilirim.
        
        **Örnek sorular:**
        - AMIF hibeleri için başvuru kriterleri nelerdir?
        - Entegrasyon projeleri için hangi destekler var?
        - Başvuru süreçleri nasıl işliyor?
        
        **Not:** Şu anda demo modunda çalışıyorum. Gerçek veritabanı bağlantısı için sistem yöneticisine başvurun.
        """
    }
    
    # Anahtar kelime bazlı basit yanıtlar
    query_lower = query.lower()
    
    if any(word in query_lower for word in ['başvuru', 'application', 'apply']):
        return """
        📋 **AMIF Başvuru Süreci**
        
        AMIF hibeleri için başvuru yapmak üzere:
        
        1. **Uygunluk Kontrolü**: Projenizin AMIF kriterlerine uygun olduğundan emin olun
        2. **Belge Hazırlığı**: Gerekli tüm belgeleri hazırlayın
        3. **Online Başvuru**: Resmi portal üzerinden başvurunuzu yapın
        4. **Değerlendirme**: Başvurunuz uzmanlar tarafından değerlendirilir
        
        *Demo modunda detaylı bilgi sınırlıdır.*
        """
    
    elif any(word in query_lower for word in ['entegrasyon', 'integration', 'integrate']):
        return """
        🤝 **AMIF Entegrasyon Destekleri**
        
        AMIF çerçevesinde entegrasyon projeleri için:
        
        - **Sosyal Entegrasyon**: Toplumsal uyum projeleri
        - **Ekonomik Entegrasyon**: İstihdam ve girişimcilik destekleri  
        - **Eğitim Entegrasyonu**: Dil öğrenimi ve mesleki eğitim
        - **Kültürel Entegrasyon**: Kültürlerarası diyalog projeleri
        
        *Detaylı bilgi için gerçek veritabanı bağlantısı gereklidir.*
        """
    
    elif any(word in query_lower for word in ['bütçe', 'budget', 'funding', 'para']):
        return """
        💰 **AMIF Finansman Bilgileri**
        
        AMIF hibeleri kapsamında:
        
        - **Proje Bütçeleri**: Değişken tutarlarda destek
        - **Eş Finansman**: Genellikle %25 eş finansman gerekli
        - **Ödeme Planı**: Avans ve ara ödemeler mevcut
        - **Raporlama**: Düzenli mali raporlama zorunlu
        
        *Güncel tutarlar için resmi kaynaklara başvurun.*
        """
    
    return demo_responses["default"]

@app.route('/')
def index():
    """Ana sayfa"""
    return render_template('index.html', 
                         db_connected=db_connected, 
                         db_info=db_info)

@app.route('/search', methods=['POST'])
def search():
    """Arama endpoint'i"""
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'Arama sorgusu boş olamaz'
            })
        
        # Veritabanında arama yap
        if db_connected:
            results = search_in_database(query)
            
            if results is None:
                # Hata durumunda demo moda geç
                response = get_demo_response(query)
                return jsonify({
                    'success': True,
                    'mode': 'demo',
                    'response': response,
                    'query': query
                })
            elif len(results) == 0:
                return jsonify({
                    'success': True,
                    'mode': 'database',
                    'response': f"'{query}' ile ilgili sonuç bulunamadı. Lütfen farklı anahtar kelimeler deneyin.",
                    'results': [],
                    'query': query
                })
            else:
                # Sonuçları formatla
                formatted_response = f"**'{query}' için {len(results)} sonuç bulundu:**\n\n"
                
                for result in results:
                    formatted_response += f"**{result['rank']}. Sonuç:**\n"
                    formatted_response += f"{result['content']}\n"
                    formatted_response += f"*Kaynak: {result['source']}*\n\n"
                
                return jsonify({
                    'success': True,
                    'mode': 'database',
                    'response': formatted_response,
                    'results': results,
                    'query': query
                })
        else:
            # Demo modu
            response = get_demo_response(query)
            return jsonify({
                'success': True,
                'mode': 'demo',
                'response': response,
                'query': query
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Arama sırasında hata oluştu: {str(e)}'
        })

@app.route('/status')
def status():
    """Sistem durumu"""
    return jsonify({
        'database_connected': db_connected,
        'database_info': db_info,
        'openai_configured': bool(settings.OPENAI_API_KEY)
    })

if __name__ == '__main__':
    print("🚀 AMIF Grant Assistant başlatılıyor...")
    
    # Veritabanı bağlantısını kontrol et
    check_database_connection()
    
    print(f"🌐 Web arayüzü: http://localhost:3000")
    print(f"📊 Veritabanı durumu: {'Bağlı' if db_connected else 'Bağlı değil'}")
    
    if db_connected:
        print(f"📄 Toplam doküman: {db_info.get('document_count', 'Bilinmiyor')}")
    
    app.run(host='0.0.0.0', port=3000, debug=True) 