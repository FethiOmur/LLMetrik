"""
Veri işleme (ingestion) modülü

Bu modül PDF dosyalarını yükleme, metin işleme ve vektör veritabanına kaydetme
işlemlerini gerçekleştirir.

Kullanım örneği:
    from ingestion import PDFLoader, TextProcessor, VectorStore
    
    # PDF'leri yükle
    loader = PDFLoader()
    documents = loader.load_all_pdfs("data/raw")
    
    # Metinleri işle ve parçala
    processor = TextProcessor()
    chunks = processor.process_documents(documents)
    
    # Vektör veritabanına kaydet
    vector_store = VectorStore()
    vector_store.add_documents(chunks)
"""

from .pdf_loader import PDFLoader
from .text_processor import TextProcessor
from .vector_store import VectorStore

__all__ = ["PDFLoader", "TextProcessor", "VectorStore"]

def create_ingestion_pipeline(data_dir: str = "data/raw", db_dir: str = "data/db"):
    """
    Tam bir veri işleme pipeline'ı oluşturur
    
    Args:
        data_dir: PDF dosyalarının bulunduğu dizin
        db_dir: Vektör veritabanının kaydedileceği dizin
        
    Returns:
        (loader, processor, vector_store) tuple'ı
    """
    loader = PDFLoader(data_dir=data_dir)
    processor = TextProcessor()
    vector_store = VectorStore(persist_directory=db_dir)
    
    return loader, processor, vector_store

def run_full_ingestion(data_dir: str = "data/raw", db_dir: str = "data/db", reset_db: bool = False):
    """
    Tam veri işleme sürecini çalıştırır
    
    Args:
        data_dir: PDF dosyalarının bulunduğu dizin
        db_dir: Vektör veritabanının kaydedileceği dizin
        reset_db: Veritabanını sıfırla
        
    Returns:
        Başarılı ise True
    """
    try:
        print("🚀 Veri işleme pipeline'ı başlatılıyor...")
        
        # Pipeline bileşenlerini oluştur
        loader, processor, vector_store = create_ingestion_pipeline(data_dir, db_dir)
        
        # Veritabanını sıfırla (istenirse)
        if reset_db:
            vector_store.reset_database()
        
        # PDF'leri yükle
        print("\n📂 1. PDF dosyaları yükleniyor...")
        documents = loader.load_all_pdfs()
        
        if not documents:
            print("❌ Yüklenecek PDF dosyası bulunamadı")
            return False
        
        # Belge bilgilerini göster
        doc_info = loader.get_document_info(documents)
        print(f"📊 Yüklenen belgeler: {doc_info}")
        
        # Metinleri işle
        print("\n✂️  2. Metinler işleniyor ve parçalanıyor...")
        chunks = processor.process_documents(documents)
        
        if not chunks:
            print("❌ İşlenecek metin parçası bulunamadı")
            return False
        
        # Chunk istatistiklerini göster
        chunk_stats = processor.get_chunk_statistics(chunks)
        print(f"📊 Chunk istatistikleri: {chunk_stats}")
        
        # Vektör veritabanına kaydet
        print("\n🗃️  3. Vektör veritabanına kaydediliyor...")
        success = vector_store.add_documents(chunks)
        
        if not success:
            print("❌ Vektör veritabanına kaydetme başarısız")
            return False
        
        # Veritabanı bilgilerini göster
        db_info = vector_store.get_database_info()
        print(f"📊 Veritabanı bilgileri: {db_info}")
        
        print("\n🎉 Veri işleme pipeline'ı başarıyla tamamlandı!")
        return True
        
    except Exception as e:
        print(f"❌ Veri işleme hatası: {e}")
        return False 