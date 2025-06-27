"""
GrantSpider Workflows Module

This module manages GrantSpider's operational workflows:
- Bulk Document Processing: Batch document processing
- Automated Report Generation: Automated report generation  
- Scheduled Analysis Jobs: Scheduled analysis jobs
- Export/Import Functionality: Export/import functionality
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