"""
Advanced Report Generator
Gelişmiş rapor üretimi, analitik ve görselleştirme sistemi
"""

from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import json
import csv
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
from collections import defaultdict, Counter
import seaborn as sns

from workflows.batch_processor import BatchAnalysisResult, QueryResult

@dataclass
class AnalyticsReport:
    """Analytics raporu veri sınıfı"""
    report_id: str
    title: str
    description: str
    generated_at: datetime
    data_period: Dict[str, datetime]  # start_date, end_date
    summary: Dict[str, Any]
    sections: List[Dict[str, Any]] = field(default_factory=list)
    visualizations: List[str] = field(default_factory=list)  # file paths
    export_formats: List[str] = field(default_factory=list)  # json, csv, pdf
    
    def to_dict(self) -> Dict[str, Any]:
        """Dictionary'ye dönüştür"""
        return {
            "report_id": self.report_id,
            "title": self.title,
            "description": self.description,
            "generated_at": self.generated_at.isoformat(),
            "data_period": {k: v.isoformat() for k, v in self.data_period.items()},
            "summary": self.summary,
            "sections": self.sections,
            "visualizations": self.visualizations,
            "export_formats": self.export_formats
        }

class ReportGenerator:
    """Gelişmiş rapor üretici sınıfı"""
    
    def __init__(self, output_dir: str = "interfaces/data/reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Görselleştirme ayarları
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
        print("📊 ReportGenerator başlatılıyor...")
    
    def generate_comprehensive_analytics_report(self, 
                                              batch_results: List[BatchAnalysisResult],
                                              time_period: Optional[Tuple[datetime, datetime]] = None) -> AnalyticsReport:
        """
        Kapsamlı analitik rapor üret
        
        Args:
            batch_results: Batch analiz sonuçları
            time_period: Analiz edilecek zaman aralığı
            
        Returns:
            Analitik rapor
        """
        report_id = f"analytics_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Zaman aralığını belirle
        if time_period:
            start_date, end_date = time_period
            filtered_results = [r for r in batch_results 
                              if start_date <= (r.started_at or datetime.now()) <= end_date]
        else:
            filtered_results = batch_results
            start_date = min((r.started_at or datetime.now()) for r in filtered_results) if filtered_results else datetime.now()
            end_date = max((r.completed_at or datetime.now()) for r in filtered_results) if filtered_results else datetime.now()
        
        print(f"📈 Analitik rapor oluşturuluyor: {len(filtered_results)} batch sonucu analiz ediliyor")
        
        # Ana analiz
        summary = self._generate_summary_analytics(filtered_results)
        
        # Rapor bölümleri
        sections = []
        visualizations = []
        
        # 1. Genel performans analizi
        performance_section, perf_charts = self._generate_performance_section(filtered_results, report_id)
        sections.append(performance_section)
        visualizations.extend(perf_charts)
        
        # 2. Grant analizi
        grant_section, grant_charts = self._generate_grant_analysis_section(filtered_results, report_id)
        sections.append(grant_section)
        visualizations.extend(grant_charts)
        
        # 3. Sorgu analizi
        query_section, query_charts = self._generate_query_analysis_section(filtered_results, report_id)
        sections.append(query_section)
        visualizations.extend(query_charts)
        
        # 4. Trend analizi
        trend_section, trend_charts = self._generate_trend_analysis_section(filtered_results, report_id)
        sections.append(trend_section)
        visualizations.extend(trend_charts)
        
        # Rapor nesnesi oluştur
        report = AnalyticsReport(
            report_id=report_id,
            title="AMIF Grant Assistant - Comprehensive Analytics Report",
            description=f"Analysis of {len(filtered_results)} batch operations from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}",
            generated_at=datetime.now(),
            data_period={"start_date": start_date, "end_date": end_date},
            summary=summary,
            sections=sections,
            visualizations=visualizations
        )
        
        # Raporu kaydet
        self._save_report(report)
        
        print(f"✅ Analitik rapor oluşturuldu: {report.report_id}")
        return report
    
    def _generate_summary_analytics(self, batch_results: List[BatchAnalysisResult]) -> Dict[str, Any]:
        """Özet analitikler üret"""
        if not batch_results:
            return {}
        
        # Toplam metrikler
        total_batches = len(batch_results)
        total_queries = sum(r.total_queries for r in batch_results)
        total_successful = sum(r.successful_queries for r in batch_results)
        total_failed = sum(r.failed_queries for r in batch_results)
        
        # Timing analizi
        processing_times = []
        for batch in batch_results:
            if batch.total_processing_time > 0:
                processing_times.append(batch.total_processing_time)
        
        avg_batch_time = sum(processing_times) / len(processing_times) if processing_times else 0
        
        # Query-level timing
        query_times = []
        for batch in batch_results:
            for result in batch.results:
                if result.processing_time > 0:
                    query_times.append(result.processing_time)
        
        avg_query_time = sum(query_times) / len(query_times) if query_times else 0
        
        # Success rate
        success_rate = (total_successful / total_queries) * 100 if total_queries > 0 else 0
        
        # Grant analysis
        grant_types_found = set()
        cross_doc_count = 0
        total_sources = 0
        
        for batch in batch_results:
            for result in batch.results:
                if result.cross_document_analysis and "grant_groups" in result.cross_document_analysis:
                    grant_types_found.update(result.cross_document_analysis["grant_groups"].keys())
                    cross_doc_count += 1
                total_sources += len(result.sources)
        
        return {
            "total_batches": total_batches,
            "total_queries": total_queries,
            "success_rate": round(success_rate, 2),
            "total_successful_queries": total_successful,
            "total_failed_queries": total_failed,
            "average_batch_processing_time": round(avg_batch_time, 2),
            "average_query_processing_time": round(avg_query_time, 2),
            "unique_grant_types_analyzed": len(grant_types_found),
            "grant_types_list": list(grant_types_found),
            "cross_document_analyses_performed": cross_doc_count,
            "total_sources_found": total_sources,
            "average_sources_per_query": round(total_sources / total_queries, 2) if total_queries > 0 else 0
        }
    
    def _generate_performance_section(self, batch_results: List[BatchAnalysisResult], report_id: str) -> Tuple[Dict[str, Any], List[str]]:
        """Performans analizi bölümü"""
        charts = []
        
        # Processing time distribution chart
        processing_times = []
        batch_names = []
        
        for i, batch in enumerate(batch_results):
            if batch.total_processing_time > 0:
                processing_times.append(batch.total_processing_time)
                batch_names.append(f"Batch {i+1}")
        
        if processing_times:
            # Processing time chart
            plt.figure(figsize=(12, 6))
            plt.bar(batch_names, processing_times, color='skyblue', alpha=0.7)
            plt.title('Batch Processing Times', fontsize=14, fontweight='bold')
            plt.xlabel('Batch')
            plt.ylabel('Processing Time (seconds)')
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            chart_path = self.output_dir / f"{report_id}_processing_times.png"
            plt.savefig(chart_path, dpi=300, bbox_inches='tight')
            plt.close()
            charts.append(str(chart_path))
        
        # Success rate chart
        success_rates = []
        for batch in batch_results:
            if batch.total_queries > 0:
                rate = (batch.successful_queries / batch.total_queries) * 100
                success_rates.append(rate)
        
        if success_rates:
            plt.figure(figsize=(10, 6))
            plt.hist(success_rates, bins=10, color='lightgreen', alpha=0.7, edgecolor='black')
            plt.title('Success Rate Distribution', fontsize=14, fontweight='bold')
            plt.xlabel('Success Rate (%)')
            plt.ylabel('Number of Batches')
            plt.axvline(sum(success_rates)/len(success_rates), color='red', linestyle='--', label=f'Average: {sum(success_rates)/len(success_rates):.1f}%')
            plt.legend()
            plt.tight_layout()
            
            chart_path = self.output_dir / f"{report_id}_success_rates.png"
            plt.savefig(chart_path, dpi=300, bbox_inches='tight')
            plt.close()
            charts.append(str(chart_path))
        
        # Performance section data
        section_data = {
            "title": "Performance Analysis",
            "description": "Analysis of system performance metrics",
            "metrics": {
                "average_success_rate": round(sum(success_rates) / len(success_rates), 2) if success_rates else 0,
                "average_processing_time": round(sum(processing_times) / len(processing_times), 2) if processing_times else 0,
                "fastest_batch": min(processing_times) if processing_times else 0,
                "slowest_batch": max(processing_times) if processing_times else 0,
                "performance_consistency": round(1 - (max(processing_times) - min(processing_times)) / max(processing_times), 2) if processing_times else 0
            }
        }
        
        return section_data, charts
    
    def _generate_grant_analysis_section(self, batch_results: List[BatchAnalysisResult], report_id: str) -> Tuple[Dict[str, Any], List[str]]:
        """Grant analizi bölümü"""
        charts = []
        
        # Grant type frequency analysis
        grant_type_counts = Counter()
        cross_doc_counts = Counter()
        
        for batch in batch_results:
            for result in batch.results:
                cross_doc = result.cross_document_analysis
                if cross_doc and "grant_groups" in cross_doc:
                    for grant_type, count in cross_doc["grant_groups"].items():
                        grant_type_counts[grant_type] += count
                        if count > 1:  # Cross-document analysis yapıldı
                            cross_doc_counts[grant_type] += 1
        
        # Grant type distribution chart
        if grant_type_counts:
            plt.figure(figsize=(12, 8))
            grant_types = list(grant_type_counts.keys())
            counts = list(grant_type_counts.values())
            
            # Grant type names'i kısalt
            short_names = [gt.split('-')[-1] if len(gt) > 20 else gt for gt in grant_types]
            
            plt.pie(counts, labels=short_names, autopct='%1.1f%%', startangle=90)
            plt.title('Grant Types Distribution', fontsize=14, fontweight='bold')
            plt.axis('equal')
            
            chart_path = self.output_dir / f"{report_id}_grant_distribution.png"
            plt.savefig(chart_path, dpi=300, bbox_inches='tight')
            plt.close()
            charts.append(str(chart_path))
            
            # Cross-document analysis chart
            if cross_doc_counts:
                plt.figure(figsize=(10, 6))
                cd_types = list(cross_doc_counts.keys())
                cd_counts = list(cross_doc_counts.values())
                
                cd_short_names = [gt.split('-')[-1] if len(gt) > 20 else gt for gt in cd_types]
                
                plt.bar(cd_short_names, cd_counts, color='orange', alpha=0.7)
                plt.title('Cross-Document Analysis by Grant Type', fontsize=14, fontweight='bold')
                plt.xlabel('Grant Type')
                plt.ylabel('Cross-Document Analyses')
                plt.xticks(rotation=45)
                plt.tight_layout()
                
                chart_path = self.output_dir / f"{report_id}_cross_document_analysis.png"
                plt.savefig(chart_path, dpi=300, bbox_inches='tight')
                plt.close()
                charts.append(str(chart_path))
        
        # Grant analysis section
        section_data = {
            "title": "Grant Analysis",
            "description": "Analysis of grant types and cross-document relationships",
            "metrics": {
                "total_grant_types_found": len(grant_type_counts),
                "most_analyzed_grant_type": max(grant_type_counts, key=grant_type_counts.get) if grant_type_counts else "N/A",
                "cross_document_analyses": sum(cross_doc_counts.values()),
                "grant_type_distribution": dict(grant_type_counts)
            }
        }
        
        return section_data, charts
    
    def _generate_query_analysis_section(self, batch_results: List[BatchAnalysisResult], report_id: str) -> Tuple[Dict[str, Any], List[str]]:
        """Sorgu analizi bölümü"""
        charts = []
        
        # Query complexity analysis
        complexity_counts = Counter()
        language_counts = Counter()
        response_lengths = []
        
        for batch in batch_results:
            for result in batch.results:
                # Query complexity
                word_count = len(result.query.split())
                if word_count < 5:
                    complexity = "Simple"
                elif word_count < 15:
                    complexity = "Medium"
                else:
                    complexity = "Complex"
                complexity_counts[complexity] += 1
                
                # Language
                lang = result.metadata.get("detected_language", "unknown")
                language_counts[lang] += 1
                
                # Response length
                if result.response:
                    response_lengths.append(len(result.response))
        
        # Query complexity chart
        if complexity_counts:
            plt.figure(figsize=(8, 6))
            complexities = list(complexity_counts.keys())
            counts = list(complexity_counts.values())
            colors = ['lightgreen', 'yellow', 'orange']
            
            plt.bar(complexities, counts, color=colors[:len(complexities)], alpha=0.7)
            plt.title('Query Complexity Distribution', fontsize=14, fontweight='bold')
            plt.xlabel('Complexity Level')
            plt.ylabel('Number of Queries')
            
            chart_path = self.output_dir / f"{report_id}_query_complexity.png"
            plt.savefig(chart_path, dpi=300, bbox_inches='tight')
            plt.close()
            charts.append(str(chart_path))
        
        # Language distribution
        if language_counts:
            plt.figure(figsize=(8, 6))
            languages = list(language_counts.keys())
            counts = list(language_counts.values())
            
            plt.pie(counts, labels=languages, autopct='%1.1f%%', startangle=90)
            plt.title('Query Language Distribution', fontsize=14, fontweight='bold')
            plt.axis('equal')
            
            chart_path = self.output_dir / f"{report_id}_language_distribution.png"
            plt.savefig(chart_path, dpi=300, bbox_inches='tight')
            plt.close()
            charts.append(str(chart_path))
        
        # Query analysis section
        section_data = {
            "title": "Query Analysis", 
            "description": "Analysis of user queries and response patterns",
            "metrics": {
                "total_queries": sum(complexity_counts.values()),
                "average_response_length": round(sum(response_lengths) / len(response_lengths), 2) if response_lengths else 0,
                "complexity_distribution": dict(complexity_counts),
                "language_distribution": dict(language_counts),
                "longest_response": max(response_lengths) if response_lengths else 0,
                "shortest_response": min(response_lengths) if response_lengths else 0
            }
        }
        
        return section_data, charts
    
    def _generate_trend_analysis_section(self, batch_results: List[BatchAnalysisResult], report_id: str) -> Tuple[Dict[str, Any], List[str]]:
        """Trend analizi bölümü"""
        charts = []
        
        # Time-based analysis
        if batch_results:
            # Sort by time
            sorted_batches = sorted(batch_results, key=lambda x: x.started_at or datetime.now())
            
            # Extract time series data
            timestamps = []
            success_rates = []
            processing_times = []
            query_counts = []
            
            for batch in sorted_batches:
                if batch.started_at:
                    timestamps.append(batch.started_at)
                    if batch.total_queries > 0:
                        success_rates.append((batch.successful_queries / batch.total_queries) * 100)
                    else:
                        success_rates.append(0)
                    processing_times.append(batch.total_processing_time)
                    query_counts.append(batch.total_queries)
            
            if len(timestamps) > 1:
                # Trend charts
                fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
                
                # Success rate trend
                ax1.plot(timestamps, success_rates, marker='o', linewidth=2, markersize=6)
                ax1.set_title('Success Rate Trend', fontweight='bold')
                ax1.set_ylabel('Success Rate (%)')
                ax1.grid(True, alpha=0.3)
                
                # Processing time trend
                ax2.plot(timestamps, processing_times, marker='s', color='orange', linewidth=2, markersize=6)
                ax2.set_title('Processing Time Trend', fontweight='bold')
                ax2.set_ylabel('Processing Time (seconds)')
                ax2.grid(True, alpha=0.3)
                
                # Query count trend
                ax3.plot(timestamps, query_counts, marker='^', color='green', linewidth=2, markersize=6)
                ax3.set_title('Query Volume Trend', fontweight='bold')
                ax3.set_ylabel('Number of Queries')
                ax3.grid(True, alpha=0.3)
                
                # Combined efficiency (success rate / processing time)
                efficiency = [sr / pt if pt > 0 else 0 for sr, pt in zip(success_rates, processing_times)]
                ax4.plot(timestamps, efficiency, marker='D', color='purple', linewidth=2, markersize=6)
                ax4.set_title('Efficiency Trend (Success/Time)', fontweight='bold')
                ax4.set_ylabel('Efficiency Score')
                ax4.grid(True, alpha=0.3)
                
                plt.tight_layout()
                chart_path = self.output_dir / f"{report_id}_trends.png"
                plt.savefig(chart_path, dpi=300, bbox_inches='tight')
                plt.close()
                charts.append(str(chart_path))
        
        # Trend analysis section
        section_data = {
            "title": "Trend Analysis",
            "description": "Time-based trends and performance evolution",
            "metrics": {
                "analysis_period_days": (max(timestamps) - min(timestamps)).days if len(timestamps) > 1 else 0,
                "trend_direction": "improving" if len(success_rates) > 1 and success_rates[-1] > success_rates[0] else "stable",
                "peak_performance_date": timestamps[success_rates.index(max(success_rates))].isoformat() if success_rates else None,
                "total_batches_analyzed": len(batch_results)
            }
        }
        
        return section_data, charts
    
    def _save_report(self, report: AnalyticsReport):
        """Raporu kaydet"""
        try:
            # JSON raporu
            json_path = self.output_dir / f"{report.report_id}.json"
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(report.to_dict(), f, indent=2, ensure_ascii=False, default=str)
            report.export_formats.append(str(json_path))
            
            # CSV export (summary data)
            csv_path = self.output_dir / f"{report.report_id}_summary.csv"
            summary_df = pd.DataFrame([report.summary])
            summary_df.to_csv(csv_path, index=False)
            report.export_formats.append(str(csv_path))
            
            print(f"📄 Rapor kaydedildi: {json_path}")
            
        except Exception as e:
            print(f"⚠️ Rapor kaydetme hatası: {e}")
    
    def generate_grant_comparison_report(self, 
                                       batch_results: List[BatchAnalysisResult],
                                       grant_types: List[str]) -> Dict[str, Any]:
        """
        Grant karşılaştırma raporu oluştur
        
        Args:
            batch_results: Batch sonuçları
            grant_types: Karşılaştırılacak grant tipleri
            
        Returns:
            Karşılaştırma raporu
        """
        comparison_data = {}
        
        for grant_type in grant_types:
            grant_metrics = {
                "total_mentions": 0,
                "cross_document_analyses": 0,
                "average_sources_per_query": 0,
                "common_topics": [],
                "success_rate": 0
            }
            
            total_sources = 0
            relevant_queries = 0
            successful_queries = 0
            
            for batch in batch_results:
                for result in batch.results:
                    # Grant type mention kontrolü
                    if grant_type.lower() in result.query.lower():
                        relevant_queries += 1
                        total_sources += len(result.sources)
                        
                        if result.status.value == "completed":
                            successful_queries += 1
                        
                        # Cross-document analysis
                        cross_doc = result.cross_document_analysis
                        if cross_doc and "grant_groups" in cross_doc:
                            if any(grant_type in gt for gt in cross_doc["grant_groups"].keys()):
                                grant_metrics["cross_document_analyses"] += 1
            
            if relevant_queries > 0:
                grant_metrics["total_mentions"] = relevant_queries
                grant_metrics["average_sources_per_query"] = total_sources / relevant_queries
                grant_metrics["success_rate"] = (successful_queries / relevant_queries) * 100
            
            comparison_data[grant_type] = grant_metrics
        
        return {
            "comparison_type": "grant_types",
            "compared_grants": grant_types,
            "comparison_data": comparison_data,
            "generated_at": datetime.now().isoformat()
        } 