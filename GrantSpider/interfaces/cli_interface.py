"""
CLI (Command Line Interface) arayüzü
"""

import click
from typing import Optional
from graph.multi_agent_graph import MultiAgentGraph
from ingestion.vector_store import VectorStore
from memory.conversation_memory import ConversationMemory

class CLIInterface:
    """CLI arayüz sınıfı"""
    
    def __init__(self):
        self.vector_store = VectorStore()
        self.multi_agent_graph = MultiAgentGraph(self.vector_store)
        self.conversation_memory = ConversationMemory()
        self.session_id = "cli_session"
    
    def start_chat(self):
        """Sohbet başlatır"""
        click.echo("🤖 GrantSpider Chatbot'a hoş geldiniz!")
        click.echo("Grant belgeleri hakkında sorularınızı sorabilirsiniz.")
        click.echo("Çıkmak için 'quit', 'exit' veya 'q' yazın.\n")
        
        while True:
            try:
                # Kullanıcı girişi al
                user_input = click.prompt("Siz", type=str).strip()
                
                # Çıkış komutu kontrolü
                if user_input.lower() in ['quit', 'exit', 'q']:
                    click.echo("Hoşça kalın! 👋")
                    break
                
                if not user_input:
                    continue
                
                # Kullanıcı mesajını belleğe ekle
                self.conversation_memory.add_user_message(user_input)
                
                # Graf'ı çalıştır
                click.echo("🔍 Belgeler aranıyor...")
                result = self.multi_agent_graph.run(user_input, self.session_id)
                
                # Yanıtı göster
                response = result.get("cited_response", result.get("qa_response", "Yanıt bulunamadı."))
                click.echo(f"\n🤖 GrantSpider: {response}\n")
                
                # Asistan mesajını belleğe ekle
                self.conversation_memory.add_assistant_message(response)
                
            except KeyboardInterrupt:
                click.echo("\n\nHoşça kalın! 👋")
                break
            except Exception as e:
                click.echo(f"❌ Hata: {e}")

@click.group()
def cli():
    """GrantSpider CLI - Grant belgeleriniz için AI asistan"""
    pass

@cli.command()
@click.option('--pdf-dir', '-d', help='PDF dosyalarının bulunduğu dizin', required=True)
def ingest(pdf_dir: str):
    """PDF dosyalarını sisteme yükler"""
    try:
        from ingestion.pdf_loader import PDFLoader
        from ingestion.text_processor import TextProcessor
        
        click.echo(f"📂 PDF dosyaları yükleniyor: {pdf_dir}")
        
        # PDF'leri yükle
        loader = PDFLoader()
        documents = loader.load_directory(pdf_dir)
        click.echo(f"✅ {len(documents)} PDF dosyası yüklendi")
        
        # Metinleri işle
        processor = TextProcessor()
        chunks = processor.process_documents(documents)
        click.echo(f"✅ {len(chunks)} metin parçası oluşturuldu")
        
        # Vektör veritabanına ekle
        vector_store = VectorStore()
        vector_store.add_documents(chunks)
        click.echo("✅ Belgeler vektör veritabanına eklendi")
        
        click.echo("🎉 Belge yükleme işlemi tamamlandı!")
        
    except Exception as e:
        click.echo(f"❌ Hata: {e}")

@cli.command()
def chat():
    """Sohbet modunu başlatır"""
    cli_interface = CLIInterface()
    cli_interface.start_chat()

@cli.command()
@click.option('--query', '-q', help='Sorulacak soru', required=True)
def ask(query: str):
    """Tek soru sorar"""
    try:
        cli_interface = CLIInterface()
        result = cli_interface.multi_agent_graph.run(query, "single_query")
        
        response = result.get("cited_response", result.get("qa_response", "Yanıt bulunamadı."))
        click.echo(f"\n🤖 GrantSpider: {response}")
        
    except Exception as e:
        click.echo(f"❌ Hata: {e}")

if __name__ == "__main__":
    cli() 