"""
AMIF Grant Assistant - Web Arayüzü
LangGraph Multi-Agent System kullanıyor
"""

import sys
import os
from pathlib import Path
import uuid

# Ana dizini Python path'ine ekle
sys.path.insert(0, str(Path(__file__).parent.parent))

from flask import Flask, render_template, request, jsonify
from config.settings import settings
from ingestion.vector_store import get_vector_store, get_collection_info
from graph.multi_agent_graph import MultiAgentGraph
from utils.performance_monitor import performance_tracker, QueryTracker

app = Flask(__name__, 
           template_folder='templates',
           static_folder='static')

# Global değişkenler
db_connected = False
db_info = {}
multi_agent_graph = None

def initialize_multi_agent_system():
    """Multi-Agent Graph sistemini başlat"""
    global multi_agent_graph, db_connected, db_info
    try:
        print("🚀 AMIF Grant Assistant başlatılıyor...")
        
        # Vector store'u başlat
        print("🔧 Vector store başlatılıyor...")
        vector_store = get_vector_store()
        print("✅ Vector store hazır")
        
        # Collection bilgilerini al
        db_info = get_collection_info()
        db_connected = True
        print(f"✅ Veritabanı bağlantısı başarılı: {db_info['document_count']} doküman")
        
        # Multi-Agent Graph'ı başlat
        print("🤖 Multi-Agent Graph başlatılıyor...")
        multi_agent_graph = MultiAgentGraph(vector_store)
        print("✅ Multi-Agent Graph hazır")
        
        return True
    except Exception as e:
        print(f"❌ Multi-Agent sistem başlatma hatası: {e}")
        db_connected = False
        return False

def get_demo_response(query: str):
    """Demo yanıtı döndür (fallback)"""
    return {
        'qa_response': f"""
        🤖 **AMIF Grant Assistant (Demo Modu)**
        
        Üzgünüm, şu anda multi-agent sistemine bağlanamıyorum.
        Sorgunuz: "{query}"
        
        **Demo modunda çalışıyorum.** Gerçek sistem için lütfen daha sonra tekrar deneyin.
        """,
        'sources': [],
        'cited_response': 'Demo modunda kaynak bilgisi mevcut değil.',
        'detected_language': 'tr'
    }

@app.route('/')
def index():
    """Ana sayfa"""
    return render_template('index.html', 
                         db_connected=db_connected, 
                         db_info=db_info)

