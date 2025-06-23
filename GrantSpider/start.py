#!/usr/bin/env python3
"""
AMIF Grant Assistant - Hızlı Başlatma Scripti
"""

import os
import sys
import subprocess
from pathlib import Path

# Proje kök dizinini Python path'ine ekle
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def print_banner():
    """Başlık banner'ını yazdırır"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                    🚀 AMIF Grant Assistant                   ║
║              AI-Powered Grant Document Q&A System           ║
║                     Hızlı Başlatma Scripti                  ║
╚══════════════════════════════════════════════════════════════╝
    """)

def get_correct_python_executable():
    """Doğru Python executable'ını tespit eder"""
    # Önce which python3 komutunu dene
    try:
        result = subprocess.run(["which", "python3"], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
    except:
        pass
    
    # Alternatif yolları dene
    possible_paths = [
        "/usr/bin/python3",
        "/opt/homebrew/bin/python3.11", 
        "/opt/homebrew/bin/python3",
        sys.executable
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    return sys.executable  # Son çare

def check_prerequisites():
    """Ön koşulları kontrol eder"""
    print("🔍 Ön koşullar kontrol ediliyor...")
    
    issues = []
    
    # .env dosyası kontrolü
    env_file = Path(".env")
    if not env_file.exists():
        issues.append("❌ .env dosyası bulunamadı")
        print("💡 .env dosyası oluşturuluyor...")
        create_env_template()
    else:
        print("✅ .env dosyası mevcut")
    
    # Doğru Python executable'ını tespit et
    python_exec = get_correct_python_executable()
    
    # Dependencies kontrolü - doğru Python kullan
    try:
        # Streamlit kontrolü
        result = subprocess.run([python_exec, "-c", "import streamlit"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Streamlit yüklü")
        else:
            issues.append("❌ Streamlit yüklü değil")
    except Exception:
        issues.append("❌ Streamlit kontrolü başarısız")
    
    try:
        # LangChain kontrolü
        result = subprocess.run([python_exec, "-c", "import langchain"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ LangChain yüklü")
        else:
            issues.append("❌ LangChain yüklü değil")
    except Exception:
        issues.append("❌ LangChain kontrolü başarısız")
    
    try:
        # ChromaDB kontrolü
        result = subprocess.run([python_exec, "-c", "import chromadb"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ ChromaDB yüklü")
        else:
            issues.append("❌ ChromaDB yüklü değil")
    except Exception:
        issues.append("❌ ChromaDB kontrolü başarısız")
    
    try:
        # OpenAI kontrolü
        result = subprocess.run([python_exec, "-c", "import openai"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ OpenAI yüklü")
        else:
            issues.append("❌ OpenAI yüklü değil")
    except Exception:
        issues.append("❌ OpenAI kontrolü başarısız")
    
    # Veritabanı kontrolü
    db_path = Path("data/db")
    if db_path.exists() and any(db_path.iterdir()):
        print("✅ Vektör veritabanı mevcut")
    else:
        issues.append("⚠️  Vektör veritabanı boş veya mevcut değil")
    
    # PDF dosyaları kontrolü
    pdf_path = Path("data/raw")
    if pdf_path.exists():
        pdf_count = len(list(pdf_path.glob("*.pdf")))
        if pdf_count > 0:
            print(f"✅ {pdf_count} PDF dosyası bulundu")
        else:
            issues.append("⚠️  PDF dosyası bulunamadı")
    else:
        issues.append("❌ data/raw dizini bulunamadı")
    
    return issues

def create_env_template():
    """Örnek .env dosyası oluşturur"""
    env_template = """# AMIF Grant Assistant - Environment Variables

# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Model Configuration  
OPENAI_MODEL=o4-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small

# Vector Database Configuration
CHROMA_PERSIST_DIRECTORY=data/db
CHROMA_COLLECTION_NAME=amif_documents

# Application Configuration
MAX_CHAT_HISTORY=50
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
MAX_SEARCH_RESULTS=8

# Logging
LOG_LEVEL=INFO
"""
    
    with open(".env", "w", encoding="utf-8") as f:
        f.write(env_template)
    
    print("📝 .env dosyası oluşturuldu. Lütfen API anahtarlarınızı ekleyin!")

def show_quick_start_menu():
    """Hızlı başlatma menüsünü gösterir"""
    print("\n🚀 HIZLI BAŞLATMA MENÜSÜ")
    print("=" * 50)
    print("1. 🌐 Streamlit Web Arayüzü (Önerilen)")
    print("2. 💻 Gelişmiş CLI Arayüzü")
    print("3. 🔧 Basit CLI Arayüzü")
    print("4. 📂 PDF Yükleme (Ingestion)")
    print("5. 📊 Sistem Durumu")
    print("6. ❓ Yardım")
    print("7. 🚪 Çıkış")
    print("=" * 50)

def handle_user_choice(choice: str):
    """Kullanıcı seçimini işler"""
    if choice == '1':
        print("🌐 Streamlit başlatılıyor...")
        os.system("python main.py --streamlit")
    
    elif choice == '2':
        print("💻 Gelişmiş CLI başlatılıyor...")
        os.system("python main.py --cli")
    
    elif choice == '3':
        print("🔧 Basit CLI başlatılıyor...")
        os.system("python main.py --simple")
    
    elif choice == '4':
        print("📂 PDF yükleme başlatılıyor...")
        os.system("python main.py --ingest")
    
    elif choice == '5':
        print("📊 Sistem durumu kontrol ediliyor...")
        os.system("python main.py --status")
    
    elif choice == '6':
        show_help()
    
    elif choice == '7':
        print("👋 Görüşürüz!")
        sys.exit(0)
    
    else:
        print("❌ Geçersiz seçim! Lütfen 1-7 arası bir sayı girin.")

def show_help():
    """Yardım bilgilerini gösterir"""
    print("\n📚 YARDIM BİLGİLERİ")
    print("=" * 60)
    print("🌐 Streamlit Web Arayüzü:")
    print("   • En kullanıcı dostu arayüz")
    print("   • Web tarayıcısında çalışır")
    print("   • Sürükle-bırak dosya yükleme")
    print("   • Görsel sonuç gösterimi")
    print()
    print("💻 Gelişmiş CLI Arayüzü:")
    print("   • Terminal tabanlı")
    print("   • Detaylı kaynak bilgileri")
    print("   • Gelişmiş komutlar")
    print("   • LangGraph tabanlı")
    print()
    print("🔧 Basit CLI Arayüzü:")
    print("   • Hızlı test için")
    print("   • Minimal arayüz")
    print("   • Temel soru-cevap")
    print()
    print("📂 PDF Yükleme:")
    print("   • Yeni PDF dosyalarını sisteme ekler")
    print("   • data/raw klasöründeki PDF'leri işler")
    print("   • Vektör veritabanını günceller")
    print("=" * 60)

def run_diagnostic():
    """Detaylı sistem diagnostiği çalıştırır"""
    print("\n🔍 DETAYLI SİSTEM DİAGNOSTİĞİ")
    print("=" * 60)
    
    # Doğru Python executable'ını tespit et
    python_exec = get_correct_python_executable()
    
    # Python bilgileri
    print(f"🐍 Python: {sys.version}")
    print(f"📁 Python executable: {python_exec}")
    print(f"📂 Çalışma dizini: {os.getcwd()}")
    
    print("\n📦 YÜKLÜ PAKETLER:")
    print("-" * 30)
    
    # Kritik paketleri kontrol et
    critical_packages = [
        "streamlit", "langchain", "chromadb", "openai", 
        "langchain-openai", "langchain-chroma", "python-dotenv"
    ]
    
    for package in critical_packages:
        try:
            result = subprocess.run([python_exec, "-c", f"import {package}; print(f'{package}: YÜKLÜ')"], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print(f"✅ {package}")
            else:
                print(f"❌ {package}: {result.stderr.strip()}")
        except Exception as e:
            print(f"❌ {package}: {str(e)}")
    
    print("\n📁 PROJE YAPISINI KONTROL ET:")
    print("-" * 30)
    
    # Kritik dizinleri kontrol et
    critical_dirs = [
        "agents", "config", "graph", "ingestion", "interfaces", 
        "memory", "chains", "utils", "data", "data/db", "data/raw"
    ]
    
    for dir_name in critical_dirs:
        if os.path.exists(dir_name):
            if dir_name == "data/db":
                files = os.listdir(dir_name) if os.path.isdir(dir_name) else []
                print(f"✅ {dir_name}/ ({len(files)} dosya)")
            elif dir_name == "data/raw":
                pdf_files = [f for f in os.listdir(dir_name) if f.endswith('.pdf')] if os.path.isdir(dir_name) else []
                print(f"✅ {dir_name}/ ({len(pdf_files)} PDF)")
            else:
                print(f"✅ {dir_name}/")
        else:
            print(f"❌ {dir_name}/ eksik")
    
    print("\n🔧 KRITIK DOSYALAR:")
    print("-" * 30)
    
    critical_files = [
        ".env", "requirements.txt", "main.py", "start.py", 
        "streamlit_app.py", "config/settings.py", "config/models.py"
    ]
    
    for file_name in critical_files:
        if os.path.exists(file_name):
            size = os.path.getsize(file_name)
            print(f"✅ {file_name} ({size} bytes)")
        else:
            print(f"❌ {file_name} eksik")
    
    # Environment variables kontrolü
    print("\n🔐 ENVIRONMENT VARIABLES:")
    print("-" * 30)
    
    if os.path.exists(".env"):
        try:
            with open(".env", "r") as f:
                env_content = f.read()
                if "OPENAI_API_KEY=your_openai_api_key_here" in env_content:
                    print("⚠️  OpenAI API key henüz ayarlanmamış")
                elif "OPENAI_API_KEY=" in env_content:
                    print("✅ OpenAI API key ayarlanmış görünüyor")
                else:
                    print("❌ .env dosyasında API key bulunamadı")
        except Exception as e:
            print(f"❌ .env dosyası okunamadı: {e}")
    
    print("\n💾 VERİTABANI DURUMU:")
    print("-" * 30)
    
    db_path = Path("data/db")
    if db_path.exists():
        try:
            # ChromaDB dosyalarını kontrol et
            chroma_file = db_path / "chroma.sqlite3"
            if chroma_file.exists():
                size_mb = chroma_file.stat().st_size / (1024*1024)
                print(f"✅ ChromaDB: {size_mb:.1f}MB")
            else:
                print("❌ ChromaDB dosyası bulunamadı")
            
            # Collection dizinlerini say
            collections = [d for d in db_path.iterdir() if d.is_dir()]
            print(f"📁 Collection sayısı: {len(collections)}")
            
        except Exception as e:
            print(f"❌ Veritabanı kontrolü başarısız: {e}")
    else:
        print("❌ Veritabanı dizini bulunamadı")
    
    print("=" * 60)

def launch_streamlit():
    """Streamlit uygulamasını başlatır"""
    print("\n🌐 Streamlit uygulaması başlatılıyor...")
    try:
        os.system(f"{sys.executable} -m streamlit run streamlit_app.py")
    except Exception as e:
        print(f"❌ Streamlit başlatılamadı: {e}")

def launch_flask_app():
    """Flask web uygulamasını başlatır"""
    print("\n🌐 Flask web uygulaması başlatılıyor...")
    print("📍 Adres: http://localhost:3000")
    print("🎨 Modern web arayüzü yükleniyor...")
    try:
        # interfaces dizinine geç ve web_app.py'yi çalıştır
        os.chdir("interfaces")
        import subprocess
        subprocess.run([sys.executable, "web_app.py"])
    except Exception as e:
        print(f"❌ Flask uygulaması başlatılamadı: {e}")
        print("💡 Alternatif çözüm denenecek...")
        try:
            os.system(f"{sys.executable} web_app.py")
        except Exception as e2:
            print(f"❌ Alternatif çözüm de başarısız: {e2}")
        finally:
            # Ana dizine geri dön
            os.chdir("..")

def show_system_status():
    """Sistem durumunu gösterir"""
    print("\n📊 SİSTEM DURUMU")
    print("=" * 30)
    
    # Doğru Python executable'ını tespit et
    python_exec = get_correct_python_executable()
    
    # Hızlı kontroller
    print("🔧 Temel Kontroller:")
    
    # Python version
    print(f"🐍 Python: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    
    # Dependencies
    deps_ok = True
    for dep in ["streamlit", "langchain", "chromadb", "openai"]:
        try:
            result = subprocess.run([python_exec, "-c", f"import {dep}"], 
                                  capture_output=True, text=True, timeout=3)
            if result.returncode == 0:
                print(f"✅ {dep}")
            else:
                print(f"❌ {dep}")
                deps_ok = False
        except:
            print(f"❌ {dep}")
            deps_ok = False
    
    # Database
    if Path("data/db").exists() and any(Path("data/db").iterdir()):
        print("✅ Veritabanı")
    else:
        print("❌ Veritabanı")
    
    # PDFs
    pdf_count = len(list(Path("data/raw").glob("*.pdf"))) if Path("data/raw").exists() else 0
    print(f"📄 PDF Dosyaları: {pdf_count}")
    
    # Overall status
    if deps_ok and Path("data/db").exists() and pdf_count > 0:
        print("\n🎉 Sistem hazır! Tüm bileşenler çalışıyor.")
    else:
        print("\n⚠️  Bazı sorunlar var. Detaylı analiz için '4' seçeneğini kullanın.")

def main():
    """Ana fonksiyon - Direkt Flask web uygulamasını başlatır"""
    print_banner()
    
    # Ön koşulları kontrol et
    issues = check_prerequisites()
    
    if issues:
        print("\n⚠️  Tespit edilen durumlar:")
        for issue in issues:
            print(f"  {issue}")
        
        # Kritik hatalar varsa durdur
        if any("❌" in issue for issue in issues):
            print("\n❌ Kritik hatalar mevcut. Lütfen problemleri çözün ve tekrar deneyin.")
            print("💡 Yardım almak için: python install.sh")
            return
    
    print(f"\n✅ Sistem hazır! Web uygulaması başlatılıyor...")
    
    # Direkt Flask web uygulamasını başlat
    launch_flask_app()

if __name__ == "__main__":
    main() 