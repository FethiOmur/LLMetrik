"""
Advanced Dashboard Generator
PHASE 3.1: Advanced Analytics & Insights

İnteraktif analitik dashboard'lar oluşturan gelişmiş sistem.
Real-time metrics, interactive charts, comprehensive insights.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import json
from pathlib import Path
import base64
from io import BytesIO

# Visualization libraries
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.offline as pyo
import matplotlib.pyplot as plt
import seaborn as sns

# Dashboard framework
import streamlit as st
from jinja2 import Template

@dataclass
class DashboardWidget:
    """Dashboard widget tanımı"""
    widget_id: str
    widget_type: str  # chart, metric, table, text
    title: str
    data: Dict[str, Any]
    config: Dict[str, Any]
    position: Dict[str, int]  # row, col, width, height
    created_at: datetime

@dataclass
class DashboardLayout:
    """Dashboard layout tanımı"""
    layout_id: str
    layout_name: str
    widgets: List[DashboardWidget]
    theme: str
    refresh_interval: int  # seconds
    filters: Dict[str, Any]
    created_at: datetime

@dataclass
class DashboardReport:
    """Dashboard raporu"""
    report_id: str
    layout: DashboardLayout
    generated_html: str
    static_charts: List[str]  # Base64 encoded images
    interactive_charts: List[str]  # HTML strings
    metadata: Dict[str, Any]
    created_at: datetime

class AdvancedDashboardGenerator:
    """
    Gelişmiş dashboard oluşturucu sistem
    
    Bu sınıf, analitik verilerden interaktif ve statik
    dashboard'lar oluşturur.
    """
    
    def __init__(self, data_path: str = "interfaces/data"):
        """
        Dashboard Generator başlatıcısı
        
        Args:
            data_path: Veri dosyalarının bulunduğu yol
        """
        self.data_path = Path(data_path)
        self.dashboards_path = self.data_path / "dashboards"
        self.dashboards_path.mkdir(exist_ok=True)
        
        # Dashboard temaları
        self.themes = {
            "corporate": {
                "primary_color": "#1f77b4",
                "secondary_color": "#ff7f0e", 
                "background_color": "#ffffff",
                "text_color": "#2c3e50",
                "font_family": "Arial, sans-serif"
            },
            "dark": {
                "primary_color": "#00d4aa",
                "secondary_color": "#ff6b6b",
                "background_color": "#2c3e50",
                "text_color": "#ffffff", 
                "font_family": "Roboto, sans-serif"
            },
            "minimal": {
                "primary_color": "#3498db",
                "secondary_color": "#e74c3c",
                "background_color": "#f8f9fa",
                "text_color": "#495057",
                "font_family": "Helvetica, sans-serif"
            }
        }
        
        # Widget türleri
        self.widget_types = {
            "kpi_card": self._create_kpi_card,
            "line_chart": self._create_line_chart,
            "bar_chart": self._create_bar_chart,
            "pie_chart": self._create_pie_chart,
            "heatmap": self._create_heatmap,
            "scatter_plot": self._create_scatter_plot,
            "gauge_chart": self._create_gauge_chart,
            "data_table": self._create_data_table,
            "metric_comparison": self._create_metric_comparison,
            "trend_indicator": self._create_trend_indicator
        }
        
        # Dashboard geçmişi
        self.dashboard_history = []
        
        print("📊 AdvancedDashboardGenerator başlatıldı")
    
    def create_executive_dashboard(self, 
                                 time_range: Optional[tuple] = None,
                                 theme: str = "corporate") -> DashboardReport:
        """
        Yönetici özet dashboard'u oluştur
        
        Args:
            time_range: Zaman aralığı
            theme: Dashboard teması
            
        Returns:
            Dashboard raporu
        """
        print("👔 Executive Dashboard oluşturuluyor...")
        
        # Veri yükleme
        data = self._load_dashboard_data(time_range)
        
        # KPI'ları hesapla
        kpis = self._calculate_executive_kpis(data)
        
        # Widget'ları oluştur
        widgets = []
        
        # 1. Ana KPI kartları (üst satır)
        widgets.extend([
            DashboardWidget(
                widget_id="total_queries",
                widget_type="kpi_card",
                title="Toplam Sorgu",
                data={"value": kpis["total_queries"], "change": kpis["query_change"]},
                config={"color": "primary", "icon": "📊"},
                position={"row": 1, "col": 1, "width": 3, "height": 1},
                created_at=datetime.now()
            ),
            DashboardWidget(
                widget_id="success_rate",
                widget_type="kpi_card", 
                title="Başarı Oranı",
                data={"value": f"{kpis['success_rate']:.1%}", "change": kpis["success_change"]},
                config={"color": "success", "icon": "✅"},
                position={"row": 1, "col": 2, "width": 3, "height": 1},
                created_at=datetime.now()
            ),
            DashboardWidget(
                widget_id="avg_response_time",
                widget_type="kpi_card",
                title="Ort. Yanıt Süresi",
                data={"value": f"{kpis['avg_response_time']:.1f}s", "change": kpis["response_time_change"]},
                config={"color": "info", "icon": "⏱️"},
                position={"row": 1, "col": 3, "width": 3, "height": 1},
                created_at=datetime.now()
            ),
            DashboardWidget(
                widget_id="quality_score",
                widget_type="kpi_card",
                title="Kalite Puanı",
                data={"value": f"{kpis['quality_score']:.2f}", "change": kpis["quality_change"]},
                config={"color": "warning", "icon": "⭐"},
                position={"row": 1, "col": 4, "width": 3, "height": 1},
                created_at=datetime.now()
            )
        ])
        
        # 2. Zaman serisi grafiği (ikinci satır)
        time_series_data = self._prepare_time_series_data(data)
        widgets.append(
            DashboardWidget(
                widget_id="queries_timeline",
                widget_type="line_chart",
                title="Sorgu Trendi (Son 30 Gün)",
                data=time_series_data,
                config={"height": 400, "show_legend": True},
                position={"row": 2, "col": 1, "width": 8, "height": 2},
                created_at=datetime.now()
            )
        )
        
        # 3. Grant türü dağılımı (ikinci satır, sağda)
        grant_distribution = self._prepare_grant_distribution_data(data)
        widgets.append(
            DashboardWidget(
                widget_id="grant_distribution",
                widget_type="pie_chart",
                title="Grant Türü Dağılımı",
                data=grant_distribution,
                config={"height": 400},
                position={"row": 2, "col": 9, "width": 4, "height": 2},
                created_at=datetime.now()
            )
        )
        
        # 4. Performans heatmap (üçüncü satır)
        performance_heatmap = self._prepare_performance_heatmap_data(data)
        widgets.append(
            DashboardWidget(
                widget_id="performance_heatmap",
                widget_type="heatmap",
                title="Günlük/Saatlik Performans",
                data=performance_heatmap,
                config={"height": 300},
                position={"row": 3, "col": 1, "width": 6, "height": 2},
                created_at=datetime.now()
            )
        )
        
        # 5. Top grant türleri tablosu (üçüncü satır, sağda)
        top_grants_table = self._prepare_top_grants_table(data)
        widgets.append(
            DashboardWidget(
                widget_id="top_grants_table",
                widget_type="data_table",
                title="En Popüler Grant Türleri",
                data=top_grants_table,
                config={"height": 300, "sortable": True},
                position={"row": 3, "col": 7, "width": 6, "height": 2},
                created_at=datetime.now()
            )
        )
        
        # Layout oluştur
        layout = DashboardLayout(
            layout_id=f"executive_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            layout_name="Executive Dashboard",
            widgets=widgets,
            theme=theme,
            refresh_interval=300,  # 5 dakika
            filters={},
            created_at=datetime.now()
        )
        
        # Dashboard'u oluştur
        dashboard_report = self._generate_dashboard_report(layout)
        
        # Kaydet
        self._save_dashboard_report(dashboard_report)
        self.dashboard_history.append(dashboard_report)
        
        print(f"✅ Executive Dashboard oluşturuldu: {dashboard_report.report_id}")
        return dashboard_report
    
    def create_operational_dashboard(self,
                                   time_range: Optional[tuple] = None,
                                   theme: str = "dark") -> DashboardReport:
        """
        Operasyonel dashboard oluştur
        
        Args:
            time_range: Zaman aralığı
            theme: Dashboard teması
            
        Returns:
            Dashboard raporu
        """
        print("🔧 Operational Dashboard oluşturuluyor...")
        
        # Veri yükleme
        data = self._load_dashboard_data(time_range)
        
        # Operasyonel metrikleri hesapla
        ops_metrics = self._calculate_operational_metrics(data)
        
        widgets = []
        
        # 1. Sistem durumu indikatörleri
        widgets.extend([
            DashboardWidget(
                widget_id="system_health",
                widget_type="gauge_chart",
                title="Sistem Sağlığı",
                data={"value": ops_metrics["system_health"], "max": 100},
                config={"color_ranges": [(0, 50, "red"), (50, 80, "yellow"), (80, 100, "green")]},
                position={"row": 1, "col": 1, "width": 4, "height": 1},
                created_at=datetime.now()
            ),
            DashboardWidget(
                widget_id="response_time_gauge",
                widget_type="gauge_chart",
                title="Yanıt Süresi",
                data={"value": ops_metrics["avg_response_time"], "max": 60},
                config={"color_ranges": [(0, 10, "green"), (10, 30, "yellow"), (30, 60, "red")]},
                position={"row": 1, "col": 2, "width": 4, "height": 1},
                created_at=datetime.now()
            ),
            DashboardWidget(
                widget_id="error_rate_gauge",
                widget_type="gauge_chart",
                title="Hata Oranı",
                data={"value": ops_metrics["error_rate"], "max": 100},
                config={"color_ranges": [(0, 5, "green"), (5, 15, "yellow"), (15, 100, "red")]},
                position={"row": 1, "col": 3, "width": 4, "height": 1},
                created_at=datetime.now()
            )
        ])
        
        # 2. Gerçek zamanlı metrikler
        realtime_data = self._prepare_realtime_metrics_data(data)
        widgets.append(
            DashboardWidget(
                widget_id="realtime_metrics",
                widget_type="line_chart",
                title="Gerçek Zamanlı Metrikler (Son 24 Saat)",
                data=realtime_data,
                config={"height": 400, "refresh_interval": 30},
                position={"row": 2, "col": 1, "width": 12, "height": 2},
                created_at=datetime.now()
            )
        )
        
        # 3. Hata analizi
        error_analysis = self._prepare_error_analysis_data(data)
        widgets.append(
            DashboardWidget(
                widget_id="error_analysis",
                widget_type="bar_chart",
                title="Hata Türü Analizi",
                data=error_analysis,
                config={"height": 300, "orientation": "horizontal"},
                position={"row": 3, "col": 1, "width": 6, "height": 2},
                created_at=datetime.now()
            )
        )
        
        # 4. Performans dağılımı
        performance_dist = self._prepare_performance_distribution_data(data)
        widgets.append(
            DashboardWidget(
                widget_id="performance_distribution",
                widget_type="scatter_plot",
                title="Performans Dağılımı",
                data=performance_dist,
                config={"height": 300},
                position={"row": 3, "col": 7, "width": 6, "height": 2},
                created_at=datetime.now()
            )
        )
        
        # 5. Aktif işlemler tablosu
        active_jobs = self._prepare_active_jobs_table(data)
        widgets.append(
            DashboardWidget(
                widget_id="active_jobs",
                widget_type="data_table",
                title="Aktif İşlemler",
                data=active_jobs,
                config={"height": 250, "realtime": True},
                position={"row": 4, "col": 1, "width": 12, "height": 1},
                created_at=datetime.now()
            )
        )
        
        # Layout oluştur
        layout = DashboardLayout(
            layout_id=f"operational_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            layout_name="Operational Dashboard",
            widgets=widgets,
            theme=theme,
            refresh_interval=30,  # 30 saniye
            filters={"show_errors": True, "show_warnings": True},
            created_at=datetime.now()
        )
        
        # Dashboard'u oluştur
        dashboard_report = self._generate_dashboard_report(layout)
        
        # Kaydet
        self._save_dashboard_report(dashboard_report)
        self.dashboard_history.append(dashboard_report)
        
        print(f"✅ Operational Dashboard oluşturuldu: {dashboard_report.report_id}")
        return dashboard_report
    
    def create_analytical_dashboard(self,
                                  time_range: Optional[tuple] = None,
                                  theme: str = "minimal") -> DashboardReport:
        """
        Detaylı analitik dashboard oluştur
        
        Args:
            time_range: Zaman aralığı
            theme: Dashboard teması
            
        Returns:
            Dashboard raporu
        """
        print("📈 Analytical Dashboard oluşturuluyor...")
        
        # Veri yükleme
        data = self._load_dashboard_data(time_range)
        
        # Analitik metrikleri hesapla
        analytics = self._calculate_analytical_metrics(data)
        
        widgets = []
        
        # 1. Trend analiz kartları
        widgets.extend([
            DashboardWidget(
                widget_id="trend_analysis",
                widget_type="metric_comparison",
                title="Trend Analizi",
                data=analytics["trends"],
                config={"show_arrows": True, "comparison_period": "last_month"},
                position={"row": 1, "col": 1, "width": 12, "height": 1},
                created_at=datetime.now()
            )
        ])
        
        # 2. Korelasyon analizi
        correlation_data = self._prepare_correlation_analysis(data)
        widgets.append(
            DashboardWidget(
                widget_id="correlation_matrix",
                widget_type="heatmap",
                title="Metrik Korelasyon Matrisi",
                data=correlation_data,
                config={"height": 400, "color_scale": "RdBu"},
                position={"row": 2, "col": 1, "width": 6, "height": 2},
                created_at=datetime.now()
            )
        )
        
        # 3. Grant türü performans karşılaştırması
        grant_performance = self._prepare_grant_performance_comparison(data)
        widgets.append(
            DashboardWidget(
                widget_id="grant_performance_comparison",
                widget_type="bar_chart",
                title="Grant Türü Performans Karşılaştırması",
                data=grant_performance,
                config={"height": 400, "grouped": True},
                position={"row": 2, "col": 7, "width": 6, "height": 2},
                created_at=datetime.now()
            )
        )
        
        # 4. Zaman bazlı analiz
        temporal_analysis = self._prepare_temporal_analysis(data)
        widgets.append(
            DashboardWidget(
                widget_id="temporal_analysis",
                widget_type="line_chart",
                title="Zaman Bazlı Performans Analizi",
                data=temporal_analysis,
                config={"height": 350, "multi_axis": True},
                position={"row": 3, "col": 1, "width": 8, "height": 2},
                created_at=datetime.now()
            )
        )
        
        # 5. İstatistiksel özet
        statistical_summary = self._prepare_statistical_summary(data)
        widgets.append(
            DashboardWidget(
                widget_id="statistical_summary",
                widget_type="data_table",
                title="İstatistiksel Özet",
                data=statistical_summary,
                config={"height": 350, "precision": 3},
                position={"row": 3, "col": 9, "width": 4, "height": 2},
                created_at=datetime.now()
            )
        )
        
        # 6. Anomali tespiti
        anomaly_data = self._prepare_anomaly_detection(data)
        if anomaly_data["anomalies"]:
            widgets.append(
                DashboardWidget(
                    widget_id="anomaly_detection",
                    widget_type="scatter_plot",
                    title="Anomali Tespiti",
                    data=anomaly_data,
                    config={"height": 300, "highlight_anomalies": True},
                    position={"row": 4, "col": 1, "width": 12, "height": 2},
                    created_at=datetime.now()
                )
            )
        
        # Layout oluştur
        layout = DashboardLayout(
            layout_id=f"analytical_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            layout_name="Analytical Dashboard",
            widgets=widgets,
            theme=theme,
            refresh_interval=600,  # 10 dakika
            filters={
                "time_aggregation": "daily",
                "show_trends": True,
                "show_correlations": True
            },
            created_at=datetime.now()
        )
        
        # Dashboard'u oluştur
        dashboard_report = self._generate_dashboard_report(layout)
        
        # Kaydet
        self._save_dashboard_report(dashboard_report)
        self.dashboard_history.append(dashboard_report)
        
        print(f"✅ Analytical Dashboard oluşturuldu: {dashboard_report.report_id}")
        return dashboard_report
    
    def create_custom_dashboard(self,
                              widget_configs: List[Dict[str, Any]],
                              layout_name: str = "Custom Dashboard",
                              theme: str = "corporate") -> DashboardReport:
        """
        Özel dashboard oluştur
        
        Args:
            widget_configs: Widget konfigürasyonları
            layout_name: Dashboard adı
            theme: Tema
            
        Returns:
            Dashboard raporu
        """
        print(f"🎨 Custom Dashboard oluşturuluyor: {layout_name}")
        
        # Veri yükleme
        data = self._load_dashboard_data()
        
        widgets = []
        
        # Her widget için konfigürasyonu işle
        for i, config in enumerate(widget_configs):
            try:
                widget_data = self._prepare_widget_data(data, config)
                
                widget = DashboardWidget(
                    widget_id=config.get("widget_id", f"custom_widget_{i}"),
                    widget_type=config["widget_type"],
                    title=config["title"],
                    data=widget_data,
                    config=config.get("config", {}),
                    position=config.get("position", {"row": i+1, "col": 1, "width": 6, "height": 1}),
                    created_at=datetime.now()
                )
                widgets.append(widget)
                
            except Exception as e:
                print(f"⚠️ Widget oluşturma hatası: {e}")
                continue
        
        # Layout oluştur
        layout = DashboardLayout(
            layout_id=f"custom_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            layout_name=layout_name,
            widgets=widgets,
            theme=theme,
            refresh_interval=300,
            filters={},
            created_at=datetime.now()
        )
        
        # Dashboard'u oluştur
        dashboard_report = self._generate_dashboard_report(layout)
        
        # Kaydet
        self._save_dashboard_report(dashboard_report)
        self.dashboard_history.append(dashboard_report)
        
        print(f"✅ Custom Dashboard oluşturuldu: {dashboard_report.report_id}")
        return dashboard_report
    
    def export_dashboard_to_html(self, dashboard_report: DashboardReport) -> str:
        """
        Dashboard'u HTML olarak export et
        
        Args:
            dashboard_report: Dashboard raporu
            
        Returns:
            HTML dosya yolu
        """
        try:
            export_path = self.dashboards_path / "exports"
            export_path.mkdir(exist_ok=True)
            
            filename = f"dashboard_{dashboard_report.report_id}.html"
            filepath = export_path / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(dashboard_report.generated_html)
            
            print(f"📤 Dashboard HTML olarak export edildi: {filepath}")
            return str(filepath)
            
        except Exception as e:
            print(f"❌ HTML export hatası: {e}")
            return ""
    
    def export_dashboard_to_pdf(self, dashboard_report: DashboardReport) -> str:
        """
        Dashboard'u PDF olarak export et
        
        Args:
            dashboard_report: Dashboard raporu
            
        Returns:
            PDF dosya yolu
        """
        try:
            # Bu özellik için additional dependencies gerekli
            # import pdfkit veya weasyprint kullanılabilir
            print("📄 PDF export özelliği geliştirilecek")
            return ""
            
        except Exception as e:
            print(f"❌ PDF export hatası: {e}")
            return ""
    
    def get_dashboard_history(self, limit: int = 10) -> List[DashboardReport]:
        """Dashboard geçmişini döndür"""
        return self.dashboard_history[-limit:]
    
    def get_dashboard_summary(self) -> Dict[str, Any]:
        """Dashboard özetini döndür"""
        if not self.dashboard_history:
            return {"message": "Henüz dashboard oluşturulmamış"}
        
        latest_dashboard = self.dashboard_history[-1]
        
        return {
            "latest_dashboard_id": latest_dashboard.report_id,
            "layout_name": latest_dashboard.layout.layout_name,
            "widget_count": len(latest_dashboard.layout.widgets),
            "theme": latest_dashboard.layout.theme,
            "created_at": latest_dashboard.created_at.isoformat(),
            "total_dashboards": len(self.dashboard_history)
        }
    
    # Private metodları (veri hazırlama ve işleme)
    def _load_dashboard_data(self, time_range: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """Dashboard verilerini yükle"""
        try:
            data = []
            
            # Batch results'dan yükle
            batch_results_path = self.data_path / "batch_results"
            if batch_results_path.exists():
                for file_path in batch_results_path.glob("*.json"):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            batch_data = json.load(f)
                        data.extend(self._process_batch_data_for_dashboard(batch_data))
                    except Exception as e:
                        continue
            
            # Memory verilerinden yükle
            memory_path = self.data_path / "memory"
            if memory_path.exists():
                for file_path in memory_path.glob("*.json"):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            memory_data = json.load(f)
                        data.extend(self._process_memory_data_for_dashboard(memory_data))
                    except Exception as e:
                        continue
            
            # Zaman filtresi uygula
            if time_range:
                start_time, end_time = time_range
                data = [d for d in data if start_time <= d["timestamp"] <= end_time]
            
            print(f"📊 Dashboard için {len(data)} veri noktası yüklendi")
            return data
            
        except Exception as e:
            print(f"❌ Dashboard veri yükleme hatası: {e}")
            return []
    
    def _generate_dashboard_report(self, layout: DashboardLayout) -> DashboardReport:
        """Dashboard raporu oluştur"""
        report_id = f"dashboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # HTML oluştur
        html_content = self._generate_html_dashboard(layout)
        
        # Statik grafikler oluştur
        static_charts = []
        interactive_charts = []
        
        for widget in layout.widgets:
            try:
                if widget.widget_type in ["line_chart", "bar_chart", "pie_chart", "heatmap"]:
                    # İnteraktif grafik oluştur
                    interactive_chart = self._create_interactive_chart(widget)
                    interactive_charts.append(interactive_chart)
                    
                    # Statik grafik oluştur
                    static_chart = self._create_static_chart(widget)
                    static_charts.append(static_chart)
                    
            except Exception as e:
                print(f"⚠️ Widget grafik oluşturma hatası: {e}")
                continue
        
        return DashboardReport(
            report_id=report_id,
            layout=layout,
            generated_html=html_content,
            static_charts=static_charts,
            interactive_charts=interactive_charts,
            metadata={
                "widget_count": len(layout.widgets),
                "theme": layout.theme,
                "generation_time": datetime.now().isoformat()
            },
            created_at=datetime.now()
        )
    
    def _generate_html_dashboard(self, layout: DashboardLayout) -> str:
        """HTML dashboard oluştur"""
        try:
            # HTML template
            html_template = Template("""
            <!DOCTYPE html>
            <html lang="tr">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>{{ layout_name }}</title>
                <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
                <style>
                    body {
                        background-color: {{ theme.background_color }};
                        color: {{ theme.text_color }};
                        font-family: {{ theme.font_family }};
                    }
                    .dashboard-container {
                        padding: 20px;
                    }
                    .widget-container {
                        margin-bottom: 20px;
                        padding: 15px;
                        border-radius: 8px;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        background-color: white;
                    }
                    .kpi-card {
                        text-align: center;
                        padding: 20px;
                    }
                    .kpi-value {
                        font-size: 2rem;
                        font-weight: bold;
                        color: {{ theme.primary_color }};
                    }
                    .kpi-change {
                        font-size: 0.9rem;
                        margin-top: 5px;
                    }
                    .chart-container {
                        height: 400px;
                    }
                </style>
            </head>
            <body>
                <div class="dashboard-container">
                    <h1 class="mb-4">{{ layout_name }}</h1>
                    <div class="row">
                        {% for widget in widgets %}
                        <div class="col-md-{{ widget.position.width }}">
                            <div class="widget-container">
                                <h5>{{ widget.title }}</h5>
                                <div id="widget_{{ widget.widget_id }}">
                                    <!-- Widget content will be inserted here -->
                                </div>
                            </div>
                        </div>
                        {% endfor %}
                    </div>
                </div>
                
                <script>
                    // Dashboard refresh logic
                    setInterval(function() {
                        // Refresh logic here
                    }, {{ refresh_interval * 1000 }});
                </script>
            </body>
            </html>
            """)
            
            # Template'i render et
            theme = self.themes.get(layout.theme, self.themes["corporate"])
            
            html_content = html_template.render(
                layout_name=layout.layout_name,
                widgets=layout.widgets,
                theme=theme,
                refresh_interval=layout.refresh_interval
            )
            
            return html_content
            
        except Exception as e:
            print(f"❌ HTML oluşturma hatası: {e}")
            return "<html><body><h1>Dashboard oluşturma hatası</h1></body></html>"
    
    def _save_dashboard_report(self, dashboard_report: DashboardReport):
        """Dashboard raporunu kaydet"""
        try:
            # JSON formatında kaydet
            report_file = self.dashboards_path / f"dashboard_{dashboard_report.report_id}.json"
            
            # Serialize 
            report_dict = asdict(dashboard_report)
            report_dict['created_at'] = dashboard_report.created_at.isoformat()
            report_dict['layout']['created_at'] = dashboard_report.layout.created_at.isoformat()
            
            for widget in report_dict['layout']['widgets']:
                widget['created_at'] = widget['created_at'] if isinstance(widget['created_at'], str) else widget['created_at'].isoformat()
            
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report_dict, f, indent=2, ensure_ascii=False)
            
            # HTML dosyasını da kaydet
            html_file = self.dashboards_path / f"dashboard_{dashboard_report.report_id}.html"
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(dashboard_report.generated_html)
            
            print(f"💾 Dashboard kaydedildi: {report_file}")
            
        except Exception as e:
            print(f"⚠️ Dashboard kaydetme hatası: {e}")
    
    # Placeholder metodları (widget ve veri işleme)
    def _calculate_executive_kpis(self, data): 
        """Executive KPI hesaplama - placeholder"""
        return {
            "total_queries": len(data),
            "query_change": "+15%",
            "success_rate": 0.85,
            "success_change": "+5%", 
            "avg_response_time": 12.5,
            "response_time_change": "-8%",
            "quality_score": 4.2,
            "quality_change": "+12%"
        }
    
    def _calculate_operational_metrics(self, data):
        """Operasyonel metrik hesaplama - placeholder"""
        return {
            "system_health": 92,
            "avg_response_time": 12.5,
            "error_rate": 3.2
        }
    
    def _calculate_analytical_metrics(self, data):
        """Analitik metrik hesaplama - placeholder"""
        return {
            "trends": {"queries": "+15%", "success": "+5%", "quality": "+12%"}
        }
    
    # Widget creation metodları (placeholder)
    def _create_kpi_card(self, widget): return {"type": "kpi", "data": "placeholder"}
    def _create_line_chart(self, widget): return {"type": "line", "data": "placeholder"}
    def _create_bar_chart(self, widget): return {"type": "bar", "data": "placeholder"}
    def _create_pie_chart(self, widget): return {"type": "pie", "data": "placeholder"}
    def _create_heatmap(self, widget): return {"type": "heatmap", "data": "placeholder"}
    def _create_scatter_plot(self, widget): return {"type": "scatter", "data": "placeholder"}
    def _create_gauge_chart(self, widget): return {"type": "gauge", "data": "placeholder"}
    def _create_data_table(self, widget): return {"type": "table", "data": "placeholder"}
    def _create_metric_comparison(self, widget): return {"type": "comparison", "data": "placeholder"}
    def _create_trend_indicator(self, widget): return {"type": "trend", "data": "placeholder"}
    
    # Veri hazırlama metodları (placeholder)
    def _prepare_time_series_data(self, data): return {"x": [], "y": []}
    def _prepare_grant_distribution_data(self, data): return {"labels": [], "values": []}
    def _prepare_performance_heatmap_data(self, data): return {"matrix": []}
    def _prepare_top_grants_table(self, data): return {"columns": [], "rows": []}
    def _prepare_realtime_metrics_data(self, data): return {"x": [], "y": []}
    def _prepare_error_analysis_data(self, data): return {"categories": [], "counts": []}
    def _prepare_performance_distribution_data(self, data): return {"x": [], "y": []}
    def _prepare_active_jobs_table(self, data): return {"columns": [], "rows": []}
    def _prepare_correlation_analysis(self, data): return {"matrix": []}
    def _prepare_grant_performance_comparison(self, data): return {"categories": [], "values": []}
    def _prepare_temporal_analysis(self, data): return {"x": [], "y": []}
    def _prepare_statistical_summary(self, data): return {"columns": [], "rows": []}
    def _prepare_anomaly_detection(self, data): return {"anomalies": []}
    def _prepare_widget_data(self, data, config): return {"data": "placeholder"}
    
    def _process_batch_data_for_dashboard(self, batch_data): return []
    def _process_memory_data_for_dashboard(self, memory_data): return []
    def _create_interactive_chart(self, widget): return "interactive_chart_html"
    def _create_static_chart(self, widget): return "base64_encoded_image" 