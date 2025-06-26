"""
Workflow Scheduler
Otomatik batch işleme, zamanlanmış görevler ve iş yükü yönetimi sistemi
"""

import asyncio
import schedule
import threading
import time
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import json
from pathlib import Path

from workflows.batch_processor import BatchProcessor, BatchAnalysisRequest
from workflows.report_generator import ReportGenerator

class ScheduleType(Enum):
    """Zamanlama türleri"""
    ONCE = "once"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    INTERVAL = "interval"

@dataclass
class ScheduledTask:
    """Zamanlanmış görev"""
    id: str
    name: str
    task_type: str  # batch_analysis, report_generation, maintenance
    schedule_type: ScheduleType
    schedule_config: Dict[str, Any]  # time, interval, etc.
    task_config: Dict[str, Any]
    created_at: datetime = field(default_factory=datetime.now)
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None
    is_active: bool = True
    run_count: int = 0
    success_count: int = 0
    failure_count: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Dictionary'ye dönüştür"""
        return {
            "id": self.id,
            "name": self.name,
            "task_type": self.task_type,
            "schedule_type": self.schedule_type.value,
            "schedule_config": self.schedule_config,
            "task_config": self.task_config,
            "created_at": self.created_at.isoformat(),
            "last_run": self.last_run.isoformat() if self.last_run else None,
            "next_run": self.next_run.isoformat() if self.next_run else None,
            "is_active": self.is_active,
            "run_count": self.run_count,
            "success_count": self.success_count,
            "failure_count": self.failure_count
        }

