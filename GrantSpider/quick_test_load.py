#!/usr/bin/env python3
"""
Hızlı test için sadece birkaç PDF yükleme scripti
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
    print("🚀 Hızlı test PDF yükleme başlatılıyor...")
    
    try:
        # Vector store'u sıfırla
        print("🗑️  Vector store sıfırlanıyor...")
        reset_vector_store()
        
        # PDF loader ve text processor'ı başlat
        print("📚 PDF loader başlatılıyor...")
        loader = PDFLoader()
        processor = TextProcessor()
        
        # Sadece birkaç PDF dosyasını yükle (test için)
        pdf_files = list(Path('data/raw').glob('*.pdf'))[:3]  # İlk 3 PDF
        
        if not pdf_files:
            print("❌ Hiç PDF bulunamadı!")
            return False
        
        print(f"📄 Test için {len(pdf_files)} PDF yükleniyor...")
        for pdf_file in pdf_files:
            print(f"  - {pdf_file.name}")
        
        # PDF'leri yükle
        all_chunks = []
        for pdf_file in pdf_files:
            print(f"📄 İşleniyor: {pdf_file}")
            docs = loader.load_pdf(str(pdf_file))
            if docs:
                chunks = processor.process_documents(docs)
                all_chunks.extend(chunks)
                print(f"✂️  {len(chunks)} parçaya bölündü")
        
        if not all_chunks:
            print("❌ Hiç metin parçası oluşturulamadı!")
            return False
        
        print(f"🎉 Toplam {len(all_chunks)} metin parçası oluşturuldu")
        
        # Vector store'a ekle
        print("💾 Vector store'a ekleniyor...")
        success = add_documents_to_vector_store(all_chunks)
        
        if success:
            print(f"✅ Test başarıyla tamamlandı! {len(all_chunks)} doküman chunk'ı yüklendi.")
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
        print("\n🎉 Test PDF yükleme tamamlandı! Web uygulamasını test edebilirsiniz.")
    else:
        print("\n💥 Test PDF yükleme başarısız!")
    
    sys.exit(0 if success else 1) 