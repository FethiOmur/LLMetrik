"""
Yardımcı fonksiyonlar
"""

import os
import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime

def generate_session_id() -> str:
    """
    Benzersiz session ID oluşturur
    
    Returns:
        UUID formatında session ID
    """
    return str(uuid.uuid4())

def format_timestamp(timestamp: datetime = None) -> str:
    """
    Zaman damgasını formatlar
    
    Args:
        timestamp: Zaman damgası, None ise şu anki zaman
        
    Returns:
        Formatlanmış zaman string'i
    """
    if timestamp is None:
        timestamp = datetime.now()
    
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")

def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Metni belirli uzunlukta keser
    
    Args:
        text: Kesilecek metin
        max_length: Maksimum uzunluk
        
    Returns:
        Kesilmiş metin
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length-3] + "..."

def clean_filename(filename: str) -> str:
    """
    Dosya adını temizler
    
    Args:
        filename: Temizlenecek dosya adı
        
    Returns:
        Temizlenmiş dosya adı
    """
    # Özel karakterleri temizle
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    return filename.strip()

def ensure_directory_exists(directory_path: str):
    """
    Dizinin var olduğundan emin olur, yoksa oluşturur
    
    Args:
        directory_path: Dizin yolu
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path, exist_ok=True)

def calculate_similarity_percentage(score: float) -> str:
    """
    Benzerlik skorunu yüzde formatına çevirir
    
    Args:
        score: 0-1 arası benzerlik skoru
        
    Returns:
        Yüzde formatında string
    """
    percentage = score * 100
    return f"{percentage:.1f}%"

def extract_file_extension(filename: str) -> str:
    """
    Dosya uzantısını çıkarır
    
    Args:
        filename: Dosya adı
        
    Returns:
        Dosya uzantısı (nokta olmadan)
    """
    return os.path.splitext(filename)[1].lower().lstrip('.')

def format_file_size(size_bytes: int) -> str:
    """
    Dosya boyutunu okunabilir formata çevirir
    
    Args:
        size_bytes: Byte cinsinden dosya boyutu
        
    Returns:
        Formatlanmış dosya boyutu
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    
    while size_bytes >= 1024 and i < len(size_names)-1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"

def validate_query(query: str) -> bool:
    """
    Sorgu geçerliliğini kontrol eder
    
    Args:
        query: Kontrol edilecek sorgu
        
    Returns:
        Geçerli ise True
    """
    if not query or not query.strip():
        return False
    
    if len(query.strip()) < 3:
        return False
    
    return True

def extract_keywords(text: str, min_length: int = 3) -> List[str]:
    """
    Metinden anahtar kelimeleri çıkarır
    
    Args:
        text: Analiz edilecek metin
        min_length: Minimum kelime uzunluğu
        
    Returns:
        Anahtar kelimeler listesi
    """
    # Basit keyword extraction
    words = text.lower().split()
    
    # Stop words (Türkçe)
    stop_words = {
        've', 'ile', 'bu', 'bir', 'için', 'den', 'dan', 'de', 'da',
        'ki', 'olan', 'olarak', 'olan', 'sonra', 'kadar', 'daha',
        'çok', 'az', 'gibi', 'ancak', 'fakat', 'ama', 'veya', 'ya',
        'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been'
    }
    
    keywords = []
    for word in words:
        # Temizle
        word = word.strip('.,!?;:"()[]{}')
        
        # Koşulları kontrol et
        if (len(word) >= min_length and 
            word.lower() not in stop_words and 
            word.isalpha()):
            keywords.append(word.lower())
    
    return list(set(keywords))  # Benzersiz kelimeler 