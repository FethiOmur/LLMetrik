"""
GrantSpider Workflows Module

Bu modül GrantSpider'ın operasyonel iş akışlarını yönetir:
- Bulk Document Processing: Toplu doküman işleme
- Automated Report Generation: Otomatik rapor üretimi  
- Scheduled Analysis Jobs: Zamanlanmış analiz işleri
- Export/Import Functionality: Dışa/içe aktarım işlevleri
"""

from .bulk_processor import (
    BulkDocumentProcessor,
    ProcessingJob,
    ProcessingResult,
    ProcessingStatus,
    ProcessingConfig
)

__version__ = "1.0.0"
__author__ = "GrantSpider Analytics Team"

__all__ = [
    "BulkDocumentProcessor",
    "ProcessingJob", 
    "ProcessingResult",
    "ProcessingStatus",
    "ProcessingConfig"
] 