@app.route('/search', methods=['POST'])
def search():
    """Multi-Agent Graph kullanarak arama"""
    try:
        data = request.get_json()
        query = data.get('query', data.get('message', '')).strip()
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'Arama sorgusu boş olamaz'
            })
        
        print(f"🔍 Multi-Agent Graph ile sorgu işleniyor: '{query}'")
        
        # Multi-Agent Graph sistemini kullan
        if multi_agent_graph and db_connected:
            # Session ID - çerezden al veya yeni oluştur
            session_id = request.cookies.get('session_id')
            if not session_id:
                session_id = str(uuid.uuid4())
            
            print(f"🎯 Session ID: {session_id}")
            print("🚀 Multi-Agent workflow başlatılıyor...")
            
            # Performance tracking ile Multi-Agent Graph'ı çalıştır
            with QueryTracker(session_id, query) as query_tracker:
                result = multi_agent_graph.run(query, session_id)
                
                # Document metrics kaydet
                performance_tracker.record_document_metrics(
                    session_id,
                    documents_retrieved=len(result.get('retrieved_documents', [])),
                    sources_generated=len(result.get('sources', [])),
                    detected_language=result.get('detected_language', 'unknown')
                )
            
            print(f"✅ Multi-Agent workflow tamamlandı")
            print(f"📄 QA Yanıt uzunluğu: {len(result.get('qa_response', ''))} karakter")
            print(f"📋 Kaynak sayısı: {len(result.get('sources', []))}")
            
            # Kaynakları formatla
            sources = result.get('sources', [])
            retrieved_docs = result.get('retrieved_documents', [])
            source_details = []
            
            # Eğer sources boşsa, retrieved_documents'ten kaynak oluştur
            if not sources and retrieved_docs:
                for i, doc in enumerate(retrieved_docs[:8], 1):
                    metadata = doc.get('metadata', {})
                    
                    # Kaynak adını çıkar
                    source_path = metadata.get('source', '')
                    clean_source = source_path.replace('data/raw/', '').replace('.pdf', '')
                    if not clean_source:
                        clean_source = metadata.get('filename', 'Bilinmeyen')
                    
                    # Sayfa bilgisini çıkar
                    page_number = metadata.get('page_number', metadata.get('page', ''))
                    page_display = f"Sayfa {page_number}" if page_number else 'Sayfa bilinmiyor'
                    
                    source_details.append({
                        'rank': i,
                        'source': clean_source,
                        'page': page_display,
                        'content': doc.get('content', '')[:100] + '...'
                    })
            else:
                # Normal sources işleme - SourceTracker'dan gelen sources
                for i, source in enumerate(sources, 1):
                    if isinstance(source, dict):
                        source_details.append({
                            'rank': i,
                            'source': source.get('clean_source', 'Bilinmeyen'),
                            'page': source.get('page', 'Sayfa bilinmiyor'),
                            'content': source.get('content', '...')
                        })
            
            # Cross-document analysis bilgilerini ekle
            cross_doc_analysis = result.get('cross_document_analysis', {})
            cross_doc_summary = {}
            
            if cross_doc_analysis:
                cross_doc_summary = {
                    'grants_analyzed': cross_doc_analysis.get('total_grants_analyzed', 0),
                    'insights_found': cross_doc_analysis.get('cross_document_insights', 0),
                    'comparison_type': cross_doc_analysis.get('comparison', {}).get('comparison_type', 'none')
                }
            
            response = jsonify({
                'success': True,
                'mode': 'multi_agent',
                'response': result.get('cited_response', result.get('qa_response', '')),
                'sources': source_details,
                'source_details': source_details,
                'session_id': session_id,
                'cross_document_analysis': cross_doc_summary,
                'metadata': {
                    'detected_language': result.get('detected_language', 'tr'),
                    'agent_workflow': 'supervisor -> document_retriever -> cross_document -> qa_agent -> source_tracker'
                }
            })
            
            # Session cookie ayarla
            response.set_cookie('session_id', session_id, max_age=86400)  # 24 saat
            return response
        
        else:
            # Fallback: Demo modu
            print("⚠️ Multi-Agent sistem kullanılamıyor, demo moda geçiliyor...")
            demo_result = get_demo_response(query)
            
            return jsonify({
                'success': True,
                'mode': 'demo',
                'response': demo_result['qa_response'],
                'source_details': [],
                'metadata': {
                    'detected_language': demo_result['detected_language'],
                    'note': 'Demo modunda çalışıyor - Multi-Agent sistem bağlantısı kurulamadı'
                }
            })
        
    except Exception as e:
        print(f"❌ Arama hatası: {e}")
        return jsonify({
            'success': False,
            'error': f'Arama sırasında hata oluştu: {str(e)}',
            'mode': 'error'
        })

@app.route('/status')
def status():
    """Sistem durumu"""
    try:
        agent_status = "Aktif" if multi_agent_graph else "İnaktif"
        memory_status = "Aktif" if (multi_agent_graph and multi_agent_graph.graph.checkpointer) else "İnaktif"
        session_id = request.cookies.get('session_id', 'Yok')
        
        return jsonify({
            'database_connected': db_connected,
            'multi_agent_system': agent_status,
            'memory_system': memory_status,
            'current_session': session_id[:8] + "..." if len(session_id) > 8 else session_id,
            'document_count': db_info.get('document_count', 0),
            'collection_name': db_info.get('collection_name', 'N/A'),
            'system_mode': 'multi_agent' if multi_agent_graph else 'demo'
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'database_connected': False,
            'multi_agent_system': 'Hata',
            'memory_system': 'Hata',
            'system_mode': 'error'
        })

@app.route('/health')
def health():
    """Sağlık kontrol endpoint'i"""
    return jsonify({
        'status': 'healthy',
        'multi_agent_ready': multi_agent_graph is not None,
        'database_ready': db_connected
    })

@app.route('/api/performance/stats')
def performance_stats():
    """Performance metrics endpoint"""
    try:
        stats = performance_tracker.get_system_stats()
        analytics = performance_tracker.get_query_analytics(hours=24)
        
        return jsonify({
            'success': True,
            'system_stats': stats,
            'query_analytics': analytics,
            'timestamp': performance_tracker.stats['system_start_time'].isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Performance stats alınamadı: {str(e)}'
        })