class WorkflowScheduler:
    """Workflow zamanlayıcı sınıfı"""
    
    def __init__(self, 
                 batch_processor: Optional[BatchProcessor] = None,
                 report_generator: Optional[ReportGenerator] = None,
                 config_path: str = "interfaces/data/scheduler"):
        
        self.config_path = Path(config_path)
        self.config_path.mkdir(parents=True, exist_ok=True)
        
        # Sistem bileşenleri
        self.batch_processor = batch_processor or BatchProcessor()
        self.report_generator = report_generator or ReportGenerator()
        
        # Zamanlanmış görevler
        self.scheduled_tasks: Dict[str, ScheduledTask] = {}
        self.scheduler_thread: Optional[threading.Thread] = None
        self.is_running = False
        
        # Görev geçmişi
        self.task_history: List[Dict[str, Any]] = []
        
        # Önceden tanımlı görev şablonları
        self.task_templates = {
            "daily_analytics": {
                "name": "Daily Analytics Report",
                "task_type": "report_generation", 
                "schedule_type": ScheduleType.DAILY,
                "schedule_config": {"time": "09:00"},
                "task_config": {
                    "report_type": "analytics",
                    "time_period": "last_24_hours"
                }
            },
            "weekly_grant_analysis": {
                "name": "Weekly Grant Analysis",
                "task_type": "batch_analysis",
                "schedule_type": ScheduleType.WEEKLY,
                "schedule_config": {"day": "monday", "time": "08:00"},
                "task_config": {
                    "queries": [
                        "AMIF grants for women",
                        "AMIF grants for children", 
                        "AMIF health grants",
                        "AMIF digital grants"
                    ],
                    "analysis_type": "comparative"
                }
            },
            "monthly_performance_review": {
                "name": "Monthly Performance Review",
                "task_type": "report_generation",
                "schedule_type": ScheduleType.MONTHLY,
                "schedule_config": {"day": 1, "time": "10:00"},
                "task_config": {
                    "report_type": "comprehensive_analytics",
                    "time_period": "last_30_days",
                    "include_trends": True
                }
            }
        }
        
        print("📅 WorkflowScheduler başlatılıyor...")
        self._load_scheduled_tasks()
    
    def start_scheduler(self):
        """Scheduler'ı başlat"""
        if self.is_running:
            print("⚠️ Scheduler zaten çalışıyor")
            return
        
        self.is_running = True
        self.scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.scheduler_thread.start()
        
        print("🚀 Workflow Scheduler başlatıldı")
        print(f"📊 Aktif görev sayısı: {len([t for t in self.scheduled_tasks.values() if t.is_active])}")
    
    def stop_scheduler(self):
        """Scheduler'ı durdur"""
        self.is_running = False
        if self.scheduler_thread and self.scheduler_thread.is_alive():
            self.scheduler_thread.join(timeout=5)
        
        print("⏹️ Workflow Scheduler durduruldu")
    
    def _run_scheduler(self):
        """Scheduler ana döngüsü"""
        while self.is_running:
            try:
                schedule.run_pending()
                time.sleep(30)  # 30 saniyede bir kontrol et
            except Exception as e:
                print(f"❌ Scheduler hatası: {e}")
                time.sleep(60)  # Hata durumunda 1 dakika bekle
    
    def add_scheduled_task(self, 
                          name: str,
                          task_type: str,
                          schedule_type: ScheduleType,
                          schedule_config: Dict[str, Any],
                          task_config: Dict[str, Any]) -> str:
        """
        Zamanlanmış görev ekle
        
        Args:
            name: Görev adı
            task_type: Görev türü
            schedule_type: Zamanlama türü
            schedule_config: Zamanlama konfigürasyonu
            task_config: Görev konfigürasyonu
            
        Returns:
            Görev ID'si
        """
        task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(self.scheduled_tasks)}"
        
        task = ScheduledTask(
            id=task_id,
            name=name,
            task_type=task_type,
            schedule_type=schedule_type,
            schedule_config=schedule_config,
            task_config=task_config
        )
        
        # Schedule'a ekle
        self._schedule_task(task)
        
        self.scheduled_tasks[task_id] = task
        self._save_scheduled_tasks()
        
        print(f"✅ Zamanlanmış görev eklendi: {name} ({task_id})")
        return task_id
    
    def _schedule_task(self, task: ScheduledTask):
        """Görevi schedule'a ekle"""
        task_func = lambda: self._execute_task(task.id)
        
        if task.schedule_type == ScheduleType.DAILY:
            time_str = task.schedule_config.get("time", "09:00")
            schedule.every().day.at(time_str).do(task_func)
            
        elif task.schedule_type == ScheduleType.WEEKLY:
            day = task.schedule_config.get("day", "monday")
            time_str = task.schedule_config.get("time", "09:00")
            getattr(schedule.every(), day).at(time_str).do(task_func)
            
        elif task.schedule_type == ScheduleType.MONTHLY:
            # Basit monthly implementasyonu (her ayın 1'i)
            day = task.schedule_config.get("day", 1)
            time_str = task.schedule_config.get("time", "09:00")
            # Monthly için özel kontrol gerekli
            schedule.every().day.at(time_str).do(self._check_monthly_task, task.id, day)
            
        elif task.schedule_type == ScheduleType.INTERVAL:
            interval_minutes = task.schedule_config.get("interval_minutes", 60)
            schedule.every(interval_minutes).minutes.do(task_func)
    
    def _check_monthly_task(self, task_id: str, target_day: int):
        """Monthly görevler için özel kontrol"""
        current_day = datetime.now().day
        if current_day == target_day:
            self._execute_task(task_id)
    
    def _execute_task(self, task_id: str):
        """Görevi çalıştır"""
        if task_id not in self.scheduled_tasks:
            print(f"⚠️ Görev bulunamadı: {task_id}")
            return
        
        task = self.scheduled_tasks[task_id]
        
        if not task.is_active:
            print(f"⏭️ Görev deaktif: {task.name}")
            return
        
        print(f"▶️ Görev çalıştırılıyor: {task.name}")
        
        start_time = datetime.now()
        task.run_count += 1
        task.last_run = start_time
        
        try:
            if task.task_type == "batch_analysis":
                self._execute_batch_analysis_task(task)
            elif task.task_type == "report_generation":
                self._execute_report_generation_task(task)
            elif task.task_type == "maintenance":
                self._execute_maintenance_task(task)
            else:
                raise ValueError(f"Bilinmeyen görev türü: {task.task_type}")
            
            task.success_count += 1
            status = "success"
            error_message = None
            
        except Exception as e:
            task.failure_count += 1
            status = "failed"
            error_message = str(e)
            print(f"❌ Görev hatası: {task.name} - {e}")
        
        # Görev geçmişine ekle
        execution_time = (datetime.now() - start_time).total_seconds()
        self.task_history.append({
            "task_id": task_id,
            "task_name": task.name,
            "executed_at": start_time.isoformat(),
            "execution_time": execution_time,
            "status": status,
            "error_message": error_message
        })
        
        # Dosyaya kaydet
        self._save_scheduled_tasks()
        
        print(f"✅ Görev tamamlandı: {task.name} ({execution_time:.2f}s)")
    
    def _execute_batch_analysis_task(self, task: ScheduledTask):
        """Batch analiz görevini çalıştır"""
        config = task.task_config
        queries = config.get("queries", [])
        
        if not queries:
            raise ValueError("Batch analiz için sorgular belirtilmemiş")
        
        # Batch request oluştur
        batch_request = self.batch_processor.create_batch_request(
            name=f"Scheduled_{task.name}_{datetime.now().strftime('%Y%m%d_%H%M')}",
            queries=queries,
            description=f"Otomatik zamanlanmış analiz: {task.name}",
            max_workers=config.get("max_workers", 2)
        )
        
        # Asenkron olarak çalıştır (sync wrapper)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(
                self.batch_processor.process_batch_async(batch_request)
            )
            print(f"📊 Batch analiz tamamlandı: {result.successful_queries}/{result.total_queries} başarılı")
        finally:
            loop.close()
    
    def _execute_report_generation_task(self, task: ScheduledTask):
        """Rapor üretim görevini çalıştır"""
        config = task.task_config
        report_type = config.get("report_type", "analytics")
        
        # Batch sonuçlarını al
        batch_results = self.batch_processor.get_job_history(limit=100)
        
        if not batch_results:
            print("⚠️ Rapor için veri bulunamadı")
            return
        
        # Zaman aralığını belirle
        time_period = config.get("time_period", "all")
        if time_period == "last_24_hours":
            start_date = datetime.now() - timedelta(days=1)
            filtered_results = [r for r in batch_results 
                              if (r.started_at or datetime.now()) >= start_date]
        elif time_period == "last_7_days":
            start_date = datetime.now() - timedelta(days=7)
            filtered_results = [r for r in batch_results 
                              if (r.started_at or datetime.now()) >= start_date]
        elif time_period == "last_30_days":
            start_date = datetime.now() - timedelta(days=30)
            filtered_results = [r for r in batch_results 
                              if (r.started_at or datetime.now()) >= start_date]
        else:
            filtered_results = batch_results
        
        if report_type == "analytics" or report_type == "comprehensive_analytics":
            report = self.report_generator.generate_comprehensive_analytics_report(
                filtered_results
            )
            print(f"📈 Analitik rapor oluşturuldu: {report.report_id}")
        else:
            print(f"⚠️ Bilinmeyen rapor türü: {report_type}")
    
    def _execute_maintenance_task(self, task: ScheduledTask):
        """Bakım görevini çalıştır"""
        config = task.task_config
        maintenance_type = config.get("maintenance_type", "cleanup")
        
        if maintenance_type == "cleanup":
            # Eski dosyları temizle
            self._cleanup_old_files()
        elif maintenance_type == "backup":
            # Backup işlemi
            self._backup_data()
        else:
            print(f"⚠️ Bilinmeyen bakım türü: {maintenance_type}")
    
    def _cleanup_old_files(self):
        """Eski dosyaları temizle"""
        # 30 günden eski batch sonuçlarını temizle
        cutoff_date = datetime.now() - timedelta(days=30)
        
        # Batch results
        batch_dir = Path("interfaces/data/batch_results")
        if batch_dir.exists():
            for file_path in batch_dir.glob("*.json"):
                if file_path.stat().st_mtime < cutoff_date.timestamp():
                    file_path.unlink()
                    print(f"🗑️ Eski dosya silindi: {file_path}")
        
        print("🧹 Dosya temizliği tamamlandı")
    
    def _backup_data(self):
        """Veri yedekleme"""
        backup_dir = Path("interfaces/data/backups")
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Memory backup
        memory_dir = Path("interfaces/data/memory")
        if memory_dir.exists():
            backup_memory_dir = backup_dir / f"memory_{timestamp}"
            backup_memory_dir.mkdir()
            
            for file_path in memory_dir.glob("*.json"):
                backup_file = backup_memory_dir / file_path.name
                backup_file.write_text(file_path.read_text())
        
        print(f"💾 Veri yedekleme tamamlandı: {timestamp}")
    
    def create_task_from_template(self, template_name: str, custom_config: Dict[str, Any] = None) -> str:
        """Şablondan görev oluştur"""
        if template_name not in self.task_templates:
            raise ValueError(f"Bilinmeyen şablon: {template_name}")
        
        template = self.task_templates[template_name].copy()
        
        # Custom config ile şablonu güncelle
        if custom_config:
            template.update(custom_config)
        
        return self.add_scheduled_task(
            name=template["name"],
            task_type=template["task_type"],
            schedule_type=template["schedule_type"],
            schedule_config=template["schedule_config"],
            task_config=template["task_config"]
        )
    
    def remove_scheduled_task(self, task_id: str) -> bool:
        """Zamanlanmış görevi kaldır"""
        if task_id not in self.scheduled_tasks:
            return False
        
        task = self.scheduled_tasks[task_id]
        task.is_active = False
        
        # Schedule'dan kaldır (schedule kütüphanesi tüm job'ları temizlemek için)
        schedule.clear()
        
        # Aktif görevleri yeniden schedule'a ekle
        for remaining_task in self.scheduled_tasks.values():
            if remaining_task.is_active and remaining_task.id != task_id:
                self._schedule_task(remaining_task)
        
        self._save_scheduled_tasks()
        
        print(f"🗑️ Zamanlanmış görev kaldırıldı: {task.name}")
        return True
    
    def get_scheduled_tasks(self) -> List[ScheduledTask]:
        """Zamanlanmış görevleri döndür"""
        return list(self.scheduled_tasks.values())
    
    def get_task_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Görev geçmişini döndür"""
        return self.task_history[-limit:]
    
    def get_scheduler_stats(self) -> Dict[str, Any]:
        """Scheduler istatistiklerini döndür"""
        active_tasks = [t for t in self.scheduled_tasks.values() if t.is_active]
        
        total_runs = sum(t.run_count for t in self.scheduled_tasks.values())
        total_successes = sum(t.success_count for t in self.scheduled_tasks.values())
        
        return {
            "is_running": self.is_running,
            "total_tasks": len(self.scheduled_tasks),
            "active_tasks": len(active_tasks),
            "total_runs": total_runs,
            "total_successes": total_successes,
            "success_rate": (total_successes / total_runs * 100) if total_runs > 0 else 0,
            "task_history_size": len(self.task_history),
            "available_templates": list(self.task_templates.keys())
        }
    
    def _save_scheduled_tasks(self):
        """Zamanlanmış görevleri kaydet"""
        try:
            tasks_data = {
                "tasks": {task_id: task.to_dict() for task_id, task in self.scheduled_tasks.items()},
                "task_history": self.task_history,
                "last_updated": datetime.now().isoformat()
            }
            
            tasks_file = self.config_path / "scheduled_tasks.json"
            with open(tasks_file, 'w', encoding='utf-8') as f:
                json.dump(tasks_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"⚠️ Görev kaydetme hatası: {e}")
    
    def _load_scheduled_tasks(self):
        """Zamanlanmış görevleri yükle"""
        try:
            tasks_file = self.config_path / "scheduled_tasks.json"
            
            if tasks_file.exists():
                with open(tasks_file, 'r', encoding='utf-8') as f:
                    tasks_data = json.load(f)
                
                # Görevleri yükle
                for task_id, task_dict in tasks_data.get("tasks", {}).items():
                    task = ScheduledTask(
                        id=task_dict["id"],
                        name=task_dict["name"],
                        task_type=task_dict["task_type"],
                        schedule_type=ScheduleType(task_dict["schedule_type"]),
                        schedule_config=task_dict["schedule_config"],
                        task_config=task_dict["task_config"],
                        created_at=datetime.fromisoformat(task_dict["created_at"]),
                        last_run=datetime.fromisoformat(task_dict["last_run"]) if task_dict["last_run"] else None,
                        next_run=datetime.fromisoformat(task_dict["next_run"]) if task_dict["next_run"] else None,
                        is_active=task_dict["is_active"],
                        run_count=task_dict["run_count"],
                        success_count=task_dict["success_count"],
                        failure_count=task_dict["failure_count"]
                    )
                    
                    self.scheduled_tasks[task_id] = task
                    
                    # Aktif görevleri schedule'a ekle
                    if task.is_active:
                        self._schedule_task(task)
                
                # Görev geçmişini yükle
                self.task_history = tasks_data.get("task_history", [])
                
                print(f"✅ Zamanlanmış görevler yüklendi: {len(self.scheduled_tasks)} görev")
                
        except Exception as e:
            print(f"⚠️ Görev yükleme hatası: {e}")
    
    def __del__(self):
        """Destructor - scheduler'ı temiz kapat"""
        if hasattr(self, 'is_running') and self.is_running:
            self.stop_scheduler() 