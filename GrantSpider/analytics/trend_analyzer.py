"""
Grant Trend Analyzer
PHASE 3.1: Advanced Analytics & Insights

Advanced system for analyzing grant trends.
Time series analysis, seasonal trends, success rates.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
import json
from pathlib import Path
from collections import defaultdict, Counter
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

@dataclass
class TrendData:
    """Data class for trend data"""
    period: str
    grant_type: str
    value: float
    metric_type: str  # funding_amount, application_count, success_rate
    metadata: Dict[str, Any]

@dataclass
class TrendAnalysisResult:
    """Trend analysis result"""
    analysis_id: str
    analysis_type: str
    period_start: datetime
    period_end: datetime
    trends: List[TrendData]
    insights: List[str]
    visualizations: List[Dict[str, Any]]
    statistics: Dict[str, Any]
    created_at: datetime

class GrantTrendAnalyzer:
    """
    Advanced system for grant trend analysis
    
    This class analyzes trends, seasonal changes and success rates
    of AMIF grants over time.
    """
    
    def __init__(self, data_path: str = "interfaces/data"):
        """
        GrantTrendAnalyzer başlatıcısı
        
        Args:
            data_path: Veri dosyalarının bulunduğu yol
        """
        self.data_path = Path(data_path)
        self.trend_cache = {}
        self.analysis_history = []
        
        # Analiz konfigürasyonu
        self.config = {
            "trend_window": 30,  # gün
            "seasonal_periods": [7, 30, 90, 365],  # gün (haftalık, aylık, üç aylık, yıllık)
            "significance_level": 0.05,
            "min_data_points": 10
        }
        
        # Grant kategorileri ve metrikleri
        self.grant_categories = [
            "WOMEN", "CHILDREN", "DISABLED", "ELDERLY", "MIGRANTS", 
            "HEALTH", "EDUCATION", "INTEGRATION", "WELFARE"
        ]
        
        self.metrics = [
            "funding_amount", "application_count", "success_rate",
            "processing_time", "response_quality", "user_satisfaction"
        ]
        
        print("📊 GrantTrendAnalyzer başlatıldı")
    
    def analyze_historical_trends(self, 
                                time_range: Optional[Tuple[datetime, datetime]] = None,
                                grant_types: Optional[List[str]] = None) -> TrendAnalysisResult:
        """
        Geçmiş verilerin trend analizini yapar
        
        Args:
            time_range: Analiz edilecek zaman aralığı
            grant_types: Analiz edilecek grant türleri
            
        Returns:
            Trend analiz sonucu
        """
        print("📈 Geçmiş trend analizi başlatılıyor...")
        
        # Veri yükleme
        historical_data = self._load_historical_data(time_range, grant_types)
        
        if not historical_data:
            print("⚠️ Yeterli geçmiş veri bulunamadı")
            return self._create_empty_result("historical_trends")
        
        # Trend hesaplamaları
        trends = []
        insights = []
        visualizations = []
        statistics = {}
        
        # 1. Zaman serisi analizi
        time_series_analysis = self._analyze_time_series(historical_data)
        trends.extend(time_series_analysis["trends"])
        insights.extend(time_series_analysis["insights"])
        visualizations.extend(time_series_analysis["visualizations"])
        statistics.update(time_series_analysis["statistics"])
        
        # 2. Mevsimsel analiz
        seasonal_analysis = self._analyze_seasonal_patterns(historical_data)
        trends.extend(seasonal_analysis["trends"])
        insights.extend(seasonal_analysis["insights"])
        visualizations.extend(seasonal_analysis["visualizations"])
        statistics.update(seasonal_analysis["statistics"])
        
        # 3. Grant türü analizi
        grant_type_analysis = self._analyze_grant_type_trends(historical_data)
        trends.extend(grant_type_analysis["trends"])
        insights.extend(grant_type_analysis["insights"])
        visualizations.extend(grant_type_analysis["visualizations"])
        statistics.update(grant_type_analysis["statistics"])
        
        # Sonuç oluşturma
        analysis_id = f"historical_trends_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        result = TrendAnalysisResult(
            analysis_id=analysis_id,
            analysis_type="historical_trends",
            period_start=time_range[0] if time_range else datetime.now() - timedelta(days=365),
            period_end=time_range[1] if time_range else datetime.now(),
            trends=trends,
            insights=insights,
            visualizations=visualizations,
            statistics=statistics,
            created_at=datetime.now()
        )
        
        # Sonucu kaydet
        self._save_analysis_result(result)
        self.analysis_history.append(result)
        
        print(f"✅ Trend analizi tamamlandı: {analysis_id}")
        print(f"📊 {len(trends)} trend, {len(insights)} insight bulundu")
        
        return result
    
    def analyze_real_time_trends(self, 
                               window_size: int = 7) -> TrendAnalysisResult:
        """
        Gerçek zamanlı trend analizi
        
        Args:
            window_size: Analiz penceresi (gün)
            
        Returns:
            Gerçek zamanlı trend analizi
        """
        print(f"⚡ Gerçek zamanlı trend analizi başlatılıyor (son {window_size} gün)...")
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=window_size)
        
        # Son dönem verilerini yükle
        recent_data = self._load_historical_data((start_date, end_date))
        
        if not recent_data:
            print("⚠️ Yeterli güncel veri bulunamadı")
            return self._create_empty_result("real_time_trends")
        
        trends = []
        insights = []
        visualizations = []
        statistics = {}
        
        # 1. Momentum analizi
        momentum_analysis = self._analyze_momentum(recent_data)
        trends.extend(momentum_analysis["trends"])
        insights.extend(momentum_analysis["insights"])
        visualizations.extend(momentum_analysis["visualizations"])
        statistics.update(momentum_analysis["statistics"])
        
        # 2. Anomali tespiti
        anomaly_analysis = self._detect_anomalies(recent_data)
        trends.extend(anomaly_analysis["trends"])
        insights.extend(anomaly_analysis["insights"])
        visualizations.extend(anomaly_analysis["visualizations"])
        statistics.update(anomaly_analysis["statistics"])
        
        # 3. Performans değişimleri
        performance_analysis = self._analyze_performance_changes(recent_data)
        trends.extend(performance_analysis["trends"])
        insights.extend(performance_analysis["insights"])
        visualizations.extend(performance_analysis["visualizations"])
        statistics.update(performance_analysis["statistics"])
        
        # Sonuç oluşturma
        analysis_id = f"realtime_trends_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        result = TrendAnalysisResult(
            analysis_id=analysis_id,
            analysis_type="real_time_trends",
            period_start=start_date,
            period_end=end_date,
            trends=trends,
            insights=insights,
            visualizations=visualizations,
            statistics=statistics,
            created_at=datetime.now()
        )
        
        # Sonucu kaydet
        self._save_analysis_result(result)
        self.analysis_history.append(result)
        
        print(f"✅ Gerçek zamanlı analiz tamamlandı: {analysis_id}")
        
        return result
    
    def compare_periods(self, 
                       period1: Tuple[datetime, datetime],
                       period2: Tuple[datetime, datetime],
                       metrics: Optional[List[str]] = None) -> TrendAnalysisResult:
        """
        İki dönemin karşılaştırmalı analizi
        
        Args:
            period1: İlk dönem
            period2: İkinci dönem  
            metrics: Karşılaştırılacak metrikler
            
        Returns:
            Karşılaştırmalı analiz sonucu
        """
        print("🔀 Dönem karşılaştırma analizi başlatılıyor...")
        
        if not metrics:
            metrics = self.metrics
        
        # İki dönem için veri yükle
        data1 = self._load_historical_data(period1)
        data2 = self._load_historical_data(period2)
        
        if not data1 or not data2:
            print("⚠️ Karşılaştırma için yeterli veri bulunamadı")
            return self._create_empty_result("period_comparison")
        
        trends = []
        insights = []
        visualizations = []
        statistics = {}
        
        # Her metrik için karşılaştırma
        for metric in metrics:
            comparison = self._compare_metric_between_periods(
                data1, data2, metric, period1, period2
            )
            trends.extend(comparison["trends"])
            insights.extend(comparison["insights"])
            visualizations.extend(comparison["visualizations"])
            statistics[metric] = comparison["statistics"]
        
        # Genel karşılaştırma istatistikleri
        overall_stats = self._calculate_overall_comparison_stats(data1, data2)
        statistics["overall"] = overall_stats
        insights.extend(overall_stats["insights"])
        
        # Sonuç oluşturma
        analysis_id = f"period_comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        result = TrendAnalysisResult(
            analysis_id=analysis_id,
            analysis_type="period_comparison",
            period_start=min(period1[0], period2[0]),
            period_end=max(period1[1], period2[1]),
            trends=trends,
            insights=insights,
            visualizations=visualizations,
            statistics=statistics,
            created_at=datetime.now()
        )
        
        # Sonucu kaydet
        self._save_analysis_result(result)
        self.analysis_history.append(result)
        
        print(f"✅ Dönem karşılaştırması tamamlandı: {analysis_id}")
        
        return result
    
    def predict_future_trends(self, 
                            forecast_days: int = 30,
                            confidence_level: float = 0.95) -> TrendAnalysisResult:
        """
        Gelecek trend tahmini
        
        Args:
            forecast_days: Tahmin günü sayısı
            confidence_level: Güven seviyesi
            
        Returns:
            Gelecek trend tahmini
        """
        print(f"🔮 {forecast_days} günlük trend tahmini başlatılıyor...")
        
        # Geçmiş verileri yükle (tahmin için)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)  # Son 1 yıl
        historical_data = self._load_historical_data((start_date, end_date))
        
        if not historical_data:
            print("⚠️ Tahmin için yeterli geçmiş veri bulunamadı")
            return self._create_empty_result("future_trends")
        
        trends = []
        insights = []
        visualizations = []
        statistics = {}
        
        # Her metrik için tahmin
        for metric in self.metrics:
            forecast = self._forecast_metric(
                historical_data, metric, forecast_days, confidence_level
            )
            trends.extend(forecast["trends"])
            insights.extend(forecast["insights"])
            visualizations.extend(forecast["visualizations"])
            statistics[metric] = forecast["statistics"]
        
        # Grant türleri için tahmin
        for grant_type in self.grant_categories:
            grant_forecast = self._forecast_grant_type(
                historical_data, grant_type, forecast_days, confidence_level
            )
            trends.extend(grant_forecast["trends"])
            insights.extend(grant_forecast["insights"])
        
        # Sonuç oluşturma
        analysis_id = f"future_trends_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        result = TrendAnalysisResult(
            analysis_id=analysis_id,
            analysis_type="future_trends",
            period_start=end_date,
            period_end=end_date + timedelta(days=forecast_days),
            trends=trends,
            insights=insights,
            visualizations=visualizations,
            statistics=statistics,
            created_at=datetime.now()
        )
        
        # Sonucu kaydet
        self._save_analysis_result(result)
        self.analysis_history.append(result)
        
        print(f"✅ Gelecek trend tahmini tamamlandı: {analysis_id}")
        
        return result
    
    def _load_historical_data(self, 
                            time_range: Optional[Tuple[datetime, datetime]] = None,
                            grant_types: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Geçmiş verileri yükle"""
        try:
            data = []
            
            # Batch results'dan veri yükle
            batch_results_path = self.data_path / "batch_results"
            if batch_results_path.exists():
                for file_path in batch_results_path.glob("*.json"):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            batch_data = json.load(f)
                            
                        # Batch sonuçlarını trend verisi formatına dönüştür
                        processed_data = self._process_batch_data(batch_data)
                        data.extend(processed_data)
                        
                    except Exception as e:
                        print(f"⚠️ Dosya okuma hatası {file_path}: {e}")
                        continue
            
            # Memory verilerinden yükle
            memory_path = self.data_path / "memory"
            if memory_path.exists():
                for file_path in memory_path.glob("*.json"):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            memory_data = json.load(f)
                        
                        # Memory verilerini trend verisi formatına dönüştür
                        processed_data = self._process_memory_data(memory_data)
                        data.extend(processed_data)
                        
                    except Exception as e:
                        print(f"⚠️ Memory dosya okuma hatası {file_path}: {e}")
                        continue
            
            # Zaman ve grant türü filtresi uygula
            if time_range:
                data = [d for d in data if time_range[0] <= d["timestamp"] <= time_range[1]]
            
            if grant_types:
                data = [d for d in data if any(gt in str(d.get("grant_types", [])) for gt in grant_types)]
            
            print(f"📊 {len(data)} veri noktası yüklendi")
            return data
            
        except Exception as e:
            print(f"❌ Veri yükleme hatası: {e}")
            return []
    
    def _process_batch_data(self, batch_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Batch verilerini trend analizi için işle"""
        processed = []
        
        try:
            # Batch metadata'sından temel bilgileri al
            batch_id = batch_data.get("batch_id", "unknown")
            created_at = datetime.fromisoformat(batch_data.get("created_at", datetime.now().isoformat()))
            
            # Her query sonucu için veri noktası oluştur
            for query_result in batch_data.get("query_results", []):
                data_point = {
                    "timestamp": created_at,
                    "batch_id": batch_id,
                    "query_id": query_result.get("query_id"),
                    "processing_time": query_result.get("processing_time", 0),
                    "success": query_result.get("success", False),
                    "grant_types": query_result.get("metadata", {}).get("grant_types", []),
                    "response_quality": query_result.get("metadata", {}).get("response_quality", 0.5),
                    "sources_count": len(query_result.get("metadata", {}).get("sources", [])),
                    "type": "batch_query"
                }
                processed.append(data_point)
            
        except Exception as e:
            print(f"⚠️ Batch veri işleme hatası: {e}")
        
        return processed
    
    def _process_memory_data(self, memory_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Memory verilerini trend analizi için işle"""
        processed = []
        
        try:
            # Conversation history'den veri noktaları oluştur
            for entry in memory_data.get("conversation_history", []):
                if entry.get("role") == "assistant":  # Sadece assistant cevapları
                    data_point = {
                        "timestamp": datetime.fromisoformat(entry.get("timestamp")),
                        "entry_id": entry.get("id"),
                        "processing_time": entry.get("context", {}).get("processing_time", 0),
                        "response_quality": entry.get("context", {}).get("response_quality", 0.5),
                        "grant_types": entry.get("context", {}).get("grant_types_mentioned", []),
                        "sources_count": entry.get("context", {}).get("sources_count", 0),
                        "query_complexity": entry.get("context", {}).get("query_complexity", "medium"),
                        "type": "conversation"
                    }
                    processed.append(data_point)
            
        except Exception as e:
            print(f"⚠️ Memory veri işleme hatası: {e}")
        
        return processed
    
    def _analyze_time_series(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Zaman serisi analizi"""
        trends = []
        insights = []
        visualizations = []
        statistics = {}
        
        try:
            # Günlük metrikleri hesapla
            daily_metrics = self._calculate_daily_metrics(data)
            
            if len(daily_metrics) < self.config["min_data_points"]:
                insights.append("Zaman serisi analizi için yeterli veri yok")
                return {"trends": trends, "insights": insights, "visualizations": visualizations, "statistics": statistics}
            
            # Trend eğimlerini hesapla
            for metric in ["query_count", "avg_processing_time", "success_rate", "avg_quality"]:
                if metric in daily_metrics.columns:
                    values = daily_metrics[metric].values
                    days = np.arange(len(values))
                    
                    # Linear regression
                    slope, intercept, r_value, p_value, std_err = stats.linregress(days, values)
                    
                    # Trend yönü belirleme
                    if abs(slope) < 0.001:
                        trend_direction = "stable"
                    elif slope > 0:
                        trend_direction = "increasing"
                    else:
                        trend_direction = "decreasing"
                    
                    # Trend verisi oluştur
                    trend = TrendData(
                        period=f"{daily_metrics.index[0]} - {daily_metrics.index[-1]}",
                        grant_type="ALL",
                        value=slope,
                        metric_type=metric,
                        metadata={
                            "direction": trend_direction,
                            "correlation": r_value,
                            "p_value": p_value,
                            "significance": p_value < self.config["significance_level"]
                        }
                    )
                    trends.append(trend)
                    
                    # İstatistikler
                    statistics[f"{metric}_trend"] = {
                        "slope": slope,
                        "r_squared": r_value**2,
                        "p_value": p_value,
                        "direction": trend_direction
                    }
                    
                    # Insight oluştur
                    if p_value < self.config["significance_level"]:
                        insight = f"{metric.replace('_', ' ').title()} {trend_direction} trend gösteriyor (R²={r_value**2:.3f})"
                        insights.append(insight)
            
            # Zaman serisi görselleştirmesi
            visualization = self._create_time_series_visualization(daily_metrics)
            visualizations.append(visualization)
            
        except Exception as e:
            print(f"⚠️ Zaman serisi analizi hatası: {e}")
            insights.append(f"Zaman serisi analizi hatası: {str(e)}")
        
        return {"trends": trends, "insights": insights, "visualizations": visualizations, "statistics": statistics}
    
    def _analyze_seasonal_patterns(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Mevsimsel patern analizi"""
        trends = []
        insights = []
        visualizations = []
        statistics = {}
        
        try:
            # Günlük verileri hazırla
            df = pd.DataFrame(data)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.set_index('timestamp').sort_index()
            
            # Haftalık paternler
            df['day_of_week'] = df.index.dayofweek
            df['hour'] = df.index.hour
            
            # Günlük paternler analizi
            daily_patterns = df.groupby('day_of_week').agg({
                'processing_time': 'mean',
                'success': 'mean',
                'response_quality': 'mean'
            }).round(3)
            
            # En yoğun günleri bul
            query_counts_by_day = df.groupby('day_of_week').size()
            busiest_day = query_counts_by_day.idxmax()
            day_names = ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi', 'Pazar']
            
            insights.append(f"En yoğun gün: {day_names[busiest_day]} ({query_counts_by_day[busiest_day]} sorgu)")
            
            # Saatlik paternler
            hourly_patterns = df.groupby('hour').agg({
                'processing_time': 'mean',
                'success': 'mean',
                'response_quality': 'mean'
            }).round(3)
            
            # En yoğun saatleri bul
            query_counts_by_hour = df.groupby('hour').size()
            peak_hour = query_counts_by_hour.idxmax()
            
            insights.append(f"En yoğun saat: {peak_hour}:00 ({query_counts_by_hour[peak_hour]} sorgu)")
            
            # Mevsimsel trend verileri
            for day_idx, day_name in enumerate(day_names):
                if day_idx in daily_patterns.index:
                    row = daily_patterns.loc[day_idx]
                    trend = TrendData(
                        period=day_name,
                        grant_type="ALL",
                        value=float(row['success']),
                        metric_type="daily_success_rate",
                        metadata={
                            "avg_processing_time": float(row['processing_time']),
                            "avg_quality": float(row['response_quality']),
                            "query_count": int(query_counts_by_day.get(day_idx, 0))
                        }
                    )
                    trends.append(trend)
            
            # İstatistikler
            statistics["seasonal_patterns"] = {
                "daily_patterns": daily_patterns.to_dict(),
                "hourly_patterns": hourly_patterns.to_dict(),
                "busiest_day": busiest_day,
                "peak_hour": peak_hour
            }
            
            # Görselleştirme
            visualization = self._create_seasonal_visualization(daily_patterns, hourly_patterns)
            visualizations.append(visualization)
            
        except Exception as e:
            print(f"⚠️ Mevsimsel analiz hatası: {e}")
            insights.append(f"Mevsimsel analiz hatası: {str(e)}")
        
        return {"trends": trends, "insights": insights, "visualizations": visualizations, "statistics": statistics}
    
    def _analyze_grant_type_trends(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Grant türü trend analizi"""
        trends = []
        insights = []
        visualizations = []
        statistics = {}
        
        try:
            # Grant türlerini çıkar ve analiz et
            grant_type_data = defaultdict(list)
            
            for item in data:
                grant_types = item.get("grant_types", [])
                if isinstance(grant_types, str):
                    grant_types = [grant_types]
                
                for grant_type in grant_types:
                    grant_type_data[grant_type].append(item)
            
            # Her grant türü için analiz
            for grant_type, type_data in grant_type_data.items():
                if len(type_data) >= 3:  # Minimum veri gereksinimi
                    # Başarı oranı
                    success_rate = sum(1 for d in type_data if d.get("success", False)) / len(type_data)
                    
                    # Ortalama işlem süresi
                    avg_processing_time = np.mean([d.get("processing_time", 0) for d in type_data])
                    
                    # Ortalama kalite
                    avg_quality = np.mean([d.get("response_quality", 0.5) for d in type_data])
                    
                    # Trend verisi oluştur
                    trend = TrendData(
                        period="ALL",
                        grant_type=grant_type,
                        value=success_rate,
                        metric_type="success_rate",
                        metadata={
                            "sample_size": len(type_data),
                            "avg_processing_time": avg_processing_time,
                            "avg_quality": avg_quality
                        }
                    )
                    trends.append(trend)
                    
                    # İstatistikler
                    statistics[grant_type] = {
                        "sample_size": len(type_data),
                        "success_rate": success_rate,
                        "avg_processing_time": avg_processing_time,
                        "avg_quality": avg_quality
                    }
                    
                    # Insight
                    insights.append(f"{grant_type}: %{success_rate*100:.1f} başarı oranı ({len(type_data)} sorgu)")
            
            # En iyi performans gösteren grant türü
            if statistics:
                best_grant_type = max(statistics.keys(), key=lambda x: statistics[x]["success_rate"])
                insights.append(f"En yüksek başarı oranı: {best_grant_type} (%{statistics[best_grant_type]['success_rate']*100:.1f})")
            
            # Görselleştirme
            visualization = self._create_grant_type_visualization(statistics)
            visualizations.append(visualization)
            
        except Exception as e:
            print(f"⚠️ Grant türü analizi hatası: {e}")
            insights.append(f"Grant türü analizi hatası: {str(e)}")
        
        return {"trends": trends, "insights": insights, "visualizations": visualizations, "statistics": statistics}
    
    def _calculate_daily_metrics(self, data: List[Dict[str, Any]]) -> pd.DataFrame:
        """Günlük metrikleri hesapla"""
        try:
            df = pd.DataFrame(data)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df['date'] = df['timestamp'].dt.date
            
            # Günlük agregasyonlar
            daily_metrics = df.groupby('date').agg({
                'query_id': 'count',  # Sorgu sayısı
                'processing_time': 'mean',  # Ortalama işlem süresi
                'success': 'mean',  # Başarı oranı
                'response_quality': 'mean',  # Ortalama kalite
                'sources_count': 'mean'  # Ortalama kaynak sayısı
            }).round(3)
            
            # Kolon isimlerini düzenle
            daily_metrics.columns = ['query_count', 'avg_processing_time', 'success_rate', 'avg_quality', 'avg_sources']
            
            return daily_metrics
            
        except Exception as e:
            print(f"⚠️ Günlük metrik hesaplama hatası: {e}")
            return pd.DataFrame()
    
    def _create_empty_result(self, analysis_type: str) -> TrendAnalysisResult:
        """Boş analiz sonucu oluştur"""
        return TrendAnalysisResult(
            analysis_id=f"empty_{analysis_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            analysis_type=analysis_type,
            period_start=datetime.now(),
            period_end=datetime.now(),
            trends=[],
            insights=["Analiz için yeterli veri bulunamadı"],
            visualizations=[],
            statistics={},
            created_at=datetime.now()
        )
    
    def _save_analysis_result(self, result: TrendAnalysisResult):
        """Analiz sonucunu kaydet"""
        try:
            # Kayıt klasörünü oluştur
            save_path = self.data_path / "analytics"
            save_path.mkdir(exist_ok=True)
            
            # Dosya adı
            filename = f"trend_analysis_{result.analysis_id}.json"
            filepath = save_path / filename
            
            # JSON formatında kaydet
            result_dict = asdict(result)
            # Datetime objelerini string'e çevir
            result_dict['created_at'] = result.created_at.isoformat()
            result_dict['period_start'] = result.period_start.isoformat()
            result_dict['period_end'] = result.period_end.isoformat()
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(result_dict, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Analiz sonucu kaydedildi: {filepath}")
            
        except Exception as e:
            print(f"⚠️ Analiz sonucu kaydetme hatası: {e}")
    
    def get_analysis_history(self, limit: int = 10) -> List[TrendAnalysisResult]:
        """Analiz geçmişini döndür"""
        return self.analysis_history[-limit:]
    
    def get_trend_summary(self) -> Dict[str, Any]:
        """Trend özetini döndür"""
        if not self.analysis_history:
            return {"message": "Henüz analiz yapılmamış"}
        
        latest_analysis = self.analysis_history[-1]
        
        return {
            "latest_analysis_id": latest_analysis.analysis_id,
            "analysis_type": latest_analysis.analysis_type,
            "total_trends": len(latest_analysis.trends),
            "total_insights": len(latest_analysis.insights),
            "key_insights": latest_analysis.insights[:3],
            "analysis_date": latest_analysis.created_at.isoformat()
        }
    
    # Placeholder metodları (visualization ve advanced analysis için)
    def _analyze_momentum(self, data): 
        """Momentum analizi - implement in advanced version"""
        return {"trends": [], "insights": [], "visualizations": [], "statistics": {}}
    
    def _detect_anomalies(self, data): 
        """Anomali tespiti - implement in advanced version"""
        return {"trends": [], "insights": [], "visualizations": [], "statistics": {}}
    
    def _analyze_performance_changes(self, data): 
        """Performans değişimi analizi - implement in advanced version"""
        return {"trends": [], "insights": [], "visualizations": [], "statistics": {}}
    
    def _compare_metric_between_periods(self, data1, data2, metric, period1, period2):
        """Dönemler arası metrik karşılaştırması - implement in advanced version"""
        return {"trends": [], "insights": [], "visualizations": [], "statistics": {}}
    
    def _calculate_overall_comparison_stats(self, data1, data2):
        """Genel karşılaştırma istatistikleri - implement in advanced version"""
        return {"insights": []}
    
    def _forecast_metric(self, data, metric, days, confidence):
        """Metrik tahmini - implement in advanced version"""
        return {"trends": [], "insights": [], "visualizations": [], "statistics": {}}
    
    def _forecast_grant_type(self, data, grant_type, days, confidence):
        """Grant türü tahmini - implement in advanced version"""
        return {"trends": [], "insights": []}
    
    def _create_time_series_visualization(self, daily_metrics):
        """Zaman serisi görselleştirmesi - implement in advanced version"""
        return {"type": "time_series", "data": "placeholder"}
    
    def _create_seasonal_visualization(self, daily_patterns, hourly_patterns):
        """Mevsimsel görselleştirme - implement in advanced version"""
        return {"type": "seasonal", "data": "placeholder"}
    
    def _create_grant_type_visualization(self, statistics):
        """Grant türü görselleştirmesi - implement in advanced version"""
        return {"type": "grant_types", "data": "placeholder"} 