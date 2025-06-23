#!/usr/bin/env python3
"""
AMIF Grant Assistant - Ana Giriş Noktası
"""

import sys
import os
import argparse
from typing import Optional

# Proje kök dizinini Python path'ine ekle
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def check_environment():
    """Çevre değişkenlerini kontrol eder"""
    try:
        from config.settings import settings
        return True
    except Exception as e:
        print(f"❌ Çevre değişkenleri hatası: {e}")
        print("💡 Lütfen .env dosyasını oluşturun ve gerekli API anahtarlarını ekleyin")
        return False

def run_web_app():
    """Flask web arayüzünü başlatır"""
    print("🌐 Web arayüzü başlatılıyor...")
    from interfaces.web_app import app
    app.run(host='0.0.0.0', port=3000, debug=True)

def run_streamlit():
    """Streamlit web arayüzünü başlatır"""
    print("🌐 Streamlit web arayüzü başlatılıyor...")
    os.system("streamlit run streamlit_app.py")

def run_ingestion(pdf_dir: str = "data/raw"):
    """PDF ingestion sürecini başlatır"""
    print(f"📂 PDF'ler yükleniyor: {pdf_dir}")
    try:
        from ingestion import run_full_ingestion
        success = run_full_ingestion(data_dir=pdf_dir)
        if success:
            print("✅ PDF yükleme başarılı!")
        else:
            print("❌ PDF yükleme başarısız!")
    except Exception as e:
        print(f"❌ Ingestion hatası: {e}")

def show_status():
    """Sistem durumunu gösterir"""
    try:
        from ingestion.vector_store import get_collection_info
        
        print("\n📊 SİSTEM DURUMU")
        print("=" * 50)
        
        info = get_collection_info()
        
        print(f"🗃️  Veritabanı: {info.get('collection_name', 'N/A')}")
        print(f"📄 Belge sayısı: {info.get('document_count', 0):,}")
        print(f"📁 Dizin: {info.get('persist_directory', 'N/A')}")
        
        # PDF dosyalarını kontrol et
        pdf_count = len([f for f in os.listdir("data/raw") if f.endswith('.pdf')])
        print(f"📑 Raw PDF sayısı: {pdf_count}")
        
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ Durum bilgisi alınamadı: {e}")

def main():
    """Ana fonksiyon"""
    parser = argparse.ArgumentParser(
        description="AMIF Grant Assistant - AI Powered Grant Document Q&A System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Örnek Kullanımlar:
  python main.py                    # Flask web arayüzü (varsayılan)
  python main.py --streamlit        # Streamlit web arayüzü
  python main.py --ingest           # PDF'leri veritabanına yükle
  python main.py --status           # Sistem durumunu göster
        """
    )
    
    parser.add_argument(
        '--interface', '-i',
        choices=['web', 'streamlit'],
        default='web',
        help='Kullanılacak arayüz (varsayılan: web)'
    )
    
    parser.add_argument(
        '--web',
        action='store_true',
        help='Flask web arayüzünü başlat (varsayılan)'
    )
    
    parser.add_argument(
        '--streamlit', 
        action='store_true',
        help='Streamlit web arayüzünü başlat'
    )
    
    parser.add_argument(
        '--ingest',
        action='store_true',
        help='PDF dosyalarını veritabanına yükle'
    )
    
    parser.add_argument(
        '--pdf-dir',
        default='data/raw',
        help='PDF dosyalarının bulunduğu dizin (varsayılan: data/raw)'
    )
    
    parser.add_argument(
        '--status',
        action='store_true',
        help='Sistem durumunu göster'
    )
    
    args = parser.parse_args()
    
    # Environment kontrolü
    if not check_environment():
        return 1
    
    # Argümanlara göre uygun fonksiyonu çalıştır
    try:
        if args.ingest:
            run_ingestion(args.pdf_dir)
        elif args.status:
            show_status()
        elif args.streamlit or args.interface == 'streamlit':
            run_streamlit()
        else:
            # Varsayılan: Flask web arayüzü
            run_web_app()
            
    except KeyboardInterrupt:
        print("\n👋 Program sonlandırıldı!")
        return 0
    except Exception as e:
        print(f"❌ Program hatası: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 