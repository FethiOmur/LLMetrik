import sys
import os
import chromadb
from chromadb.config import Settings

sys.path.append('.')

try:
    print("🔍 ChromaDB collection'ları kontrol ediliyor...")
    
    # ChromaDB client'ı başlat
    data_dir = "data/db"
    client = chromadb.PersistentClient(
        path=data_dir,
        settings=Settings(
            anonymized_telemetry=False,
            allow_reset=True
        )
    )
    
    # Tüm collection'ları listele
    collections = client.list_collections()
    print(f"📂 Toplam collection sayısı: {len(collections)}")
    
    for i, collection in enumerate(collections, 1):
        count = collection.count()
        print(f"{i}. Collection: '{collection.name}' - {count} doküman")
        
        if count > 0:
            # Örnek bir sorgu yap
            try:
                results = collection.query(
                    query_texts=["hibe"],
                    n_results=1
                )
                if results['documents'] and results['documents'][0]:
                    sample_doc = results['documents'][0][0][:100] + "..."
                    print(f"   Örnek içerik: {sample_doc}")
            except Exception as e:
                print(f"   Sorgu hatası: {e}")
    
    # Varsayılan collection kontrol et
    try:
        default_collection = client.get_collection("amif_documents")
        default_count = default_collection.count()
        print(f"\n🎯 Varsayılan 'amif_documents' collection: {default_count} doküman")
    except Exception as e:
        print(f"\n⚠️  Varsayılan collection bulunamadı: {e}")

except Exception as e:
    print(f"❌ Hata: {e}")
    import traceback
    traceback.print_exc() 