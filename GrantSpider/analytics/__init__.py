"""
PHASE 3.1: Advanced Analytics & Insights
Grant Trend Analysis, Predictive Analytics, Advanced Dashboards

Bu modül, AMIF grant verilerinin gelişmiş analizini sağlar:
- Grant trend analizi
- Başarı tahmini modelleri
- İnteraktif dashboard'lar
- Performans metrikleri
"""

from .trend_analyzer import GrantTrendAnalyzer
from .predictive_model import GrantSuccessPredictorModel
from .dashboard_generator import AdvancedDashboardGenerator
from .metrics_engine import PerformanceMetricsEngine

__all__ = [
    'GrantTrendAnalyzer',
    'GrantSuccessPredictorModel',
    'AdvancedDashboardGenerator',
    'PerformanceMetricsEngine'
]

__version__ = '3.1.0' 