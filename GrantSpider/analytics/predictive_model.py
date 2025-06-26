"""
Grant Success Predictor Model
PHASE 3.1: Advanced Analytics & Insights

Makine öğrenmesi ile grant başarı tahmini yapan gelişmiş sistem.
Success rate prediction, outcome forecasting, risk assessment.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
import json
from pathlib import Path
import pickle
from collections import defaultdict, Counter

# ML Kütüphaneleri
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve
from sklearn.feature_selection import SelectKBest, f_classif
import warnings
warnings.filterwarnings('ignore')

@dataclass
class PredictionFeatures:
    """Tahmin için kullanılan özellikler"""
    grant_type: str
    application_amount: float
    applicant_history: Dict[str, Any]
    seasonal_factors: Dict[str, Any]
    query_complexity: str
    processing_context: Dict[str, Any]
    historical_success_rate: float
    competition_level: float
    
@dataclass
class PredictionResult:
    """Tahmin sonucu"""
    prediction_id: str
    grant_type: str
    success_probability: float
    confidence_level: float
    risk_factors: List[str]
    recommendations: List[str]
    feature_importance: Dict[str, float]
    model_version: str
    created_at: datetime

@dataclass
class ModelPerformance:
    """Model performans metrikleri"""
    model_id: str
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    auc_score: float
    cross_val_scores: List[float]
    feature_importance: Dict[str, float]
    confusion_matrix: List[List[int]]
    created_at: datetime

class GrantSuccessPredictorModel:
    """
    Grant başarı tahmini için makine öğrenmesi modeli
    
    Bu sınıf, geçmiş verilerden öğrenerek grant başvurularının
    başarı olasılığını tahmin eder ve risk analizi yapar.
    """
    
    def __init__(self, data_path: str = "interfaces/data"):
        """
        Model başlatıcısı
        
        Args:
            data_path: Veri dosyalarının bulunduğu yol
        """
        self.data_path = Path(data_path)
        self.models_path = self.data_path / "models"
        self.models_path.mkdir(exist_ok=True)
        
        # Model konfigürasyonu
        self.config = {
            "test_size": 0.2,
            "random_state": 42,
            "cv_folds": 5,
            "min_samples": 50,
            "feature_selection_k": 15
        }
        
        # Mevcut modeller
        self.models = {
            "random_forest": RandomForestClassifier(n_estimators=100, random_state=42),
            "gradient_boosting": GradientBoostingClassifier(random_state=42),
            "logistic_regression": LogisticRegression(random_state=42, max_iter=1000),
            "svm": SVC(probability=True, random_state=42)
        }
        
        # Aktif model
        self.active_model = None
        self.active_model_name = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_names = []
        
        # Model performans geçmişi
        self.performance_history = []
        self.prediction_history = []
        
        # Grant kategorileri ve risk faktörleri
        self.grant_categories = [
            "WOMEN", "CHILDREN", "DISABLED", "ELDERLY", "MIGRANTS", 
            "HEALTH", "EDUCATION", "INTEGRATION", "WELFARE"
        ]
        
        self.risk_factors = {
            "HIGH_COMPETITION": "Yüksek rekabet seviyesi",
            "LOW_HISTORICAL_SUCCESS": "Düşük geçmiş başarı oranı",
            "COMPLEX_APPLICATION": "Karmaşık başvuru süreci",
            "SEASONAL_DISADVANTAGE": "Mevsimsel dezavantaj",
            "INSUFFICIENT_PREPARATION": "Yetersiz hazırlık",
            "BUDGET_CONSTRAINTS": "Bütçe kısıtlamaları",
            "TIMING_ISSUES": "Zamanlama sorunları"
        }
        
        print("🤖 GrantSuccessPredictorModel başlatıldı")
    
    def train_models(self, 
                    retrain: bool = False,
                    model_selection: bool = True) -> Dict[str, ModelPerformance]:
        """
        Modelleri eğit ve performanslarını değerlendir
        
        Args:
            retrain: Mevcut modelleri yeniden eğit
            model_selection: En iyi modeli otomatik seç
            
        Returns:
            Model performans sonuçları
        """
        print("🎯 Model eğitimi başlatılıyor...")
        
        # Eğitim verilerini hazırla
        X, y, feature_names = self._prepare_training_data()
        
        if len(X) < self.config["min_samples"]:
            print(f"⚠️ Yetersiz eğitim verisi: {len(X)} < {self.config['min_samples']}")
            return {}
        
        # Veriyi böl
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=self.config["test_size"], 
            random_state=self.config["random_state"], stratify=y
        )
        
        # Özellikleri ölçeklendir
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        self.feature_names = feature_names
        
        # Her modeli eğit ve değerlendir
        performance_results = {}
        
        for model_name, model in self.models.items():
            print(f"🔄 {model_name} eğitiliyor...")
            
            try:
                # Modeli eğit
                model.fit(X_train_scaled, y_train)
                
                # Tahminler
                y_pred = model.predict(X_test_scaled)
                y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
                
                # Performans metrikleri hesapla
                performance = self._calculate_model_performance(
                    model_name, y_test, y_pred, y_pred_proba, model
                )
                
                performance_results[model_name] = performance
                self.performance_history.append(performance)
                
                print(f"✅ {model_name} - Accuracy: {performance.accuracy:.3f}, AUC: {performance.auc_score:.3f}")
                
            except Exception as e:
                print(f"❌ {model_name} eğitim hatası: {e}")
                continue
        
        # En iyi modeli seç
        if model_selection and performance_results:
            best_model_name = max(performance_results.keys(), 
                                key=lambda x: performance_results[x].auc_score)
            
            self.active_model = self.models[best_model_name]
            self.active_model_name = best_model_name
            
            print(f"🏆 En iyi model seçildi: {best_model_name}")
            
            # Modeli kaydet
            self._save_model()
        
        # Performans sonuçlarını kaydet
        self._save_performance_results(performance_results)
        
        print(f"✅ Model eğitimi tamamlandı: {len(performance_results)} model")
        return performance_results
    
    def predict_success(self, 
                       features: PredictionFeatures,
                       include_explanations: bool = True) -> PredictionResult:
        """
        Grant başarı olasılığını tahmin et
        
        Args:
            features: Tahmin için özellikler
            include_explanations: Açıklama ve önerileri dahil et
            
        Returns:
            Tahmin sonucu
        """
        if not self.active_model:
            # Mevcut modeli yükle
            if not self._load_model():
                raise ValueError("Aktif model bulunamadı. Önce modeli eğitin.")
        
        print(f"🔮 Grant başarı tahmini yapılıyor: {features.grant_type}")
        
        # Özellikleri vektöre dönüştür
        feature_vector = self._features_to_vector(features)
        
        # Tahmin yap
        success_probability = self.active_model.predict_proba([feature_vector])[0][1]
        confidence_level = self._calculate_confidence(feature_vector)
        
        # Risk faktörlerini belirle
        risk_factors = self._identify_risk_factors(features, success_probability)
        
        # Önerileri oluştur
        recommendations = []
        if include_explanations:
            recommendations = self._generate_recommendations(features, risk_factors, success_probability)
        
        # Feature importance
        feature_importance = {}
        if hasattr(self.active_model, 'feature_importances_'):
            feature_importance = dict(zip(self.feature_names, self.active_model.feature_importances_))
        
        # Sonuç oluştur
        prediction_id = f"pred_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        result = PredictionResult(
            prediction_id=prediction_id,
            grant_type=features.grant_type,
            success_probability=float(success_probability),
            confidence_level=float(confidence_level),
            risk_factors=risk_factors,
            recommendations=recommendations,
            feature_importance=feature_importance,
            model_version=self.active_model_name or "unknown",
            created_at=datetime.now()
        )
        
        # Tahmini kaydet
        self.prediction_history.append(result)
        self._save_prediction_result(result)
        
        print(f"✅ Tahmin tamamlandı: %{success_probability*100:.1f} başarı olasılığı")
        
        return result
    
    def batch_predict(self, 
                     features_list: List[PredictionFeatures]) -> List[PredictionResult]:
        """
        Toplu tahmin işlemi
        
        Args:
            features_list: Tahmin edilecek özelliklerin listesi
            
        Returns:
            Tahmin sonuçlarının listesi
        """
        print(f"📊 Toplu tahmin başlatılıyor: {len(features_list)} adet")
        
        results = []
        for i, features in enumerate(features_list):
            try:
                result = self.predict_success(features, include_explanations=False)
                results.append(result)
                
                if (i + 1) % 10 == 0:
                    print(f"🔄 İlerleme: {i + 1}/{len(features_list)}")
                    
            except Exception as e:
                print(f"⚠️ Tahmin hatası ({i+1}): {e}")
                continue
        
        print(f"✅ Toplu tahmin tamamlandı: {len(results)}/{len(features_list)}")
        return results
    
    def analyze_feature_importance(self) -> Dict[str, float]:
        """
        Özellik önemini analiz et
        
        Returns:
            Özellik önem skorları
        """
        if not self.active_model or not hasattr(self.active_model, 'feature_importances_'):
            print("⚠️ Feature importance analizi için uygun model bulunamadı")
            return {}
        
        importance_dict = dict(zip(self.feature_names, self.active_model.feature_importances_))
        
        # Önem sırasına göre sırala
        sorted_importance = dict(sorted(importance_dict.items(), 
                                      key=lambda x: x[1], reverse=True))
        
        print("📊 Özellik Önem Analizi:")
        for feature, importance in list(sorted_importance.items())[:10]:
            print(f"  {feature}: {importance:.3f}")
        
        return sorted_importance
    
    def evaluate_model_performance(self) -> Dict[str, Any]:
        """
        Model performansını değerlendir
        
        Returns:
            Performans metrikleri
        """
        if not self.performance_history:
            return {"message": "Henüz model performans verisi yok"}
        
        latest_performance = self.performance_history[-1]
        
        return {
            "latest_model": latest_performance.model_id,
            "accuracy": latest_performance.accuracy,
            "precision": latest_performance.precision,
            "recall": latest_performance.recall,
            "f1_score": latest_performance.f1_score,
            "auc_score": latest_performance.auc_score,
            "cv_mean": np.mean(latest_performance.cross_val_scores),
            "cv_std": np.std(latest_performance.cross_val_scores),
            "feature_count": len(latest_performance.feature_importance),
            "evaluation_date": latest_performance.created_at.isoformat()
        }
    
    def get_prediction_insights(self, 
                              grant_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Tahmin insightları al
        
        Args:
            grant_type: Spesifik grant türü filtresi
            
        Returns:
            Tahmin insightları
        """
        if not self.prediction_history:
            return {"message": "Henüz tahmin verisi yok"}
        
        predictions = self.prediction_history
        if grant_type:
            predictions = [p for p in predictions if p.grant_type == grant_type]
        
        if not predictions:
            return {"message": f"'{grant_type}' için tahmin verisi yok"}
        
        # İstatistikler hesapla
        success_probs = [p.success_probability for p in predictions]
        confidence_levels = [p.confidence_level for p in predictions]
        
        # Risk faktörlerini topla
        all_risk_factors = []
        for p in predictions:
            all_risk_factors.extend(p.risk_factors)
        
        risk_counter = Counter(all_risk_factors)
        
        return {
            "total_predictions": len(predictions),
            "avg_success_probability": np.mean(success_probs),
            "avg_confidence": np.mean(confidence_levels),
            "high_success_rate": len([p for p in success_probs if p > 0.7]) / len(success_probs),
            "low_success_rate": len([p for p in success_probs if p < 0.3]) / len(success_probs),
            "most_common_risks": dict(risk_counter.most_common(5)),
            "grant_type_filter": grant_type or "ALL"
        }
    
    def _prepare_training_data(self) -> Tuple[np.ndarray, np.ndarray, List[str]]:
        """Eğitim verilerini hazırla"""
        try:
            # Geçmiş verileri yükle
            historical_data = self._load_historical_training_data()
            
            if not historical_data:
                print("⚠️ Eğitim verisi bulunamadı")
                return np.array([]), np.array([]), []
            
            # Özellikleri çıkar
            features_list = []
            labels = []
            
            for data_point in historical_data:
                try:
                    # Özellik vektörü oluştur
                    feature_vector = self._extract_features_from_data(data_point)
                    
                    # Label (başarı/başarısızlık)
                    label = 1 if data_point.get("success", False) else 0
                    
                    features_list.append(feature_vector)
                    labels.append(label)
                    
                except Exception as e:
                    print(f"⚠️ Veri noktası işleme hatası: {e}")
                    continue
            
            if not features_list:
                print("⚠️ İşlenebilir özellik bulunamadı")
                return np.array([]), np.array([]), []
            
            # NumPy array'e dönüştür
            X = np.array(features_list)
            y = np.array(labels)
            
            # Özellik isimleri
            feature_names = self._get_feature_names()
            
            print(f"📊 Eğitim verisi hazırlandı: {X.shape[0]} sample, {X.shape[1]} feature")
            print(f"📈 Pozitif örnekler: {sum(y)} / {len(y)} (%{sum(y)/len(y)*100:.1f})")
            
            return X, y, feature_names
            
        except Exception as e:
            print(f"❌ Eğitim verisi hazırlama hatası: {e}")
            return np.array([]), np.array([]), []
    
    def _load_historical_training_data(self) -> List[Dict[str, Any]]:
        """Geçmiş eğitim verilerini yükle"""
        try:
            data = []
            
            # Batch results'dan yükle
            batch_results_path = self.data_path / "batch_results"
            if batch_results_path.exists():
                for file_path in batch_results_path.glob("*.json"):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            batch_data = json.load(f)
                        
                        # Batch verilerini eğitim formatına dönüştür
                        training_data = self._process_batch_for_training(batch_data)
                        data.extend(training_data)
                        
                    except Exception as e:
                        print(f"⚠️ Batch dosya okuma hatası: {e}")
                        continue
            
            # Memory verilerinden yükle
            memory_path = self.data_path / "memory"
            if memory_path.exists():
                for file_path in memory_path.glob("*.json"):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            memory_data = json.load(f)
                        
                        # Memory verilerini eğitim formatına dönüştür
                        training_data = self._process_memory_for_training(memory_data)
                        data.extend(training_data)
                        
                    except Exception as e:
                        print(f"⚠️ Memory dosya okuma hatası: {e}")
                        continue
            
            print(f"📚 {len(data)} eğitim verisi yüklendi")
            return data
            
        except Exception as e:
            print(f"❌ Geçmiş veri yükleme hatası: {e}")
            return []
    
    def _process_batch_for_training(self, batch_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Batch verilerini eğitim için işle"""
        training_data = []
        
        try:
            for query_result in batch_data.get("query_results", []):
                # Eğitim verisi formatı
                training_point = {
                    "timestamp": batch_data.get("created_at"),
                    "grant_types": query_result.get("metadata", {}).get("grant_types", []),
                    "processing_time": query_result.get("processing_time", 0),
                    "success": query_result.get("success", False),
                    "response_quality": query_result.get("metadata", {}).get("response_quality", 0.5),
                    "sources_count": len(query_result.get("metadata", {}).get("sources", [])),
                    "query_complexity": self._determine_complexity(query_result.get("query", "")),
                    "batch_id": batch_data.get("batch_id"),
                    "data_source": "batch"
                }
                training_data.append(training_point)
                
        except Exception as e:
            print(f"⚠️ Batch veri işleme hatası: {e}")
        
        return training_data
    
    def _process_memory_for_training(self, memory_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Memory verilerini eğitim için işle"""
        training_data = []
        
        try:
            for entry in memory_data.get("conversation_history", []):
                if entry.get("role") == "assistant":
                    # Eğitim verisi formatı
                    training_point = {
                        "timestamp": entry.get("timestamp"),
                        "grant_types": entry.get("context", {}).get("grant_types_mentioned", []),
                        "processing_time": entry.get("context", {}).get("processing_time", 0),
                        "success": True,  # Memory'deki cevaplar genelde başarılı
                        "response_quality": entry.get("context", {}).get("response_quality", 0.7),
                        "sources_count": entry.get("context", {}).get("sources_count", 0),
                        "query_complexity": entry.get("context", {}).get("query_complexity", "medium"),
                        "session_id": entry.get("session_id"),
                        "data_source": "memory"
                    }
                    training_data.append(training_point)
                    
        except Exception as e:
            print(f"⚠️ Memory veri işleme hatası: {e}")
        
        return training_data
    
    def _extract_features_from_data(self, data_point: Dict[str, Any]) -> List[float]:
        """Veri noktasından özellik vektörü çıkar"""
        features = []
        
        try:
            # 1. Grant türü (one-hot encoding)
            grant_types = data_point.get("grant_types", [])
            for category in self.grant_categories:
                features.append(1.0 if category in grant_types else 0.0)
            
            # 2. İşlem süresi (normalized)
            processing_time = min(data_point.get("processing_time", 0), 300)  # Cap at 5 minutes
            features.append(processing_time / 300.0)
            
            # 3. Kaynak sayısı (normalized)
            sources_count = min(data_point.get("sources_count", 0), 10)  # Cap at 10
            features.append(sources_count / 10.0)
            
            # 4. Kalite puanı
            features.append(data_point.get("response_quality", 0.5))
            
            # 5. Karmaşıklık seviyesi
            complexity = data_point.get("query_complexity", "medium")
            complexity_map = {"simple": 0.33, "medium": 0.67, "complex": 1.0}
            features.append(complexity_map.get(complexity, 0.67))
            
            # 6. Zaman faktörleri
            timestamp_str = data_point.get("timestamp")
            if timestamp_str:
                try:
                    timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                    # Haftanın günü (0-6)
                    features.append(timestamp.weekday() / 6.0)
                    # Saati (0-23)
                    features.append(timestamp.hour / 23.0)
                    # Ay (1-12)
                    features.append(timestamp.month / 12.0)
                except:
                    features.extend([0.5, 0.5, 0.5])  # Default values
            else:
                features.extend([0.5, 0.5, 0.5])
            
            # 7. Veri kaynağı
            data_source = data_point.get("data_source", "unknown")
            source_map = {"batch": 1.0, "memory": 0.5, "unknown": 0.0}
            features.append(source_map.get(data_source, 0.0))
            
        except Exception as e:
            print(f"⚠️ Özellik çıkarma hatası: {e}")
            # Hata durumunda default features döndür
            features = [0.0] * self._get_feature_count()
        
        return features
    
    def _get_feature_names(self) -> List[str]:
        """Özellik isimlerini döndür"""
        names = []
        
        # Grant kategorileri
        for category in self.grant_categories:
            names.append(f"grant_type_{category}")
        
        # Diğer özellikler
        names.extend([
            "processing_time_norm",
            "sources_count_norm", 
            "response_quality",
            "query_complexity",
            "weekday_norm",
            "hour_norm",
            "month_norm",
            "data_source"
        ])
        
        return names
    
    def _get_feature_count(self) -> int:
        """Toplam özellik sayısını döndür"""
        return len(self.grant_categories) + 8  # 9 grant types + 8 other features
    
    def _features_to_vector(self, features: PredictionFeatures) -> List[float]:
        """PredictionFeatures'i vektöre dönüştür"""
        vector = []
        
        # Grant türü
        for category in self.grant_categories:
            vector.append(1.0 if category == features.grant_type else 0.0)
        
        # Diğer özellikler
        vector.append(min(features.processing_context.get("expected_time", 30), 300) / 300.0)
        vector.append(min(features.processing_context.get("sources_available", 5), 10) / 10.0)
        vector.append(features.historical_success_rate)
        
        # Karmaşıklık
        complexity_map = {"simple": 0.33, "medium": 0.67, "complex": 1.0}
        vector.append(complexity_map.get(features.query_complexity, 0.67))
        
        # Zaman faktörleri (şu anki zaman)
        now = datetime.now()
        vector.append(now.weekday() / 6.0)
        vector.append(now.hour / 23.0)
        vector.append(now.month / 12.0)
        
        # Veri kaynağı (varsayılan: prediction)
        vector.append(0.8)
        
        return vector
    
    def _calculate_model_performance(self, 
                                   model_name: str,
                                   y_true: np.ndarray,
                                   y_pred: np.ndarray,
                                   y_pred_proba: np.ndarray,
                                   model) -> ModelPerformance:
        """Model performansını hesapla"""
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
        
        # Temel metrikler
        accuracy = accuracy_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred, zero_division=0)
        recall = recall_score(y_true, y_pred, zero_division=0)
        f1 = f1_score(y_true, y_pred, zero_division=0)
        auc = roc_auc_score(y_true, y_pred_proba)
        
        # Cross validation
        cv_scores = cross_val_score(model, self.scaler.transform(self._get_cv_data()), 
                                   self._get_cv_labels(), cv=self.config["cv_folds"])
        
        # Feature importance
        feature_importance = {}
        if hasattr(model, 'feature_importances_'):
            feature_importance = dict(zip(self.feature_names, model.feature_importances_))
        
        # Confusion matrix
        cm = confusion_matrix(y_true, y_pred).tolist()
        
        return ModelPerformance(
            model_id=f"{model_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            accuracy=accuracy,
            precision=precision,
            recall=recall,
            f1_score=f1,
            auc_score=auc,
            cross_val_scores=cv_scores.tolist(),
            feature_importance=feature_importance,
            confusion_matrix=cm,
            created_at=datetime.now()
        )
    
    def _calculate_confidence(self, feature_vector: List[float]) -> float:
        """Tahmin güvenilirliğini hesapla"""
        # Basit güven hesaplama (geliştirilecek)
        try:
            if hasattr(self.active_model, 'predict_proba'):
                probs = self.active_model.predict_proba([feature_vector])[0]
                # En yüksek olasılık - ikinci en yüksek olasılık
                confidence = max(probs) - min(probs)
                return min(confidence, 1.0)
            return 0.7  # Default confidence
        except:
            return 0.5
    
    def _identify_risk_factors(self, 
                             features: PredictionFeatures,
                             success_prob: float) -> List[str]:
        """Risk faktörlerini belirle"""
        risk_factors = []
        
        # Düşük başarı olasılığı
        if success_prob < 0.3:
            risk_factors.append("LOW_SUCCESS_PROBABILITY")
        
        # Yüksek rekabet
        if features.competition_level > 0.7:
            risk_factors.append("HIGH_COMPETITION")
        
        # Düşük geçmiş başarı
        if features.historical_success_rate < 0.5:
            risk_factors.append("LOW_HISTORICAL_SUCCESS")
        
        # Karmaşık başvuru
        if features.query_complexity == "complex":
            risk_factors.append("COMPLEX_APPLICATION")
        
        # Mevsimsel faktörler
        seasonal_score = features.seasonal_factors.get("current_season_score", 0.5)
        if seasonal_score < 0.4:
            risk_factors.append("SEASONAL_DISADVANTAGE")
        
        return risk_factors
    
    def _generate_recommendations(self, 
                                features: PredictionFeatures,
                                risk_factors: List[str],
                                success_prob: float) -> List[str]:
        """Öneriler oluştur"""
        recommendations = []
        
        if success_prob < 0.5:
            recommendations.append("Başvuru öncesi detaylı hazırlık yapın")
            recommendations.append("Benzer başarılı başvuruları inceleyin")
        
        if "HIGH_COMPETITION" in risk_factors:
            recommendations.append("Başvurunuzu farklılaştıracak özel değerler ekleyin")
        
        if "LOW_HISTORICAL_SUCCESS" in risk_factors:
            recommendations.append("Geçmiş başarısızlık nedenlerini analiz edin")
        
        if "COMPLEX_APPLICATION" in risk_factors:
            recommendations.append("Uzman desteği alın")
            recommendations.append("Başvuru sürecini adım adım planlayın")
        
        if "SEASONAL_DISADVANTAGE" in risk_factors:
            recommendations.append("Başvuru zamanlamasını yeniden değerlendirin")
        
        if success_prob > 0.7:
            recommendations.append("Güçlü bir başvuru profili var, güvenle ilerleyin")
        
        return recommendations
    
    def _determine_complexity(self, query: str) -> str:
        """Sorgu karmaşıklığını belirle"""
        if len(query) < 50:
            return "simple"
        elif len(query) < 150:
            return "medium"
        else:
            return "complex"
    
    def _save_model(self):
        """Aktif modeli kaydet"""
        try:
            model_file = self.models_path / f"active_model_{self.active_model_name}.pkl"
            
            model_data = {
                "model": self.active_model,
                "scaler": self.scaler,
                "feature_names": self.feature_names,
                "model_name": self.active_model_name,
                "saved_at": datetime.now().isoformat()
            }
            
            with open(model_file, 'wb') as f:
                pickle.dump(model_data, f)
            
            print(f"💾 Model kaydedildi: {model_file}")
            
        except Exception as e:
            print(f"⚠️ Model kaydetme hatası: {e}")
    
    def _load_model(self) -> bool:
        """Mevcut modeli yükle"""
        try:
            # En son model dosyasını bul
            model_files = list(self.models_path.glob("active_model_*.pkl"))
            if not model_files:
                return False
            
            latest_model = max(model_files, key=lambda x: x.stat().st_mtime)
            
            with open(latest_model, 'rb') as f:
                model_data = pickle.load(f)
            
            self.active_model = model_data["model"]
            self.scaler = model_data["scaler"]
            self.feature_names = model_data["feature_names"]
            self.active_model_name = model_data["model_name"]
            
            print(f"📂 Model yüklendi: {latest_model}")
            return True
            
        except Exception as e:
            print(f"⚠️ Model yükleme hatası: {e}")
            return False
    
    def _save_performance_results(self, performance_results: Dict[str, ModelPerformance]):
        """Performans sonuçlarını kaydet"""
        try:
            results_file = self.data_path / "analytics" / f"model_performance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            results_file.parent.mkdir(exist_ok=True)
            
            # Serialize performance results
            serialized_results = {}
            for model_name, performance in performance_results.items():
                perf_dict = asdict(performance)
                perf_dict['created_at'] = performance.created_at.isoformat()
                serialized_results[model_name] = perf_dict
            
            with open(results_file, 'w', encoding='utf-8') as f:
                json.dump(serialized_results, f, indent=2, ensure_ascii=False)
            
            print(f"📊 Performans sonuçları kaydedildi: {results_file}")
            
        except Exception as e:
            print(f"⚠️ Performans kaydetme hatası: {e}")
    
    def _save_prediction_result(self, result: PredictionResult):
        """Tahmin sonucunu kaydet"""
        try:
            predictions_path = self.data_path / "predictions"
            predictions_path.mkdir(exist_ok=True)
            
            result_file = predictions_path / f"prediction_{result.prediction_id}.json"
            
            result_dict = asdict(result)
            result_dict['created_at'] = result.created_at.isoformat()
            
            with open(result_file, 'w', encoding='utf-8') as f:
                json.dump(result_dict, f, indent=2, ensure_ascii=False)
            
        except Exception as e:
            print(f"⚠️ Tahmin kaydetme hatası: {e}")
    
    # Placeholder metodları (gelişmiş özellikler için)
    def _get_cv_data(self):
        """Cross validation verisi - placeholder"""
        return np.random.rand(100, self._get_feature_count())
    
    def _get_cv_labels(self):
        """Cross validation labelları - placeholder"""
        return np.random.randint(0, 2, 100) 