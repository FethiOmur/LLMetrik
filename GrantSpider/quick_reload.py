#!/usr/bin/env python3
"""
Hızlı PDF yeniden yükleme scripti
"""

import sys
import os
from pathlib import Path

# Proje kök dizinini Python path'ine ekle
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from ingestion.pdf_loader import PDFLoader
from ingestion.text_processor import TextProcessor
from ingestion.vector_store import reset_vector_store, add_documents_to_vector_store

def main():
    print("🚀 Hızlı PDF yeniden yükleme başlatılıyor...")
    
    try:
        # Vector store'u sıfırla
        print("🗑️  Vector store sıfırlanıyor...")
        reset_vector_store()
        
        # PDF loader ve text processor'ı başlat
        print("📚 PDF loader başlatılıyor...")
        loader = PDFLoader()
        processor = TextProcessor()
        
        # PDF'leri yükle
        print("📄 PDF'ler yükleniyor...")
        docs = loader.load_all_pdfs('data/raw')
        
        if not docs:
            print("❌ Hiç PDF bulunamadı!")
            return False
        
        # Metinleri işle
        print("✂️  Metinler parçalanıyor...")
        chunks = processor.process_documents(docs)
        
        if not chunks:
            print("❌ Hiç metin parçası oluşturulamadı!")
            return False
        
        # Vector store'a ekle
        print("💾 Vector store'a ekleniyor...")
        success = add_documents_to_vector_store(chunks)
        
        if success:
            print(f"✅ Başarıyla tamamlandı! {len(chunks)} doküman chunk'ı yüklendi.")
            return True
        else:
            print("❌ Vector store'a ekleme başarısız!")
            return False
            
    except Exception as e:
        print(f"❌ Hata: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 PDF yükleme tamamlandı! Web uygulamasını yeniden başlatabilirsiniz.")
    else:
        print("\n💥 PDF yükleme başarısız!")
    
    sys.exit(0 if success else 1) 