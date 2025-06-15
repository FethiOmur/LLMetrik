#!/usr/bin/env python3
"""
Gelişmiş CLI Arayüzü - AMIF Grant Assistant
"""

import os
import sys
from datetime import datetime
from typing import List, Dict, Any

# Proje kök dizinini Python path'ine ekle
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from ingestion.vector_store import VectorStore
from agents.qa_agent import QAAgent
from config.models import get_llm_model

class AdvancedCLI:
    """Gelişmiş komut satırı arayüzü"""
    
    def __init__(self):
        self.vector_store = None
        self.qa_agent = None
        self.question_count = 0
        self.initialize_system()
    
    def initialize_system(self):
        """Sistemi başlatır"""
        try:
            print("🔄 Sistem başlatılıyor...")
            
            # Vector store'u başlat
            print("🗃️  ChromaDB başlatılıyor: data/db")
            self.vector_store = VectorStore(persist_directory="data/db")
            
            # Collection bilgilerini al
            info = self.vector_store.get_collection_info()
            document_count = info.get("document_count", 0)
            
            if document_count == 0:
                print("⚠️  Vektör veritabanında belge bulunamadı!")
                print("📝 Önce PDF'leri yüklemek için ingestion modülünü çalıştırın.")
                return False
            
            print(f"✅ ChromaDB başarıyla başlatıldı (OpenAI embeddings)")
            
            # QA Agent'ı başlat
            self.qa_agent = QAAgent()
            
            print(f"✅ Sistem hazır! {document_count:,} belge yüklü.")
            return True
            
        except Exception as e:
            print(f"❌ Sistem başlatılırken hata: {e}")
            return False
    
    def print_header(self):
        """Başlık yazdırır"""
        print("\n" + "="*66)
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║                    🚀 AMIF Grant Assistant                   ║")
        print("║                  Akıllı Hibe Danışman Sistemi               ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        print()
        print("📚 AMIF hibe belgeleri hakkında sorularınızı sorun!")
        print("💡 Komutlar: 'help' - yardım, 'clear' - ekranı temizle, 'quit' - çıkış")
        print("="*66)
    
    def print_help(self):
        """Yardım menüsünü yazdırır"""
        print("\n📖 YARDIM MENÜSÜ")
        print("="*50)
        print("🔍 Soru sorma:")
        print("   • Doğrudan sorunuzu yazın")
        print("   • Türkçe veya İngilizce sorabilirsiniz")
        print("   • Sistem otomatik olarak dili algılar")
        print()
        print("🛠️  Komutlar:")
        print("   • help    - Bu yardım menüsünü gösterir")
        print("   • clear   - Ekranı temizler")
        print("   • status  - Sistem durumunu gösterir")
        print("   • quit    - Programdan çıkar")
        print()
        print("💡 Örnek sorular:")
        print("   • AMIF hibesi nedir?")
        print("   • What are the eligibility criteria?")
        print("   • Personel maliyetleri nasıl hesaplanır?")
        print("   • How to calculate daily rates?")
        print("="*50)
    
    def print_status(self):
        """Sistem durumunu yazdırır"""
        try:
            info = self.vector_store.get_collection_info()
            print("\n📊 SİSTEM DURUMU")
            print("="*40)
            print(f"🗃️  Veritabanı: {info.get('collection_name', 'N/A')}")
            print(f"📄 Belge sayısı: {info.get('document_count', 0):,}")
            print(f"📁 Dizin: {info.get('persist_directory', 'N/A')}")
            print(f"❓ Sorulan soru: {self.question_count}")
            print("="*40)
        except Exception as e:
            print(f"❌ Durum bilgisi alınamadı: {e}")
    
    def clear_screen(self):
        """Ekranı temizler"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def format_sources(self, documents: List[Any]) -> str:
        """Kaynakları formatlar"""
        if not documents:
            return "Kaynak bulunamadı"
        
        sources = []
        for i, doc in enumerate(documents, 1):
            metadata = doc.metadata if hasattr(doc, 'metadata') else {}
            filename = metadata.get('filename', 'Bilinmeyen kaynak')
            page_number = metadata.get('page_number', 'Bilinmeyen sayfa')
            
            # Dosya adını kısalt
            if len(filename) > 50:
                filename = filename[:47] + "..."
            
            sources.append(f"[{i}] {filename} (Sayfa: {page_number})")
        
        return "\n".join(sources)
    
    def process_question(self, question: str) -> Dict[str, Any]:
        """Soruyu işler ve yanıt döndürür"""
        try:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"🔍 [{timestamp}] Aranıyor...")
            
            # Vector store'dan arama yap (dil algılaması ile)
            documents, detected_language = self.vector_store.search_with_sources(question, k=8)
            
            print(f"🔍 '{question}' için {len(documents)} sonuç bulundu")
            print(f"📊 {len(documents)} sonuç bulundu")
            
            if not documents:
                return {
                    "answer": "Sorunuzla ilgili bilgi bulunamadı. Lütfen farklı kelimeler kullanarak tekrar deneyin.",
                    "sources": [],
                    "language": detected_language
                }
            
            # QA Agent ile yanıt oluştur
            print(f"🤖 [{timestamp}] Yanıt hazırlanıyor...")
            
            # State oluştur
            state = {
                "query": question,
                "retrieved_documents": [
                    {
                        "content": doc.page_content,
                        "metadata": doc.metadata
                    } for doc in documents
                ],
                "detected_language": detected_language
            }
            
            # QA Agent'ı çalıştır
            result_state = self.qa_agent.execute(state)
            
            return {
                "answer": result_state.get("qa_response", "Yanıt oluşturulamadı."),
                "sources": documents,
                "language": detected_language
            }
            
        except Exception as e:
            print(f"❌ Soru işlenirken hata: {e}")
            return {
                "answer": f"Hata oluştu: {e}",
                "sources": [],
                "language": "tr"
            }
    
    def run(self):
        """Ana döngüyü çalıştırır"""
        if not self.vector_store or not self.qa_agent:
            print("❌ Sistem başlatılamadı. Çıkılıyor...")
            return
        
        self.clear_screen()
        self.print_header()
        
        while True:
            try:
                # Kullanıcı girişi al
                question = input(f"\n🤔 Sorunuz: ").strip()
                
                if not question:
                    continue
                
                # Komutları kontrol et
                if question.lower() == 'quit':
                    print("\n👋 Görüşmek üzere!")
                    break
                elif question.lower() == 'help':
                    self.print_help()
                    continue
                elif question.lower() == 'clear':
                    self.clear_screen()
                    self.print_header()
                    continue
                elif question.lower() == 'status':
                    self.print_status()
                    continue
                
                # Soruyu işle
                self.question_count += 1
                result = self.process_question(question)
                
                # Yanıtı göster
                print(f"\n💡 YANIT #{self.question_count}:")
                print("─" * 66)
                print(f"Yanıt: {result['answer']}")
                print("─" * 66)
                
                # Kaynakları göster
                print(f"\n📚 KAYNAKLAR:")
                sources_text = self.format_sources(result['sources'])
                print(sources_text)
                print("=" * 66)
                
            except KeyboardInterrupt:
                print("\n\n👋 Görüşmek üzere!")
                break
            except Exception as e:
                print(f"\n❌ Beklenmeyen hata: {e}")

def main():
    """Ana fonksiyon"""
    cli = AdvancedCLI()
    cli.run()

if __name__ == "__main__":
    main() 