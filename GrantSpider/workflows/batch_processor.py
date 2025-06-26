"""
Batch Analysis Processor
Toplu belge analizi, paralel sorgu işleme ve raporlama sistemi
"""

import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any, Optional, Tuple, Union
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
import json
import uuid
from pathlib import Path
import time
from enum import Enum

from graph.multi_agent_graph import MultiAgentGraph
from memory.conversation_memory import EnhancedConversationMemory
from utils.performance_monitor import performance_tracker
from ingestion.vector_store import get_vector_store

class BatchStatus(Enum):
    """Batch işlem durumları"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class BatchQuery:
    """Tekil batch sorgusu"""
    id: str
    query: str
    language: Optional[str] = None
    priority: int = 1  # 1=high, 2=medium, 3=low
    metadata: Dict[str, Any] = field(default_factory=dict)
    expected_grant_types: List[str] = field(default_factory=list)

@dataclass
class BatchAnalysisRequest:
    """Batch analiz talebi"""
    id: str
    name: str
    description: str
    queries: List[BatchQuery]
    settings: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    max_workers: int = 3
    timeout_per_query: int = 60  # saniye
    generate_report: bool = True
    output_format: str = "json"  # json, csv, pdf
    
    def to_dict(self) -> Dict[str, Any]:
        """Dictionary'ye dönüştür"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "queries": [asdict(q) for q in self.queries],
            "settings": self.settings,
            "created_at": self.created_at.isoformat(),
            "max_workers": self.max_workers,
            "timeout_per_query": self.timeout_per_query,
            "generate_report": self.generate_report,
            "output_format": self.output_format
        }

@dataclass
class QueryResult:
    """Sorgu sonucu"""
    query_id: str
    query: str
    status: BatchStatus
    response: str = ""
    sources: List[Dict[str, Any]] = field(default_factory=list)
    processing_time: float = 0.0
    error_message: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    cross_document_analysis: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class BatchAnalysisResult:
    """Batch analiz sonucu"""
    request_id: str
    status: BatchStatus
    total_queries: int
    successful_queries: int
    failed_queries: int
    results: List[QueryResult] = field(default_factory=list)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    total_processing_time: float = 0.0
    summary_stats: Dict[str, Any] = field(default_factory=dict)
    report_path: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Dictionary'ye dönüştür"""
        return {
            "request_id": self.request_id,
            "status": self.status.value,
            "total_queries": self.total_queries,
            "successful_queries": self.successful_queries,
            "failed_queries": self.failed_queries,
            "results": [asdict(r) for r in self.results],
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "total_processing_time": self.total_processing_time,
            "summary_stats": self.summary_stats,
            "report_path": self.report_path
        }