@app.route('/api/performance/dashboard')
def performance_dashboard():
    """Performance dashboard data"""
    try:
        stats = performance_tracker.get_system_stats()
        analytics_1h = performance_tracker.get_query_analytics(hours=1)
        analytics_24h = performance_tracker.get_query_analytics(hours=24)
        
        return jsonify({
            'success': True,
            'dashboard': {
                'current_stats': {
                    'uptime_hours': round(stats['uptime_seconds'] / 3600, 2),
                    'total_queries': stats['total_queries'],
                    'success_rate': round(stats['success_rate'], 2),
                    'avg_response_time': round(stats['avg_response_time'], 2),
                    'current_memory_mb': round(stats['current_memory_mb'], 2),
                    'current_cpu_percent': round(stats['current_cpu_percent'], 2)
                },
                'last_hour': analytics_1h,
                'last_24_hours': analytics_24h,
                'real_time': {
                    'active_queries': stats['active_queries'],
                    'recent_avg_response_time': round(stats.get('recent_avg_response_time', 0), 2),
                    'recent_queries_count': stats.get('recent_queries_count', 0)
                }
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Dashboard data alınamadı: {str(e)}'
        })

@app.route('/api/history')
def get_conversation_history():
    """Conversation history döndür"""
    try:
        session_id = request.cookies.get('session_id')
        if not session_id:
            return jsonify({
                'success': True,
                'history': [],
                'message': 'Yeni oturum - henüz geçmiş yok'
            })
        
        # LangGraph'tan conversation history al
        if multi_agent_graph and multi_agent_graph.graph.checkpointer:
            try:
                config = {"configurable": {"thread_id": session_id}}
                
                # Graph'ın state history'sini al
                checkpoint = multi_agent_graph.graph.checkpointer.get(config)
                
                if checkpoint and hasattr(checkpoint, 'channel_values'):
                    # Geçmiş conversation'ları çıkar
                    history = []
                    state = checkpoint.channel_values
                    
                    # Mevcut query varsa history'e ekle
                    if state.get('query'):
                        history.append({
                            'type': 'user',
                            'message': state.get('query'),
                            'timestamp': checkpoint.ts if hasattr(checkpoint, 'ts') else None
                        })
                    
                    if state.get('qa_response'):
                        history.append({
                            'type': 'assistant', 
                            'message': state.get('qa_response'),
                            'sources': state.get('sources', []),
                            'timestamp': checkpoint.ts if hasattr(checkpoint, 'ts') else None
                        })
                    
                    return jsonify({
                        'success': True,
                        'session_id': session_id,
                        'history': history
                    })
                else:
                    return jsonify({
                        'success': True,
                        'session_id': session_id,
                        'history': [],
                        'message': 'Bu oturum için henüz geçmiş yok'
                    })
                    
            except Exception as e:
                print(f"⚠️ History alma hatası: {e}")
                return jsonify({
                    'success': True,
                    'session_id': session_id,
                    'history': [],
                    'message': 'Geçmiş bilgiler alınamadı'
                })
        
        return jsonify({
            'success': False,
            'error': 'Memory sistemi mevcut değil'
        })
        
    except Exception as e:
        print(f"❌ History endpoint hatası: {e}")
        return jsonify({
            'success': False,
            'error': f'Geçmiş alınırken hata: {str(e)}'
        })

@app.route('/api/clear-history', methods=['POST'])
def clear_conversation_history():
    """Conversation history temizle"""
    try:
        session_id = request.cookies.get('session_id')
        if not session_id:
            return jsonify({
                'success': False,
                'error': 'Session bulunamadı'
            })
        
        # Yeni session ID oluştur
        new_session_id = str(uuid.uuid4())
        
        response = jsonify({
            'success': True,
            'message': 'Conversation history temizlendi',
            'new_session_id': new_session_id
        })
        
        # Yeni session cookie ayarla
        response.set_cookie('session_id', new_session_id, max_age=86400)
        return response
        
    except Exception as e:
        print(f"❌ History temizleme hatası: {e}")
        return jsonify({
            'success': False,
            'error': f'Geçmiş temizlenirken hata: {str(e)}'
        })

@app.route('/graph')
def graph_visualization():
    """Multi-Agent Graph görselleştirmesi"""
    try:
        if multi_agent_graph:
            # Graph image varsa döndür
            graph_image = multi_agent_graph.get_graph_image()
            if graph_image:
                from flask import Response
                return Response(graph_image, mimetype='image/png')
        
        return jsonify({
            'error': 'Graph görselleştirmesi mevcut değil'
        })
    except Exception as e:
        return jsonify({
            'error': f'Graph görselleştirme hatası: {str(e)}'
        })

if __name__ == '__main__':
    # Sistem başlatma
    print("🌐 AMIF Grant Assistant Web Uygulaması")
    print("="*50)
    
    # Multi-Agent sistemi başlat
    if initialize_multi_agent_system():
        print("🌐 Web arayüzü: http://localhost:3000")
        print("📊 Veritabanı durumu: Bağlı")
        print("🤖 Multi-Agent Graph: Aktif")
        print(f"📄 Toplam doküman: {db_info.get('document_count', 0)}")
    else:
        print("⚠️ Multi-Agent sistem başlatılamadı - Demo modunda çalışacak")
    
    print("="*50)
    
    # Flask uygulamasını başlat
    app.run(host='0.0.0.0', port=3000, debug=True) 