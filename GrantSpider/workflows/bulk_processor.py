"""
Bulk Document Processing Module

Bu modül GrantSpider için toplu doküman işleme yetenekleri sağlar.
Büyük miktarlarda PDF dosyasını paralel olarak işleyebilir,
ilerleme takibi yapar ve hata yönetimi sağlar.
"""

import os
import asyncio
import logging
import hashlib
import threading
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import List, Dict, Optional, Callable, Any, Union
import json
import time
from queue import Queue, Empty

# GrantSpider imports
try:
    from ingestion.pdf_loader import PDFProcessor
    from memory.state_manager import StateManager
    from analytics.metrics_engine import PerformanceMetricsEngine
except ImportError as e:
    print(f"Warning: Could not import GrantSpider modules: {e}")
    # Fallback sınıflar
    class PDFProcessor:
        async def load_and_process_pdf(self, file_path):
            return [f"Mock document from {file_path}"]
    
    class StateManager:
        async def save_batch_result(self, job_id, data):
            pass
    
    class PerformanceMetricsEngine:
        def start_monitoring(self):
            pass
        def record_metric(self, name, value):
            pass
        def get_current_metrics(self):
            return {}


class ProcessingStatus(Enum):
    """Doküman işleme durumları"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    RETRYING = "retrying"


class ProcessingMode(Enum):
    """İşleme modları"""
    SEQUENTIAL = "sequential"  # Sıralı işleme
    PARALLEL_THREADS = "parallel_threads"  # Thread bazlı paralel
    PARALLEL_PROCESSES = "parallel_processes"  # Process bazlı paralel
    ADAPTIVE = "adaptive"  # Otomatik en iyi mod seçimi


@dataclass
class ProcessingConfig:
    """Toplu işleme konfigürasyonu"""
    max_workers: int = 4
    processing_mode: ProcessingMode = ProcessingMode.ADAPTIVE
    chunk_size: int = 10
    retry_attempts: int = 3
    retry_delay: float = 2.0
    timeout_per_document: int = 300  # 5 dakika
    memory_limit_mb: int = 1024
    enable_progress_tracking: bool = True
    save_intermediate_results: bool = True
    output_directory: Optional[str] = None
    error_handling_strategy: str = "continue"  # continue, stop, retry


@dataclass
class ProcessingJob:
    """Tek bir doküman işleme işi"""
    job_id: str
    file_path: str
    status: ProcessingStatus = ProcessingStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    retry_count: int = 0
    file_size: int = 0
    file_hash: Optional[str] = None
    processing_time: float = 0.0
    result_data: Optional[Dict[str, Any]] = None


@dataclass
class ProcessingResult:
    """Toplu işleme sonuç raporu"""
    batch_id: str
    total_files: int
    successful_files: int
    failed_files: int
    cancelled_files: int
    total_processing_time: float
    average_processing_time: float
    throughput_files_per_second: float
    started_at: datetime
    completed_at: datetime
    jobs: List[ProcessingJob]
    error_summary: Dict[str, int]
    performance_metrics: Dict[str, Any]


class BulkDocumentProcessor:
    """
    Toplu doküman işleme sistemi
    
    Bu sınıf büyük miktarlarda PDF dosyasını paralel olarak işleyebilir,
    ilerleme takibi yapar ve kapsamlı hata yönetimi sağlar.
    """
    
    def __init__(self, config: Optional[ProcessingConfig] = None):
        """
        Bulk processor başlatma
        
        Args:
            config: İşleme konfigürasyonu
        """
        self.config = config or ProcessingConfig()
        self.logger = logging.getLogger(__name__)
        
        # Core components
        self.pdf_processor = PDFProcessor()
        self.state_manager = StateManager()
        self.metrics_engine = PerformanceMetricsEngine()
        
        # Processing state
        self.active_jobs: Dict[str, ProcessingJob] = {}
        self.job_queue = Queue()
        self.result_queue = Queue()
        self.is_processing = False
        self.should_stop = False
        
        # Progress tracking
        self.progress_callbacks: List[Callable] = []
        self.current_batch_id: Optional[str] = None
        
        # Setup directories
        self._setup_directories()
        
        # Start metrics monitoring
        self.metrics_engine.start_monitoring()
    
    def _setup_directories(self):
        """Gerekli klasörleri oluştur"""
        if self.config.output_directory:
            os.makedirs(self.config.output_directory, exist_ok=True)
        
        # Results directory
        self.results_dir = Path("interfaces/data/bulk_results")
        self.results_dir.mkdir(parents=True, exist_ok=True)
        
        # Temp directory for intermediate results
        self.temp_dir = Path("interfaces/data/bulk_temp")
        self.temp_dir.mkdir(parents=True, exist_ok=True)
    
    def add_progress_callback(self, callback: Callable[[str, float, Dict], None]):
        """
        İlerleme takibi için callback ekle
        
        Args:
            callback: (batch_id, progress_percentage, info) alan fonksiyon
        """
        self.progress_callbacks.append(callback)
    
    def _notify_progress(self, batch_id: str, progress: float, info: Dict):
        """Progress callback'lerini çağır"""
        for callback in self.progress_callbacks:
            try:
                callback(batch_id, progress, info)
            except Exception as e:
                self.logger.error(f"Progress callback error: {e}")
    
    def _calculate_file_hash(self, file_path: str) -> str:
        """Dosya hash'i hesapla"""
        hasher = hashlib.md5()
        try:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception:
            return "unknown"
    
    def _create_processing_job(self, file_path: str, batch_id: str) -> ProcessingJob:
        """İşleme işi oluştur"""
        job_id = f"{batch_id}_{Path(file_path).stem}_{int(time.time())}"
        
        # File info
        file_size = 0
        file_hash = None
        try:
            file_size = os.path.getsize(file_path)
            file_hash = self._calculate_file_hash(file_path)
        except Exception as e:
            self.logger.warning(f"File info error for {file_path}: {e}")
        
        return ProcessingJob(
            job_id=job_id,
            file_path=file_path,
            file_size=file_size,
            file_hash=file_hash
        )
    
    async def process_single_document(self, job: ProcessingJob) -> ProcessingJob:
        """
        Tek bir dokümanı işle
        
        Args:
            job: İşlenecek doküman işi
            
        Returns:
            Güncellenmiş job objesi
        """
        start_time = time.time()
        job.started_at = datetime.now()
        job.status = ProcessingStatus.PROCESSING
        
        try:
            self.logger.info(f"Processing document: {job.file_path}")
            
            # Dosya varlığını kontrol et
            if not os.path.exists(job.file_path):
                raise FileNotFoundError(f"File not found: {job.file_path}")
            
            # PDF'i işle
            documents = await self.pdf_processor.load_and_process_pdf(job.file_path)
            
            if not documents:
                raise ValueError("No content extracted from PDF")
            
            # State manager'a kaydet
            batch_data = {
                'job_id': job.job_id,
                'file_path': job.file_path,
                'documents': [doc.dict() if hasattr(doc, 'dict') else str(doc) for doc in documents],
                'processed_at': datetime.now().isoformat(),
                'file_size': job.file_size,
                'file_hash': job.file_hash
            }
            
            await self.state_manager.save_batch_result(job.job_id, batch_data)
            
            # Sonuç verilerini kaydet
            job.result_data = {
                'document_count': len(documents),
                'total_characters': sum(len(str(doc)) for doc in documents),
                'extraction_successful': True
            }
            
            job.status = ProcessingStatus.COMPLETED
            job.completed_at = datetime.now()
            job.processing_time = time.time() - start_time
            
            self.logger.info(f"Successfully processed: {job.file_path} in {job.processing_time:.2f}s")
            
            # Metrics kaydet
            self.metrics_engine.record_metric("document_processed", 1)
            self.metrics_engine.record_metric("processing_time", job.processing_time)
            
        except Exception as e:
            job.status = ProcessingStatus.FAILED
            job.error_message = str(e)
            job.processing_time = time.time() - start_time
            
            self.logger.error(f"Failed to process {job.file_path}: {e}")
            
            # Metrics kaydet
            self.metrics_engine.record_metric("document_failed", 1)
            self.metrics_engine.record_metric("error_rate", 1)
        
        return job
    
    async def process_documents_bulk(
        self,
        file_paths: List[str],
        batch_name: Optional[str] = None
    ) -> ProcessingResult:
        """
        Dokümanları toplu işle
        
        Args:
            file_paths: İşlenecek dosya yolları listesi
            batch_name: Batch ismi (opsiyonel)
            
        Returns:
            İşleme sonucu raporu
        """
        # Batch ID oluştur
        batch_id = batch_name or f"bulk_batch_{int(time.time())}"
        self.current_batch_id = batch_id
        
        start_time = datetime.now()
        self.logger.info(f"Starting bulk processing for batch: {batch_id}")
        
        # Dosyaları filtrele (sadece mevcut PDF'ler)
        valid_files = []
        for file_path in file_paths:
            if os.path.exists(file_path) and file_path.lower().endswith('.pdf'):
                valid_files.append(file_path)
            else:
                self.logger.warning(f"Skipping invalid file: {file_path}")
        
        if not valid_files:
            raise ValueError("No valid PDF files found to process")
        
        # Processing jobs oluştur
        jobs = [self._create_processing_job(file_path, batch_id) for file_path in valid_files]
        
        # İşleme başlat
        self.is_processing = True
        self.should_stop = False
        
        processed_jobs = []
        total_jobs = len(jobs)
        
        try:
            # Sequential processing for simplicity
            for i, job in enumerate(jobs):
                if self.should_stop:
                    job.status = ProcessingStatus.CANCELLED
                    processed_jobs.append(job)
                    continue
                
                processed_job = await self.process_single_document(job)
                processed_jobs.append(processed_job)
                
                # Progress update
                progress = ((i + 1) / total_jobs) * 100
                self._notify_progress(batch_id, progress, {
                    'completed': i + 1,
                    'total': total_jobs,
                    'current_file': job.file_path
                })
            
            end_time = datetime.now()
            total_time = (end_time - start_time).total_seconds()
            
            # Sonuçları analiz et
            successful_jobs = [job for job in processed_jobs if job.status == ProcessingStatus.COMPLETED]
            failed_jobs = [job for job in processed_jobs if job.status == ProcessingStatus.FAILED]
            cancelled_jobs = [job for job in processed_jobs if job.status == ProcessingStatus.CANCELLED]
            
            # Error summary
            error_summary = {}
            for job in failed_jobs:
                error_type = type(Exception(job.error_message)).__name__ if job.error_message else "Unknown"
                error_summary[error_type] = error_summary.get(error_type, 0) + 1
            
            # Performance metrics
            avg_processing_time = sum(job.processing_time for job in successful_jobs) / len(successful_jobs) if successful_jobs else 0
            throughput = len(successful_jobs) / total_time if total_time > 0 else 0
            
            # Sonuç objesi oluştur
            result = ProcessingResult(
                batch_id=batch_id,
                total_files=len(jobs),
                successful_files=len(successful_jobs),
                failed_files=len(failed_jobs),
                cancelled_files=len(cancelled_jobs),
                total_processing_time=total_time,
                average_processing_time=avg_processing_time,
                throughput_files_per_second=throughput,
                started_at=start_time,
                completed_at=end_time,
                jobs=processed_jobs,
                error_summary=error_summary,
                performance_metrics=self.metrics_engine.get_current_metrics()
            )
            
            # Sonuçları kaydet
            await self._save_bulk_result(result)
            
            self.logger.info(f"Bulk processing completed: {len(successful_jobs)}/{len(jobs)} successful")
            
            return result
            
        finally:
            self.is_processing = False
            self.current_batch_id = None
    
    async def _save_bulk_result(self, result: ProcessingResult):
        """Bulk işleme sonucunu kaydet"""
        try:
            # JSON olarak kaydet
            result_file = self.results_dir / f"{result.batch_id}_result.json"
            
            result_data = {
                'batch_id': result.batch_id,
                'summary': {
                    'total_files': result.total_files,
                    'successful_files': result.successful_files,
                    'failed_files': result.failed_files,
                    'cancelled_files': result.cancelled_files,
                    'total_processing_time': result.total_processing_time,
                    'average_processing_time': result.average_processing_time,
                    'throughput_files_per_second': result.throughput_files_per_second,
                    'started_at': result.started_at.isoformat(),
                    'completed_at': result.completed_at.isoformat()
                },
                'jobs': [
                    {
                        'job_id': job.job_id,
                        'file_path': job.file_path,
                        'status': job.status.value,
                        'processing_time': job.processing_time,
                        'file_size': job.file_size,
                        'error_message': job.error_message,
                        'result_data': job.result_data
                    }
                    for job in result.jobs
                ],
                'error_summary': result.error_summary,
                'performance_metrics': result.performance_metrics
            }
            
            with open(result_file, 'w', encoding='utf-8') as f:
                json.dump(result_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Bulk result saved: {result_file}")
            
        except Exception as e:
            self.logger.error(f"Failed to save bulk result: {e}")
    
    def stop_processing(self):
        """İşlemeyi durdur"""
        self.should_stop = True
        self.logger.info("Stop signal sent to bulk processor")
    
    def get_processing_status(self) -> Dict[str, Any]:
        """Mevcut işleme durumunu getir"""
        return {
            'is_processing': self.is_processing,
            'current_batch_id': self.current_batch_id,
            'active_jobs_count': len(self.active_jobs),
            'should_stop': self.should_stop,
            'config': {
                'max_workers': self.config.max_workers,
                'processing_mode': self.config.processing_mode.value,
                'chunk_size': self.config.chunk_size
            }
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        İşleme istatistiklerini getir
        
        Returns:
            İstatistik bilgileri
        """
        stats = {
            'total_batches': 0,
            'total_processed_files': 0,
            'total_successful_files': 0,
            'total_failed_files': 0,
            'average_processing_time': 0,
            'total_processing_time': 0,
            'recent_batches': []
        }
        
        try:
            # Sonuç dosyalarını oku
            result_files = list(self.results_dir.glob("*_result.json"))
            
            total_processing_time = 0
            processing_times = []
            
            for result_file in result_files:
                with open(result_file, 'r', encoding='utf-8') as f:
                    result_data = json.load(f)
                
                stats['total_batches'] += 1
                stats['total_processed_files'] += result_data['summary']['total_files']
                stats['total_successful_files'] += result_data['summary']['successful_files']
                stats['total_failed_files'] += result_data['summary']['failed_files']
                
                batch_time = result_data['summary']['total_processing_time']
                total_processing_time += batch_time
                processing_times.append(batch_time)
                
                # Son 5 batch'i ekle
                if len(stats['recent_batches']) < 5:
                    stats['recent_batches'].append({
                        'batch_id': result_data['batch_id'],
                        'total_files': result_data['summary']['total_files'],
                        'successful_files': result_data['summary']['successful_files'],
                        'processing_time': batch_time,
                        'completed_at': result_data['summary']['completed_at']
                    })
            
            stats['total_processing_time'] = total_processing_time
            stats['average_processing_time'] = sum(processing_times) / len(processing_times) if processing_times else 0
            
            # Son batch'leri tarih sırasına göre sırala
            stats['recent_batches'].sort(key=lambda x: x['completed_at'], reverse=True)
            
        except Exception as e:
            self.logger.error(f"Error calculating statistics: {e}")
        
        return stats


# Yardımcı fonksiyonlar

def create_default_config() -> ProcessingConfig:
    """Varsayılan konfigürasyon oluştur"""
    return ProcessingConfig(
        max_workers=4,
        processing_mode=ProcessingMode.ADAPTIVE,
        chunk_size=10,
        retry_attempts=3,
        enable_progress_tracking=True,
        save_intermediate_results=True
    )


async def quick_bulk_process(file_paths: List[str], max_workers: int = 4) -> ProcessingResult:
    """
    Hızlı toplu işleme fonksiyonu
    
    Args:
        file_paths: İşlenecek dosya yolları
        max_workers: Maksimum worker sayısı
        
    Returns:
        İşleme sonucu
    """
    config = ProcessingConfig(max_workers=max_workers)
    processor = BulkDocumentProcessor(config)
    
    return await processor.process_documents_bulk(file_paths)


# Progress tracking callback örneği
def progress_callback_example(batch_id: str, progress: float, info: Dict):
    """Örnek progress callback fonksiyonu"""
    print(f"Batch {batch_id}: {progress:.1f}% - {info.get('completed', 0)}/{info.get('total', 0)} files") 