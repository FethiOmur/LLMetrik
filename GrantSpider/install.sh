#!/bin/bash
# AMIF Grant Assistant - Installation Script

set -e

echo "🚀 AMIF Grant Assistant Kurulum Scripti"
echo "======================================"

# Renk kodları
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonksiyonlar
print_step() {
    echo -e "${BLUE}[$(date +'%H:%M:%S')] $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Python versiyonu kontrolü
check_python() {
    print_step "Python versiyonu kontrol ediliyor..."
    
    if ! command -v python3 &> /dev/null; then
        print_error "Python3 bulunamadı! Lütfen Python 3.8+ yükleyin."
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    REQUIRED_VERSION="3.8"
    
    if python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
        print_success "Python $PYTHON_VERSION kullanılıyor"
    else
        print_error "Python $REQUIRED_VERSION+ gerekli, mevcut versiyon: $PYTHON_VERSION"
        exit 1
    fi
}

# Virtual environment oluşturma
create_venv() {
    print_step "Virtual environment oluşturuluyor..."
    
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        print_success "Virtual environment oluşturuldu"
    else
        print_warning "Virtual environment zaten mevcut"
    fi
    
    # Virtual environment'ı aktifleştir
    source venv/bin/activate
    print_success "Virtual environment aktifleştirildi"
}

# Dependencies yükleme
install_dependencies() {
    print_step "Dependencies yükleniyor..."
    
    if [ -f "requirements.txt" ]; then
        pip install --upgrade pip
        pip install -r requirements.txt
        print_success "Dependencies başarıyla yüklendi"
    else
        print_error "requirements.txt bulunamadı!"
        exit 1
    fi
}

# .env dosyası oluşturma
setup_env() {
    print_step ".env dosyası kontrol ediliyor..."
    
    if [ ! -f ".env" ]; then
        print_step ".env dosyası oluşturuluyor..."
        python3 start.py --create-env-only 2>/dev/null || {
            cat > .env << EOF
# AMIF Grant Assistant - Environment Variables

# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Model Configuration  
OPENAI_MODEL=gpt-4
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
EOF
        }
        print_success ".env dosyası oluşturuldu"
        print_warning "Lütfen .env dosyasındaki API anahtarlarını güncelleyin!"
    else
        print_success ".env dosyası zaten mevcut"
    fi
}

# Dizin yapısını kontrol etme
check_directories() {
    print_step "Dizin yapısı kontrol ediliyor..."
    
    # Gerekli dizinleri oluştur
    mkdir -p data/raw data/db data/processed
    
    print_success "Dizin yapısı hazır"
}

# Veritabanı kontrolü
check_database() {
    print_step "Veritabanı kontrol ediliyor..."
    
    if [ -d "data/db" ] && [ "$(ls -A data/db)" ]; then
        print_success "Vektör veritabanı mevcut"
    else
        print_warning "Vektör veritabanı boş"
        print_step "PDF dosyalarını data/raw/ klasörüne ekleyin ve aşağıdaki komutu çalıştırın:"
        echo "python main.py --ingest"
    fi
}

# Test çalıştırma
run_tests() {
    print_step "Kurulum testi yapılıyor..."
    
    # Basit import testi
    python3 -c "
try:
    from config.settings import settings
    from ingestion.vector_store import VectorStore
    from agents.qa_agent import QAAgent
    print('✅ Tüm modüller başarıyla import edildi')
except Exception as e:
    print(f'❌ Import hatası: {e}')
    exit(1)
" || {
        print_error "Kurulum testi başarısız!"
        exit 1
    }
    
    print_success "Kurulum testi başarılı"
}

# Ana kurulum fonksiyonu
main() {
    echo
    print_step "Kurulum başlatılıyor..."
    echo
    
    check_python
    create_venv
    install_dependencies
    setup_env
    check_directories
    check_database
    run_tests
    
    echo
    echo "🎉 Kurulum tamamlandı!"
    echo
    echo "📝 Sonraki adımlar:"
    echo "1. .env dosyasında API anahtarlarınızı güncelleyin"
    echo "2. PDF dosyalarını data/raw/ klasörüne ekleyin"
    echo "3. Sistemi başlatın:"
    echo
    echo "   # Virtual environment'ı aktifleştirin"
    echo "   source venv/bin/activate"
    echo
    echo "   # PDF'leri yükleyin (ilk kullanım)"
    echo "   python main.py --ingest"
    echo
    echo "   # Sistemı başlatın"
    echo "   python start.py              # Menü ile başlat"
    echo "   python main.py --streamlit   # Web arayüzü"
    echo "   python main.py --cli         # Terminal arayüzü"
    echo
    echo "📚 Daha fazla bilgi için README.md dosyasını okuyun."
}

# Cleanup fonksiyonu
cleanup() {
    if [ $? -ne 0 ]; then
        print_error "Kurulum başarısız oldu!"
        echo "Sorun yaşıyorsanız, aşağıdaki komutu manuel olarak çalıştırın:"
        echo "pip install -r requirements.txt"
    fi
}

# Cleanup trap'i ayarla
trap cleanup EXIT

# Ana fonksiyonu çalıştır
main "$@" 