class BatchProcessor:
    """Toplu analiz işlemcisi"""
    
    def __init__(self, output_dir: str = "interfaces/data/batch_results"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.multi_agent_graph = None
        self.vector_store = None
        self.active_jobs: Dict[str, BatchAnalysisResult] = {}
        self.job_history: List[BatchAnalysisResult] = []
        
        # Performance tracking
        self.performance_stats = {
            "total_jobs_processed": 0,
            "total_queries_processed": 0,
            "average_query_time": 0.0,
            "success_rate": 0.0
        }
        
        print("🔧 BatchProcessor başlatılıyor...")
        self._initialize_systems()
    
    def _initialize_systems(self):
        """Sistemleri başlat"""
        try:
            # Vector store'u başlat
            self.vector_store = get_vector_store()
            print("✅ Vector store hazır")
            
            # Multi-agent graph'ı başlat
            self.multi_agent_graph = MultiAgentGraph(self.vector_store)
            print("✅ Multi-agent graph hazır")
            
        except Exception as e:
            print(f"❌ Sistem başlatma hatası: {e}")
            raise
    
    async def process_batch_async(self, request: BatchAnalysisRequest) -> BatchAnalysisResult:
        """
        Asenkron batch işleme
        
        Args:
            request: Batch analiz talebi
            
        Returns:
            Batch analiz sonucu
        """
        result = BatchAnalysisResult(
            request_id=request.id,
            status=BatchStatus.RUNNING,
            total_queries=len(request.queries),
            successful_queries=0,
            failed_queries=0,
            started_at=datetime.now()
        )
        
        self.active_jobs[request.id] = result
        
        try:
            print(f"🚀 Batch analiz başlatılıyor: {request.name}")
            print(f"📊 Toplam sorgu sayısı: {len(request.queries)}")
            
            # Sorguları öncelik sırasına göre sırala
            sorted_queries = sorted(request.queries, key=lambda x: x.priority)
            
            # ThreadPoolExecutor ile paralel işleme
            with ThreadPoolExecutor(max_workers=request.max_workers) as executor:
                # Future'ları submit et
                future_to_query = {
                    executor.submit(
                        self._process_single_query, 
                        query, 
                        request.timeout_per_query
                    ): query 
                    for query in sorted_queries
                }
                
                # Sonuçları topla
                for future in as_completed(future_to_query):
                    query = future_to_query[future]
                    
                    try:
                        query_result = future.result(timeout=request.timeout_per_query + 10)
                        result.results.append(query_result)
                        
                        if query_result.status == BatchStatus.COMPLETED:
                            result.successful_queries += 1
                        else:
                            result.failed_queries += 1
                            
                        print(f"✅ Sorgu tamamlandı: {query.id[:8]}... ({result.successful_queries + result.failed_queries}/{result.total_queries})")
                        
                    except Exception as e:
                        # Hata durumu
                        error_result = QueryResult(
                            query_id=query.id,
                            query=query.query,
                            status=BatchStatus.FAILED,
                            error_message=str(e),
                            timestamp=datetime.now()
                        )
                        result.results.append(error_result)
                        result.failed_queries += 1
                        
                        print(f"❌ Sorgu hatası: {query.id[:8]}... - {str(e)}")
            
            # Batch tamamlandı
            result.status = BatchStatus.COMPLETED
            result.completed_at = datetime.now()
            result.total_processing_time = (result.completed_at - result.started_at).total_seconds()
            
            # Özet istatistikleri hesapla
            result.summary_stats = self._calculate_summary_stats(result)
            
            # Rapor oluştur
            if request.generate_report:
                result.report_path = await self._generate_batch_report(request, result)
            
            # Job'ı history'ye ekle
            self.job_history.append(result)
            if request.id in self.active_jobs:
                del self.active_jobs[request.id]
            
            # Performance stats güncelle
            self._update_performance_stats(result)
            
            print(f"🎉 Batch analiz tamamlandı: {result.successful_queries}/{result.total_queries} başarılı")
            
        except Exception as e:
            result.status = BatchStatus.FAILED
            result.completed_at = datetime.now()
            result.summary_stats["error"] = str(e)
            
            print(f"💥 Batch analiz hatası: {e}")
        
        return result
    
    def _process_single_query(self, query: BatchQuery, timeout: int) -> QueryResult:
        """
        Tekil sorgu işleme
        
        Args:
            query: İşlenecek sorgu
            timeout: Timeout süresi
            
        Returns:
            Sorgu sonucu
        """
        start_time = time.time()
        
        try:
            print(f"🔍 Sorgu işleniyor: {query.query[:50]}...")
            
            # Multi-agent graph ile işle
            result_state = self.multi_agent_graph.process_query(
                query.query,
                language=query.language or "tr"
            )
            
            processing_time = time.time() - start_time
            
            # Sonucu formatla
            query_result = QueryResult(
                query_id=query.id,
                query=query.query,
                status=BatchStatus.COMPLETED,
                response=result_state.get("cited_response", ""),
                sources=result_state.get("sources", []),
                processing_time=processing_time,
                metadata={
                    "detected_language": result_state.get("detected_language", ""),
                    "retrieval_performed": result_state.get("retrieval_performed", False),
                    "cross_document_performed": result_state.get("cross_document_performed", False),
                    "document_count": len(result_state.get("retrieved_documents", [])),
                    "query_priority": query.priority,
                    "expected_grant_types": query.expected_grant_types
                },
                cross_document_analysis=result_state.get("cross_document_analysis", {}),
                timestamp=datetime.now()
            )
            
            return query_result
            
        except Exception as e:
            processing_time = time.time() - start_time
            
            return QueryResult(
                query_id=query.id,
                query=query.query,
                status=BatchStatus.FAILED,
                error_message=str(e),
                processing_time=processing_time,
                timestamp=datetime.now()
            )
    
    def _calculate_summary_stats(self, result: BatchAnalysisResult) -> Dict[str, Any]:
        """Özet istatistiklerini hesapla"""
        if not result.results:
            return {}
        
        # Processing time stats
        processing_times = [r.processing_time for r in result.results if r.processing_time > 0]
        avg_processing_time = sum(processing_times) / len(processing_times) if processing_times else 0
        
        # Source stats
        total_sources = sum(len(r.sources) for r in result.results)
        avg_sources_per_query = total_sources / len(result.results)
        
        # Language distribution
        languages = {}
        for r in result.results:
            lang = r.metadata.get("detected_language", "unknown")
            languages[lang] = languages.get(lang, 0) + 1
        
        # Grant types analysis
        grant_types_found = set()
        for r in result.results:
            cross_doc = r.cross_document_analysis
            if cross_doc and "grant_groups" in cross_doc:
                grant_types_found.update(cross_doc["grant_groups"].keys())
        
        # Complexity analysis
        complexity_distribution = {"simple": 0, "medium": 0, "complex": 0}
        for r in result.results:
            word_count = len(r.query.split())
            if word_count < 5:
                complexity_distribution["simple"] += 1
            elif word_count < 15:
                complexity_distribution["medium"] += 1
            else:
                complexity_distribution["complex"] += 1
        
        return {
            "success_rate": (result.successful_queries / result.total_queries) * 100,
            "average_processing_time": avg_processing_time,
            "total_sources_found": total_sources,
            "average_sources_per_query": avg_sources_per_query,
            "language_distribution": languages,
            "grant_types_analyzed": list(grant_types_found),
            "query_complexity_distribution": complexity_distribution,
            "cross_document_analysis_performed": sum(1 for r in result.results 
                                                   if r.metadata.get("cross_document_performed", False)),
            "total_documents_processed": sum(r.metadata.get("document_count", 0) for r in result.results)
        }
    
    async def _generate_batch_report(self, request: BatchAnalysisRequest, result: BatchAnalysisResult) -> str:
        """Batch raporu oluştur"""
        try:
            # Rapor dosya adı
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_filename = f"batch_report_{request.id[:8]}_{timestamp}.json"
            report_path = self.output_dir / report_filename
            
            # Rapor verisi
            report_data = {
                "batch_request": request.to_dict(),
                "batch_result": result.to_dict(),
                "generated_at": datetime.now().isoformat(),
                "generator": "BatchProcessor v1.0"
            }
            
            # JSON raporu kaydet
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False, default=str)
            
            print(f"📊 Batch raporu oluşturuldu: {report_path}")
            return str(report_path)
            
        except Exception as e:
            print(f"⚠️ Rapor oluşturma hatası: {e}")
            return ""
    
    def _update_performance_stats(self, result: BatchAnalysisResult):
        """Performance istatistiklerini güncelle"""
        self.performance_stats["total_jobs_processed"] += 1
        self.performance_stats["total_queries_processed"] += result.total_queries
        
        # Average query time güncelle
        total_time = sum(r.processing_time for r in result.results if r.processing_time > 0)
        if result.total_queries > 0:
            current_avg = self.performance_stats["average_query_time"]
            new_avg_component = total_time / result.total_queries
            
            total_jobs = self.performance_stats["total_jobs_processed"]
            self.performance_stats["average_query_time"] = (
                (current_avg * (total_jobs - 1) + new_avg_component) / total_jobs
            )
        
        # Success rate güncelle
        total_successful = sum(len([r for r in job.results if r.status == BatchStatus.COMPLETED]) 
                             for job in self.job_history)
        total_processed = self.performance_stats["total_queries_processed"]
        
        if total_processed > 0:
            self.performance_stats["success_rate"] = (total_successful / total_processed) * 100
    
    def create_batch_request(self, 
                           name: str,
                           queries: List[str],
                           description: str = "",
                           max_workers: int = 3,
                           priority_levels: List[int] = None) -> BatchAnalysisRequest:
        """
        Batch request oluştur
        
        Args:
            name: Batch adı
            queries: Sorgu listesi
            description: Açıklama
            max_workers: Maksimum worker sayısı
            priority_levels: Öncelik seviyeleri
            
        Returns:
            Batch analiz talebi
        """
        request_id = str(uuid.uuid4())
        
        # BatchQuery listesi oluştur
        batch_queries = []
        for i, query_text in enumerate(queries):
            priority = priority_levels[i] if priority_levels and i < len(priority_levels) else 2
            
            batch_query = BatchQuery(
                id=str(uuid.uuid4()),
                query=query_text,
                priority=priority,
                metadata={"index": i}
            )
            batch_queries.append(batch_query)
        
        return BatchAnalysisRequest(
            id=request_id,
            name=name,
            description=description,
            queries=batch_queries,
            max_workers=max_workers
        )
    
    def get_job_status(self, job_id: str) -> Optional[BatchAnalysisResult]:
        """Job durumunu al"""
        # Aktif job'ları kontrol et
        if job_id in self.active_jobs:
            return self.active_jobs[job_id]
        
        # History'de ara
        for job in self.job_history:
            if job.request_id == job_id:
                return job
        
        return None
    
    def get_active_jobs(self) -> List[BatchAnalysisResult]:
        """Aktif job'ları döndür"""
        return list(self.active_jobs.values())
    
    def get_job_history(self, limit: int = 50) -> List[BatchAnalysisResult]:
        """Job geçmişini döndür"""
        return self.job_history[-limit:]
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Performance istatistiklerini döndür"""
        return self.performance_stats.copy()
    
    def cancel_job(self, job_id: str) -> bool:
        """Job'ı iptal et"""
        if job_id in self.active_jobs:
            self.active_jobs[job_id].status = BatchStatus.CANCELLED
            return True
        return False 