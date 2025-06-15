"""
Metin işleme ve chunking
"""

from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from config.settings import settings

class TextProcessor:
    """Metin işleme ve bölme işlemleri"""
    
    def __init__(self, chunk_size: int = None, chunk_overlap: int = None):
        self.chunk_size = chunk_size or settings.CHUNK_SIZE
        self.chunk_overlap = chunk_overlap or settings.CHUNK_OVERLAP
        
        # RecursiveCharacterTextSplitter oluştur
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=[
                "\n\n",  # Paragraf ayırıcıları
                "\n",    # Satır ayırıcıları
                " ",     # Kelime ayırıcıları
                ""       # Karakter ayırıcıları
            ],
            keep_separator=True
        )
    
    def process_document(self, document: Document) -> List[Document]:
        """
        Tek bir belgeyi işler ve parçalara böler
        
        Args:
            document: İşlenecek LangChain Document
            
        Returns:
            İşlenmiş Document parçalarının listesi
        """
        # Metni temizle
        cleaned_text = self._clean_text(document.page_content)
        
        # Metni parçalara böl
        chunks = self.text_splitter.split_text(cleaned_text)
        
        # Her parça için yeni Document oluştur
        processed_documents = []
        for i, chunk in enumerate(chunks):
            # Orijinal metadata'yı kopyala ve chunk bilgilerini ekle
            chunk_metadata = document.metadata.copy()
            chunk_metadata.update({
                "chunk_index": i,
                "total_chunks": len(chunks),
                "chunk_size": len(chunk)
            })
            
            chunk_document = Document(
                page_content=chunk,
                metadata=chunk_metadata
            )
            processed_documents.append(chunk_document)
        
        return processed_documents
    
    def process_documents(self, documents: List[Document]) -> List[Document]:
        """
        Birden fazla belgeyi işler
        
        Args:
            documents: İşlenecek Document listesi
            
        Returns:
            Tüm işlenmiş Document parçalarının listesi
        """
        print(f"📝 {len(documents)} belge işleniyor...")
        
        all_chunks = []
        for i, document in enumerate(documents):
            print(f"📄 İşleniyor: {document.metadata.get('filename', f'Belge {i+1}')}")
            
            chunks = self.process_document(document)
            all_chunks.extend(chunks)
            
            print(f"✂️  {len(chunks)} parçaya bölündü")
        
        print(f"🎉 Toplam {len(all_chunks)} metin parçası oluşturuldu")
        return all_chunks
    
    def _clean_text(self, text: str) -> str:
        """
        Metni temizler
        
        Args:
            text: Temizlenecek metin
            
        Returns:
            Temizlenmiş metin
        """
        if not text:
            return ""
        
        # Fazla boşlukları ve gereksiz karakterleri temizle
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # Satır başı ve sonundaki boşlukları temizle
            line = line.strip()
            
            # Boş satırları ve çok kısa satırları atla
            if len(line) > 2:
                # Fazla boşlukları tek boşluğa çevir
                line = ' '.join(line.split())
                cleaned_lines.append(line)
        
        # Satırları birleştir
        cleaned_text = '\n'.join(cleaned_lines)
        
        # Fazla satır sonlarını temizle
        while '\n\n\n' in cleaned_text:
            cleaned_text = cleaned_text.replace('\n\n\n', '\n\n')
        
        return cleaned_text.strip()
    
    def get_chunk_statistics(self, chunks: List[Document]) -> dict:
        """
        Chunk istatistiklerini döndürür
        
        Args:
            chunks: Document chunk'ları
            
        Returns:
            İstatistik bilgileri
        """
        if not chunks:
            return {"total_chunks": 0}
        
        chunk_sizes = [len(chunk.page_content) for chunk in chunks]
        
        return {
            "total_chunks": len(chunks),
            "average_chunk_size": sum(chunk_sizes) / len(chunks),
            "min_chunk_size": min(chunk_sizes),
            "max_chunk_size": max(chunk_sizes),
            "total_characters": sum(chunk_sizes),
            "documents_processed": len(set(chunk.metadata.get("filename", "") for chunk in chunks))
        } 