#!/usr/bin/env python3
"""
🔧 AMIF Grant Assistant - Hızlı Sorun Çözücü
Projedeki yaygın sorunları otomatik olarak tespit eder ve çözer.
"""

import os
import sys
import subprocess
from pathlib import Path

def print_banner():
    """Banner yazdırır"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                    🔧 HIZLI SORUN ÇÖZÜCÜ                    ║
║              AMIF Grant Assistant Fix Tool                  ║
║                  Otomatik Sorun Tespiti                     ║
╚══════════════════════════════════════════════════════════════╝
    """)

def check_and_install_dependencies():
    """Eksik bağımlılıkları kontrol eder ve yükler"""
    print("📦 Bağımlılıklar kontrol ediliyor...")
    
    required_packages = [
        "streamlit==1.45.1",
        "langchain==0.3.25", 
        "chromadb==1.0.12",
        "openai==1.86.0",
        "langchain-openai==0.3.23",
        "langchain-chroma==0.2.4",
        "python-dotenv==1.0.0"
    ]
    
    for package in required_packages:
        package_name = package.split("==")[0]
        try:
            result = subprocess.run([sys.executable, "-c", f"import {package_name}"], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print(f"✅ {package_name} yüklü")
            else:
                print(f"🔄 {package_name} yükleniyor...")
                subprocess.run([sys.executable, "-m", "pip", "install", package], check=True)
                print(f"✅ {package_name} yüklendi")
        except Exception as e:
            print(f"❌ {package_name} yüklenemedi: {e}")

def fix_env_file():
    """Environment dosyasını düzeltir"""
    print("🔐 .env dosyası kontrol ediliyor...")
    
    env_path = Path(".env")
    if not env_path.exists():
        print("📝 .env dosyası oluşturuluyor...")
        env_content = """# AMIF Grant Assistant Environment Variables
# OpenAI API Key - https://platform.openai.com/api-keys adresinden alabilirsiniz
OPENAI_API_KEY=your_openai_api_key_here

# ChromaDB Settings
CHROMA_DB_PATH=./data/db

# Logging
LOG_LEVEL=INFO
"""
        with open(".env", "w", encoding="utf-8") as f:
            f.write(env_content)
        print("✅ .env dosyası oluşturuldu")
    else:
        print("✅ .env dosyası mevcut")

def check_project_structure():
    """Proje yapısını kontrol eder ve eksik dizinleri oluşturur"""
    print("📁 Proje yapısı kontrol ediliyor...")
    
    required_dirs = [
        "agents", "config", "graph", "ingestion", "interfaces", 
        "memory", "chains", "utils", "data", "data/db", "data/raw"
    ]
    
    for dir_name in required_dirs:
        dir_path = Path(dir_name)
        if not dir_path.exists():
            print(f"📁 {dir_name} dizini oluşturuluyor...")
            dir_path.mkdir(parents=True, exist_ok=True)
            
            # __init__.py dosyalarını ekle
            if dir_name not in ["data", "data/db", "data/raw"]:
                init_file = dir_path / "__init__.py"
                if not init_file.exists():
                    init_file.write_text("# Empty init file\n")
        else:
            print(f"✅ {dir_name}")

def check_critical_files():
    """Kritik dosyaları kontrol eder"""
    print("🔧 Kritik dosyalar kontrol ediliyor...")
    
    critical_files = {
        "main.py": "Ana başlatma dosyası",
        "start.py": "Hızlı başlatma scripti", 
        "streamlit_app.py": "Streamlit uygulaması",
        "requirements.txt": "Python bağımlılıkları"
    }
    
    for file_name, description in critical_files.items():
        if not Path(file_name).exists():
            print(f"❌ {file_name} eksik ({description})")
        else:
            size = Path(file_name).stat().st_size
            if size == 0:
                print(f"⚠️  {file_name} boş ({description})")
            else:
                print(f"✅ {file_name} ({size} bytes)")

def test_basic_functionality():
    """Temel fonksiyonaliteyi test eder"""
    print("🧪 Temel fonksiyonalite test ediliyor...")
    
    try:
        # Import testleri
        test_imports = [
            "import sys",
            "import chromadb",
            "import langchain",
            "import openai",
            "from config.settings import SETTINGS",
            "from agents.retriever_agent import DocumentRetrieverAgent"
        ]
        
        for test_import in test_imports:
            try:
                result = subprocess.run([sys.executable, "-c", test_import], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    print(f"✅ {test_import}")
                else:
                    print(f"❌ {test_import}: {result.stderr.strip()}")
            except Exception as e:
                print(f"❌ {test_import}: {e}")
                
    except Exception as e:
        print(f"❌ Test başarısız: {e}")

def create_requirements_if_missing():
    """requirements.txt eksikse oluşturur"""
    requirements_path = Path("requirements.txt")
    if not requirements_path.exists():
        print("📝 requirements.txt oluşturuluyor...")
        requirements_content = """streamlit==1.45.1
langchain==0.3.25
langchain-openai==0.3.23
langchain-chroma==0.2.4
langchain-community==0.3.25
langchain-core==0.3.65
langchain-text-splitters==0.3.8
chromadb==1.0.12
openai==1.86.0
python-dotenv==1.0.0
PyMuPDF==1.24.0
pymupdf4llm==0.0.9
pathlib
uuid
"""
        requirements_path.write_text(requirements_content)
        print("✅ requirements.txt oluşturuldu")

def main():
    """Ana fonksiyon"""
    print_banner()
    
    print("🔍 Sistem analizi başlıyor...")
    print("=" * 50)
    
    # Adım adım sorun çözme
    steps = [
        ("📁 Proje yapısını kontrol et", check_project_structure),
        ("📝 requirements.txt kontrol et", create_requirements_if_missing),
        ("🔐 .env dosyasını kontrol et", fix_env_file),
        ("📦 Bağımlılıkları kontrol et", check_and_install_dependencies),
        ("🔧 Kritik dosyaları kontrol et", check_critical_files),
        ("🧪 Temel fonksiyonaliteyi test et", test_basic_functionality)
    ]
    
    for step_name, step_func in steps:
        print(f"\n{step_name}")
        print("-" * 30)
        try:
            step_func()
        except Exception as e:
            print(f"❌ {step_name} başarısız: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Hızlı düzeltme tamamlandı!")
    print("💡 Artık 'python3 start.py' ile sistemi başlatabilirsiniz.")
    
    # Son kontrol
    print("\n📊 FİNAL DURUMU:")
    if Path("data/db").exists() and any(Path("data/db").iterdir()):
        print("✅ Veritabanı hazır")
    else:
        print("⚠️  Veritabanı boş - PDF'leri yüklemek için 'python3 main.py --ingest' çalıştırın")
    
    pdf_count = len(list(Path("data/raw").glob("*.pdf"))) if Path("data/raw").exists() else 0
    print(f"📄 {pdf_count} PDF dosyası bulundu")

if __name__ == "__main__":
    main() 