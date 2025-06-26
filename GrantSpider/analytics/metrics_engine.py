"""
Performance Metrics Engine
PHASE 3.1: Advanced Analytics & Insights

Kapsamlı performans metrikleri hesaplayan, takip eden ve analiz eden sistem.
Real-time monitoring, historical analysis, predictive metrics.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
import json
from pathlib import Path
from collections import defaultdict, deque
import threading
import time
import statistics
from enum import Enum

# Mathematical libraries
from scipy import stats
from sklearn.metrics import mean_squared_error, mean_absolute_error
import warnings
warnings.filterwarnings('ignore')

class MetricType(Enum):
    """Metrik türleri"""
    COUNTER = "counter"          # Artan sayaç
    GAUGE = "gauge"             # Anlık değer
    HISTOGRAM = "histogram"      # Dağılım
    TIMER = "timer"             # Süre ölçümü
    RATIO = "ratio"             # Oran
    RATE = "rate"               # Değişim hızı

class AlertLevel(Enum):
    """Uyarı seviyeleri"""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"

@dataclass
class MetricDefinition:
    """Metrik tanımı"""
    name: str
    metric_type: MetricType
    description: str
    unit: str
    aggregation_method: str  # sum, avg, min, max, count
    alert_thresholds: Dict[AlertLevel, float]
    retention_days: int
    tags: Dict[str, str]

@dataclass
class MetricValue:
    """Metrik değeri"""
    metric_name: str
    value: Union[float, int]
    timestamp: datetime
    tags: Dict[str, str]
    metadata: Dict[str, Any]

@dataclass
class MetricAlert:
    """Metrik uyarısı"""
    alert_id: str
    metric_name: str
    level: AlertLevel
    current_value: float
    threshold_value: float
    message: str
    timestamp: datetime
    resolved: bool
    resolution_time: Optional[datetime]

@dataclass
class PerformanceReport:
    """Performans raporu"""
    report_id: str
    period_start: datetime
    period_end: datetime
    metrics_summary: Dict[str, Any]
    trends: Dict[str, float]
    alerts: List[MetricAlert]
    recommendations: List[str]
    score: float  # 0-100 arası genel performans puanı
    created_at: datetime

class PerformanceMetricsEngine:
    """
    Performans metrikleri motoru
    
    Bu sınıf, sistem performansını izler, metrikleri hesaplar,
    trendleri analiz eder ve uyarıları yönetir.
    """
    
    def __init__(self, data_path: str = "interfaces/data"):
        """
        Metrics Engine başlatıcısı
        
        Args:
            data_path: Veri dosyalarının bulunduğu yol
        """
        self.data_path = Path(data_path)
        self.metrics_path = self.data_path / "metrics"
        self.metrics_path.mkdir(exist_ok=True)
        
        # Metrik tanımları
        self.metric_definitions = {}
        self._initialize_default_metrics()
        
        # Metrik verilerini tutma (in-memory)
        self.metric_values = defaultdict(deque)  # metrik_name -> deque of MetricValue
        self.alerts = []
        self.performance_history = []
        
        # Real-time monitoring
        self.monitoring_active = False
        self.monitoring_thread = None
        self.monitoring_interval = 30  # saniye
        
        # Agregasyon cache
        self.aggregation_cache = {}
        self.cache_ttl = 300  # 5 dakika
        
        # Alert thresholds
        self.global_alert_config = {
            "response_time_critical": 30.0,  # saniye
            "error_rate_warning": 0.05,      # %5
            "error_rate_critical": 0.15,     # %15
            "success_rate_warning": 0.85,    # %85
            "success_rate_critical": 0.70,   # %70
            "quality_score_warning": 3.0,    # 5 üzerinden
            "quality_score_critical": 2.5
        }
        
        print("📊 PerformanceMetricsEngine başlatıldı")
    
    def start_monitoring(self):
        """Gerçek zamanlı monitoring başlat"""
        if self.monitoring_active:
            print("⚠️ Monitoring zaten aktif")
            return
        
        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitoring_thread.start()
        
        print("🔄 Gerçek zamanlı monitoring başlatıldı")
    
    def stop_monitoring(self):
        """Monitoring'i durdur"""
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        
        print("⏹️ Monitoring durduruldu")
    
    def record_metric(self, 
                     metric_name: str,
                     value: Union[float, int],
                     tags: Optional[Dict[str, str]] = None,
                     timestamp: Optional[datetime] = None):
        """
        Metrik değeri kaydet
        
        Args:
            metric_name: Metrik adı
            value: Metrik değeri
            tags: Ek etiketler
            timestamp: Zaman damgası
        """
        if metric_name not in self.metric_definitions:
            print(f"⚠️ Tanımlanmamış metrik: {metric_name}")
            return
        
        # Metrik değeri oluştur
        metric_value = MetricValue(
            metric_name=metric_name,
            value=value,
            timestamp=timestamp or datetime.now(),
            tags=tags or {},
            metadata={}
        )
        
        # Belleğe ekle
        self.metric_values[metric_name].append(metric_value)
        
        # Retention kontrolü
        self._cleanup_old_metrics(metric_name)
        
        # Alert kontrolü
        self._check_alerts(metric_name, value)
        
        # Persistency (opsiyonel)
        self._persist_metric(metric_value)
    
    def get_current_metrics(self) -> Dict[str, Any]:
        """
        Güncel metrikleri al
        
        Returns:
            Güncel metrik değerleri
        """
        current_metrics = {}
        
        for metric_name, definition in self.metric_definitions.items():
            values = list(self.metric_values[metric_name])
            
            if not values:
                current_metrics[metric_name] = {
                    "value": None,
                    "timestamp": None,
                    "status": "no_data"
                }
                continue
            
            # Son değeri al
            latest_value = values[-1]
            
            # İstatistikleri hesapla (son 1 saat)
            one_hour_ago = datetime.now() - timedelta(hours=1)
            recent_values = [v.value for v in values if v.timestamp >= one_hour_ago]
            
            current_metrics[metric_name] = {
                "current_value": latest_value.value,
                "timestamp": latest_value.timestamp.isoformat(),
                "hourly_avg": np.mean(recent_values) if recent_values else None,
                "hourly_min": min(recent_values) if recent_values else None,
                "hourly_max": max(recent_values) if recent_values else None,
                "data_points": len(recent_values),
                "unit": definition.unit
            }
        
        return current_metrics
    
    def calculate_performance_score(self, 
                                  time_window: timedelta = timedelta(hours=24)) -> float:
        """
        Genel performans puanı hesapla (0-100)
        
        Args:
            time_window: Hesaplama penceresi
            
        Returns:
            Performans puanı
        """
        print("🎯 Performans puanı hesaplanıyor...")
        
        end_time = datetime.now()
        start_time = end_time - time_window
        
        # Ana metrikler ve ağırlıkları
        metric_weights = {
            "response_time": 0.25,      # %25
            "success_rate": 0.30,       # %30
            "error_rate": 0.20,         # %20 (inverse)
            "quality_score": 0.15,      # %15
            "throughput": 0.10          # %10
        }
        
        total_score = 0.0
        total_weight = 0.0
        
        for metric_name, weight in metric_weights.items():
            try:
                # Metrik değerlerini al
                values = self._get_metric_values_in_window(metric_name, start_time, end_time)
                
                if not values:
                    continue
                
                # Ortalama değeri hesapla
                avg_value = np.mean(values)
                
                # Metrik türüne göre normalize et (0-100)
                if metric_name == "response_time":
                    # Düşük daha iyi (0-60 saniye arası)
                    normalized_score = max(0, 100 - (avg_value / 60.0) * 100)
                elif metric_name == "success_rate":
                    # Yüksek daha iyi (0-1 arası)
                    normalized_score = avg_value * 100
                elif metric_name == "error_rate":
                    # Düşük daha iyi (0-1 arası)
                    normalized_score = max(0, 100 - (avg_value * 100))
                elif metric_name == "quality_score":
                    # Yüksek daha iyi (0-5 arası)
                    normalized_score = (avg_value / 5.0) * 100
                elif metric_name == "throughput":
                    # Yüksek daha iyi (normalizasyon için max değer belirle)
                    max_expected_throughput = 100  # sorgu/saat
                    normalized_score = min(100, (avg_value / max_expected_throughput) * 100)
                else:
                    normalized_score = 50  # Default
                
                # Ağırlıklı puana ekle
                total_score += normalized_score * weight
                total_weight += weight
                
                print(f"  {metric_name}: {avg_value:.2f} -> {normalized_score:.1f} (ağırlık: {weight})")
                
            except Exception as e:
                print(f"⚠️ Metrik hesaplama hatası ({metric_name}): {e}")
                continue
        
        # Final puan
        final_score = total_score / total_weight if total_weight > 0 else 0
        
        print(f"📊 Genel performans puanı: {final_score:.1f}/100")
        return final_score
    
    def generate_performance_report(self,
                                  period_start: Optional[datetime] = None,
                                  period_end: Optional[datetime] = None) -> PerformanceReport:
        """
        Detaylı performans raporu oluştur
        
        Args:
            period_start: Rapor başlangıç zamanı
            period_end: Rapor bitiş zamanı
            
        Returns:
            Performans raporu
        """
        print("📋 Performans raporu oluşturuluyor...")
        
        # Default zaman aralığı (son 24 saat)
        if not period_end:
            period_end = datetime.now()
        if not period_start:
            period_start = period_end - timedelta(days=1)
        
        # Metrik özetleri hesapla
        metrics_summary = self._calculate_metrics_summary(period_start, period_end)
        
        # Trendleri analiz et
        trends = self._analyze_metric_trends(period_start, period_end)
        
        # Aktif alert'leri al
        active_alerts = [alert for alert in self.alerts if not alert.resolved]
        
        # Önerileri oluştur
        recommendations = self._generate_performance_recommendations(metrics_summary, trends, active_alerts)
        
        # Genel performans puanı
        score = self.calculate_performance_score(period_end - period_start)
        
        # Rapor oluştur
        report_id = f"perf_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        report = PerformanceReport(
            report_id=report_id,
            period_start=period_start,
            period_end=period_end,
            metrics_summary=metrics_summary,
            trends=trends,
            alerts=active_alerts,
            recommendations=recommendations,
            score=score,
            created_at=datetime.now()
        )
        
        # Raporu kaydet
        self._save_performance_report(report)
        self.performance_history.append(report)
        
        print(f"✅ Performans raporu oluşturuldu: {report_id}")
        print(f"📊 Performans puanı: {score:.1f}/100")
        print(f"⚠️ Aktif alert sayısı: {len(active_alerts)}")
        print(f"💡 Öneri sayısı: {len(recommendations)}")
        
        return report
    
    def get_metric_trends(self, 
                         metric_name: str,
                         time_window: timedelta = timedelta(days=7)) -> Dict[str, Any]:
        """
        Spesifik metrik için trend analizi
        
        Args:
            metric_name: Metrik adı
            time_window: Analiz penceresi
            
        Returns:
            Trend analizi sonuçları
        """
        if metric_name not in self.metric_definitions:
            return {"error": f"Metrik bulunamadı: {metric_name}"}
        
        end_time = datetime.now()
        start_time = end_time - time_window
        
        values = self._get_metric_values_in_window(metric_name, start_time, end_time)
        
        if len(values) < 2:
            return {"error": "Yeterli veri yok"}
        
        try:
            # Trend hesaplamaları
            timestamps = np.arange(len(values))
            slope, intercept, r_value, p_value, std_err = stats.linregress(timestamps, values)
            
            # Trend yönü
            if abs(slope) < 0.001:
                trend_direction = "stable"
            elif slope > 0:
                trend_direction = "increasing"
            else:
                trend_direction = "decreasing"
            
            # İstatistikler
            trend_analysis = {
                "metric_name": metric_name,
                "period": f"{start_time.isoformat()} - {end_time.isoformat()}",
                "data_points": len(values),
                "trend_direction": trend_direction,
                "trend_slope": slope,
                "correlation": r_value,
                "p_value": p_value,
                "current_value": values[-1],
                "period_average": np.mean(values),
                "period_std": np.std(values),
                "min_value": min(values),
                "max_value": max(values),
                "percentiles": {
                    "25th": np.percentile(values, 25),
                    "50th": np.percentile(values, 50),
                    "75th": np.percentile(values, 75),
                    "95th": np.percentile(values, 95)
                }
            }
            
            return trend_analysis
            
        except Exception as e:
            return {"error": f"Trend analizi hatası: {e}"}
    
    def set_alert_threshold(self, 
                          metric_name: str,
                          level: AlertLevel,
                          threshold: float):
        """
        Alert threshold belirleme
        
        Args:
            metric_name: Metrik adı
            level: Alert seviyesi
            threshold: Threshold değeri
        """
        if metric_name not in self.metric_definitions:
            print(f"⚠️ Metrik bulunamadı: {metric_name}")
            return
        
        self.metric_definitions[metric_name].alert_thresholds[level] = threshold
        print(f"🚨 Alert threshold belirlendi: {metric_name} {level.value} = {threshold}")
    
    def get_active_alerts(self) -> List[MetricAlert]:
        """Aktif alert'leri döndür"""
        return [alert for alert in self.alerts if not alert.resolved]
    
    def resolve_alert(self, alert_id: str):
        """Alert'i çözümlenmiş olarak işaretle"""
        for alert in self.alerts:
            if alert.alert_id == alert_id and not alert.resolved:
                alert.resolved = True
                alert.resolution_time = datetime.now()
                print(f"✅ Alert çözümlendi: {alert_id}")
                return
        
        print(f"⚠️ Alert bulunamadı veya zaten çözümlü: {alert_id}")
    
    def export_metrics_data(self, 
                           start_time: Optional[datetime] = None,
                           end_time: Optional[datetime] = None,
                           format: str = "json") -> str:
        """
        Metrik verilerini export et
        
        Args:
            start_time: Başlangıç zamanı
            end_time: Bitiş zamanı
            format: Export formatı (json, csv)
            
        Returns:
            Export dosya yolu
        """
        try:
            if not end_time:
                end_time = datetime.now()
            if not start_time:
                start_time = end_time - timedelta(days=7)
            
            # Verileri topla
            export_data = {}
            
            for metric_name in self.metric_definitions.keys():
                values = self._get_metric_values_in_window(metric_name, start_time, end_time)
                timestamps = self._get_metric_timestamps_in_window(metric_name, start_time, end_time)
                
                export_data[metric_name] = {
                    "values": values,
                    "timestamps": [ts.isoformat() for ts in timestamps],
                    "definition": asdict(self.metric_definitions[metric_name])
                }
            
            # Export dosyası oluştur
            export_filename = f"metrics_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format}"
            export_path = self.metrics_path / export_filename
            
            if format == "json":
                with open(export_path, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, indent=2, ensure_ascii=False, default=str)
            elif format == "csv":
                # CSV için pandas kullan
                df_list = []
                for metric_name, data in export_data.items():
                    for i, (value, timestamp) in enumerate(zip(data["values"], data["timestamps"])):
                        df_list.append({
                            "metric_name": metric_name,
                            "timestamp": timestamp,
                            "value": value
                        })
                
                df = pd.DataFrame(df_list)
                df.to_csv(export_path, index=False)
            
            print(f"📤 Metrik verileri export edildi: {export_path}")
            return str(export_path)
            
        except Exception as e:
            print(f"❌ Export hatası: {e}")
            return ""
    
    def get_system_health_status(self) -> Dict[str, Any]:
        """
        Sistem sağlık durumu özeti
        
        Returns:
            Sistem sağlık raporu
        """
        try:
            current_time = datetime.now()
            one_hour_ago = current_time - timedelta(hours=1)
            
            # Ana metrikler
            health_metrics = {}
            
            for metric_name in ["response_time", "success_rate", "error_rate", "quality_score"]:
                values = self._get_metric_values_in_window(metric_name, one_hour_ago, current_time)
                
                if values:
                    health_metrics[metric_name] = {
                        "current": values[-1] if values else 0,
                        "average": np.mean(values),
                        "status": self._get_metric_health_status(metric_name, values[-1] if values else 0)
                    }
                else:
                    health_metrics[metric_name] = {
                        "current": 0,
                        "average": 0,
                        "status": "no_data"
                    }
            
            # Genel durum
            status_scores = []
            for metric_data in health_metrics.values():
                if metric_data["status"] == "healthy":
                    status_scores.append(100)
                elif metric_data["status"] == "warning":
                    status_scores.append(60)
                elif metric_data["status"] == "critical":
                    status_scores.append(20)
                else:
                    status_scores.append(50)  # no_data
            
            overall_health = np.mean(status_scores) if status_scores else 0
            
            if overall_health >= 80:
                overall_status = "healthy"
            elif overall_health >= 60:
                overall_status = "warning"
            else:
                overall_status = "critical"
            
            # Alert sayıları
            active_alerts = self.get_active_alerts()
            alert_counts = {}
            for level in AlertLevel:
                alert_counts[level.value] = len([a for a in active_alerts if a.level == level])
            
            return {
                "overall_status": overall_status,
                "overall_health_score": overall_health,
                "metrics": health_metrics,
                "active_alerts": alert_counts,
                "total_active_alerts": len(active_alerts),
                "last_updated": current_time.isoformat(),
                "uptime_percentage": self._calculate_uptime_percentage()
            }
            
        except Exception as e:
            print(f"❌ Sistem sağlık durumu hesaplama hatası: {e}")
            return {"overall_status": "unknown", "error": str(e)}
    
    # Private metodları
    def _initialize_default_metrics(self):
        """Varsayılan metrik tanımlarını başlat"""
        default_metrics = [
            MetricDefinition(
                name="response_time",
                metric_type=MetricType.TIMER,
                description="Sorgu yanıt süresi",
                unit="seconds",
                aggregation_method="avg",
                alert_thresholds={
                    AlertLevel.WARNING: 20.0,
                    AlertLevel.CRITICAL: 30.0
                },
                retention_days=30,
                tags={"category": "performance"}
            ),
            MetricDefinition(
                name="success_rate",
                metric_type=MetricType.RATIO,
                description="Başarılı sorgu oranı",
                unit="ratio",
                aggregation_method="avg",
                alert_thresholds={
                    AlertLevel.WARNING: 0.85,
                    AlertLevel.CRITICAL: 0.70
                },
                retention_days=30,
                tags={"category": "reliability"}
            ),
            MetricDefinition(
                name="error_rate",
                metric_type=MetricType.RATIO,
                description="Hata oranı",
                unit="ratio",
                aggregation_method="avg",
                alert_thresholds={
                    AlertLevel.WARNING: 0.05,
                    AlertLevel.CRITICAL: 0.15
                },
                retention_days=30,
                tags={"category": "reliability"}
            ),
            MetricDefinition(
                name="quality_score",
                metric_type=MetricType.GAUGE,
                description="Yanıt kalite puanı",
                unit="score",
                aggregation_method="avg",
                alert_thresholds={
                    AlertLevel.WARNING: 3.0,
                    AlertLevel.CRITICAL: 2.5
                },
                retention_days=30,
                tags={"category": "quality"}
            ),
            MetricDefinition(
                name="throughput",
                metric_type=MetricType.RATE,
                description="Sorgu verimi",
                unit="queries/hour",
                aggregation_method="sum",
                alert_thresholds={
                    AlertLevel.WARNING: 50.0,
                    AlertLevel.CRITICAL: 20.0
                },
                retention_days=30,
                tags={"category": "performance"}
            )
        ]
        
        for metric in default_metrics:
            self.metric_definitions[metric.name] = metric
    
    def _monitoring_loop(self):
        """Monitoring döngüsü"""
        while self.monitoring_active:
            try:
                # Mevcut sistem metriklerini topla
                self._collect_system_metrics()
                
                # Alert kontrolü
                self._check_all_alerts()
                
                # Cache temizleme
                self._cleanup_cache()
                
                time.sleep(self.monitoring_interval)
                
            except Exception as e:
                print(f"⚠️ Monitoring döngüsü hatası: {e}")
                time.sleep(self.monitoring_interval)
    
    def _collect_system_metrics(self):
        """Sistem metriklerini topla"""
        try:
            # Burada gerçek sistem metriklerini toplayabilirsiniz
            # Şimdilik simulated veriler kullanıyoruz
            
            current_time = datetime.now()
            
            # Response time (simulated)
            response_time = np.random.normal(15, 5)  # Ortalama 15s, std 5s
            response_time = max(1, response_time)    # Minimum 1s
            self.record_metric("response_time", response_time, timestamp=current_time)
            
            # Success rate (simulated)
            success_rate = min(1.0, max(0.0, np.random.normal(0.9, 0.1)))
            self.record_metric("success_rate", success_rate, timestamp=current_time)
            
            # Error rate (simulated)
            error_rate = 1.0 - success_rate
            self.record_metric("error_rate", error_rate, timestamp=current_time)
            
            # Quality score (simulated)
            quality_score = min(5.0, max(1.0, np.random.normal(4.0, 0.5)))
            self.record_metric("quality_score", quality_score, timestamp=current_time)
            
            # Throughput (simulated)
            throughput = max(0, np.random.normal(60, 15))  # Ortalama 60 query/hour
            self.record_metric("throughput", throughput, timestamp=current_time)
            
        except Exception as e:
            print(f"⚠️ Sistem metrik toplama hatası: {e}")
    
    def _cleanup_old_metrics(self, metric_name: str):
        """Eski metrikleri temizle"""
        if metric_name not in self.metric_definitions:
            return
        
        retention_days = self.metric_definitions[metric_name].retention_days
        cutoff_time = datetime.now() - timedelta(days=retention_days)
        
        values = self.metric_values[metric_name]
        
        # Eski değerleri kaldır
        while values and values[0].timestamp < cutoff_time:
            values.popleft()
    
    def _check_alerts(self, metric_name: str, value: float):
        """Spesifik metrik için alert kontrolü"""
        if metric_name not in self.metric_definitions:
            return
        
        definition = self.metric_definitions[metric_name]
        
        for level, threshold in definition.alert_thresholds.items():
            # Alert koşulunu kontrol et
            should_alert = False
            
            if metric_name in ["error_rate"]:
                # Yüksek değer kötü
                should_alert = value >= threshold
            elif metric_name in ["success_rate", "quality_score"]:
                # Düşük değer kötü
                should_alert = value <= threshold
            elif metric_name in ["response_time", "throughput"]:
                # Context'e göre değişir
                if metric_name == "response_time":
                    should_alert = value >= threshold  # Yüksek kötü
                else:  # throughput
                    should_alert = value <= threshold  # Düşük kötü
            
            if should_alert:
                # Yeni alert oluştur (eğer zaten yoksa)
                existing_alert = any(
                    alert.metric_name == metric_name and 
                    alert.level == level and 
                    not alert.resolved
                    for alert in self.alerts
                )
                
                if not existing_alert:
                    alert = MetricAlert(
                        alert_id=f"alert_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{metric_name}_{level.value}",
                        metric_name=metric_name,
                        level=level,
                        current_value=value,
                        threshold_value=threshold,
                        message=f"{metric_name} {level.value}: {value:.2f} (threshold: {threshold})",
                        timestamp=datetime.now(),
                        resolved=False,
                        resolution_time=None
                    )
                    
                    self.alerts.append(alert)
                    print(f"🚨 Yeni alert: {alert.message}")
    
    def _check_all_alerts(self):
        """Tüm aktif alert'leri kontrol et"""
        for alert in self.alerts:
            if alert.resolved:
                continue
            
            # Son metrik değerini al
            metric_values = list(self.metric_values[alert.metric_name])
            if not metric_values:
                continue
            
            current_value = metric_values[-1].value
            
            # Alert hala geçerli mi kontrol et
            still_alerting = False
            threshold = alert.threshold_value
            
            if alert.metric_name in ["error_rate"]:
                still_alerting = current_value >= threshold
            elif alert.metric_name in ["success_rate", "quality_score"]:
                still_alerting = current_value <= threshold
            elif alert.metric_name == "response_time":
                still_alerting = current_value >= threshold
            elif alert.metric_name == "throughput":
                still_alerting = current_value <= threshold
            
            # Eğer alert koşulu geçmişse otomatik resolve et
            if not still_alerting:
                alert.resolved = True
                alert.resolution_time = datetime.now()
                print(f"✅ Alert otomatik çözümlendi: {alert.alert_id}")
    
    def _cleanup_cache(self):
        """Cache temizleme"""
        current_time = time.time()
        keys_to_remove = []
        
        for key, (value, timestamp) in self.aggregation_cache.items():
            if current_time - timestamp > self.cache_ttl:
                keys_to_remove.append(key)
        
        for key in keys_to_remove:
            del self.aggregation_cache[key]
    
    def _get_metric_values_in_window(self, 
                                   metric_name: str,
                                   start_time: datetime,
                                   end_time: datetime) -> List[float]:
        """Belirli zaman aralığındaki metrik değerlerini al"""
        if metric_name not in self.metric_values:
            return []
        
        values = []
        for metric_value in self.metric_values[metric_name]:
            if start_time <= metric_value.timestamp <= end_time:
                values.append(metric_value.value)
        
        return values
    
    def _get_metric_timestamps_in_window(self,
                                       metric_name: str,
                                       start_time: datetime,
                                       end_time: datetime) -> List[datetime]:
        """Belirli zaman aralığındaki metrik timestamp'lerini al"""
        if metric_name not in self.metric_values:
            return []
        
        timestamps = []
        for metric_value in self.metric_values[metric_name]:
            if start_time <= metric_value.timestamp <= end_time:
                timestamps.append(metric_value.timestamp)
        
        return timestamps
    
    def _calculate_metrics_summary(self, 
                                 start_time: datetime,
                                 end_time: datetime) -> Dict[str, Any]:
        """Metrik özetlerini hesapla"""
        summary = {}
        
        for metric_name in self.metric_definitions.keys():
            values = self._get_metric_values_in_window(metric_name, start_time, end_time)
            
            if not values:
                summary[metric_name] = {"status": "no_data"}
                continue
            
            summary[metric_name] = {
                "count": len(values),
                "min": min(values),
                "max": max(values),
                "mean": np.mean(values),
                "median": np.median(values),
                "std": np.std(values),
                "current": values[-1] if values else None,
                "unit": self.metric_definitions[metric_name].unit
            }
        
        return summary
    
    def _analyze_metric_trends(self,
                             start_time: datetime,
                             end_time: datetime) -> Dict[str, float]:
        """Metrik trendlerini analiz et"""
        trends = {}
        
        for metric_name in self.metric_definitions.keys():
            values = self._get_metric_values_in_window(metric_name, start_time, end_time)
            
            if len(values) < 2:
                trends[metric_name] = 0.0
                continue
            
            try:
                # Linear regression slope
                x = np.arange(len(values))
                slope, _, _, _, _ = stats.linregress(x, values)
                trends[metric_name] = slope
            except:
                trends[metric_name] = 0.0
        
        return trends
    
    def _generate_performance_recommendations(self,
                                            metrics_summary: Dict[str, Any],
                                            trends: Dict[str, float],
                                            alerts: List[MetricAlert]) -> List[str]:
        """Performans önerileri oluştur"""
        recommendations = []
        
        # Alert'lere dayalı öneriler
        if alerts:
            critical_alerts = [a for a in alerts if a.level == AlertLevel.CRITICAL]
            if critical_alerts:
                recommendations.append("Kritik alert'ler mevcut - acil müdahale gerekli")
        
        # Trend'lere dayalı öneriler
        for metric_name, slope in trends.items():
            if metric_name == "response_time" and slope > 0.1:
                recommendations.append("Yanıt süresi artış trendinde - performans optimizasyonu gerekli")
            elif metric_name == "error_rate" and slope > 0.01:
                recommendations.append("Hata oranı artış trendinde - sistem kararlılığını kontrol edin")
            elif metric_name == "success_rate" and slope < -0.01:
                recommendations.append("Başarı oranı düşüş trendinde - kalite iyileştirmeleri gerekli")
        
        # Metrik özetlerine dayalı öneriler
        if "response_time" in metrics_summary:
            rt_stats = metrics_summary["response_time"]
            if rt_stats.get("mean", 0) > 20:
                recommendations.append("Ortalama yanıt süresi yüksek - caching veya optimizasyon düşünün")
        
        if "quality_score" in metrics_summary:
            qs_stats = metrics_summary["quality_score"]
            if qs_stats.get("mean", 5) < 3.5:
                recommendations.append("Yanıt kalitesi düşük - model iyileştirmesi gerekli")
        
        # Genel öneriler
        if not recommendations:
            recommendations.append("Sistem performansı normal aralıkta")
        
        return recommendations
    
    def _get_metric_health_status(self, metric_name: str, value: float) -> str:
        """Metrik sağlık durumunu belirle"""
        if metric_name not in self.metric_definitions:
            return "unknown"
        
        thresholds = self.metric_definitions[metric_name].alert_thresholds
        
        if metric_name in ["error_rate"]:
            # Yüksek değer kötü
            if AlertLevel.CRITICAL in thresholds and value >= thresholds[AlertLevel.CRITICAL]:
                return "critical"
            elif AlertLevel.WARNING in thresholds and value >= thresholds[AlertLevel.WARNING]:
                return "warning"
            else:
                return "healthy"
        elif metric_name in ["success_rate", "quality_score"]:
            # Düşük değer kötü
            if AlertLevel.CRITICAL in thresholds and value <= thresholds[AlertLevel.CRITICAL]:
                return "critical"
            elif AlertLevel.WARNING in thresholds and value <= thresholds[AlertLevel.WARNING]:
                return "warning"
            else:
                return "healthy"
        elif metric_name == "response_time":
            # Yüksek değer kötü
            if AlertLevel.CRITICAL in thresholds and value >= thresholds[AlertLevel.CRITICAL]:
                return "critical"
            elif AlertLevel.WARNING in thresholds and value >= thresholds[AlertLevel.WARNING]:
                return "warning"
            else:
                return "healthy"
        elif metric_name == "throughput":
            # Düşük değer kötü
            if AlertLevel.CRITICAL in thresholds and value <= thresholds[AlertLevel.CRITICAL]:
                return "critical"
            elif AlertLevel.WARNING in thresholds and value <= thresholds[AlertLevel.WARNING]:
                return "warning"
            else:
                return "healthy"
        
        return "unknown"
    
    def _calculate_uptime_percentage(self) -> float:
        """Uptime yüzdesini hesapla"""
        # Simplified uptime calculation
        # Son 24 saat için success rate ortalaması
        end_time = datetime.now()
        start_time = end_time - timedelta(days=1)
        
        success_values = self._get_metric_values_in_window("success_rate", start_time, end_time)
        
        if success_values:
            return np.mean(success_values) * 100
        else:
            return 95.0  # Default uptime
    
    def _save_performance_report(self, report: PerformanceReport):
        """Performans raporunu kaydet"""
        try:
            report_file = self.metrics_path / f"performance_report_{report.report_id}.json"
            
            # Serialize
            report_dict = asdict(report)
            report_dict['created_at'] = report.created_at.isoformat()
            report_dict['period_start'] = report.period_start.isoformat()
            report_dict['period_end'] = report.period_end.isoformat()
            
            # Alert'leri serialize et
            for i, alert in enumerate(report_dict['alerts']):
                alert['timestamp'] = alert['timestamp'] if isinstance(alert['timestamp'], str) else alert['timestamp'].isoformat()
                if alert['resolution_time']:
                    alert['resolution_time'] = alert['resolution_time'] if isinstance(alert['resolution_time'], str) else alert['resolution_time'].isoformat()
            
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report_dict, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Performans raporu kaydedildi: {report_file}")
            
        except Exception as e:
            print(f"⚠️ Performans raporu kaydetme hatası: {e}")
    
    def _persist_metric(self, metric_value: MetricValue):
        """Metrik değerini kalıcı olarak kaydet (opsiyonel)"""
        # Bu metodda metrikleri database'e veya dosyaya kaydedebilirsiniz
        # Şimdilik basit dosya sistemi kullanıyoruz
        try:
            daily_file = self.metrics_path / f"metrics_{metric_value.timestamp.strftime('%Y%m%d')}.jsonl"
            
            metric_dict = asdict(metric_value)
            metric_dict['timestamp'] = metric_value.timestamp.isoformat()
            
            with open(daily_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(metric_dict, ensure_ascii=False) + '\n')
                
        except Exception as e:
            # Persist hatası critical değil, log'layıp devam et
            pass 