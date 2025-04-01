import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from sklearn.metrics.pairwise import cosine_similarity
from typing import Dict, List, Any, Tuple
import joblib
import os
from datetime import datetime, timedelta
import hashlib
import levenshtein
import time

class MetadataAnalyzer:
    """Machine learning analyzer for metadata system."""
    
    def __init__(self, scanner, tracker, organizer):
        self.scanner = scanner
        self.tracker = tracker
        self.organizer = organizer
        self.models = {}
        self.load_models()
    
    def load_models(self):
        """Load or initialize ML models."""
        model_path = os.path.join(os.path.dirname(__file__), 'models')
        os.makedirs(model_path, exist_ok=True)
        
        model_files = {
            'anomaly_detector': 'anomaly_detector.joblib',
            'file_clusterer': 'file_clusterer.joblib',
            'usage_predictor': 'usage_predictor.joblib'
        }
        
        for name, filename in model_files.items():
            path = os.path.join(model_path, filename)
            if os.path.exists(path):
                self.models[name] = joblib.load(path)
            else:
                self.models[name] = self._initialize_model(name)
    
    def _initialize_model(self, model_type: str) -> Any:
        """Initialize a new ML model."""
        if model_type == 'anomaly_detector':
            return IsolationForest(contamination=0.1, random_state=42)
        elif model_type == 'file_clusterer':
            return DBSCAN(eps=0.3, min_samples=2)
        elif model_type == 'usage_predictor':
            return None  # Will be initialized with first data
        return None
    
    def save_models(self):
        """Save trained models."""
        model_path = os.path.join(os.path.dirname(__file__), 'models')
        for name, model in self.models.items():
            if model is not None:
                joblib.dump(model, os.path.join(model_path, f'{name}.joblib'))
    
    def detect_anomalies(self) -> List[Dict[str, Any]]:
        """Detect anomalous file behavior."""
        features = self._extract_file_features()
        if not features.empty:
            predictions = self.models['anomaly_detector'].predict(features)
            anomalies = []
            
            for idx, is_anomaly in enumerate(predictions):
                if is_anomaly == -1:  # Anomaly detected
                    file_path = features.index[idx]
                    anomalies.append({
                        'file': file_path,
                        'reason': self._analyze_anomaly_reason(file_path, features.iloc[idx]),
                        'score': float(self.models['anomaly_detector'].score_samples([features.iloc[idx]])[0]),
                        'timestamp': datetime.now().isoformat()
                    })
            
            return anomalies
        return []
    
    def find_file_clusters(self) -> Dict[str, List[str]]:
        """Find clusters of related files."""
        features = self._extract_file_features()
        if not features.empty:
            clusters = self.models['file_clusterer'].fit_predict(features)
            
            cluster_dict = {}
            for idx, cluster_id in enumerate(clusters):
                if cluster_id != -1:  # Not noise
                    cluster_name = f'cluster_{cluster_id}'
                    if cluster_name not in cluster_dict:
                        cluster_dict[cluster_name] = []
                    cluster_dict[cluster_name].append(features.index[idx])
            
            return cluster_dict
        return {}
    
    def predict_file_usage(self, file_path: str, days: int = 7) -> Dict[str, Any]:
        """Predict future file usage patterns."""
        history = self.tracker.get_file_usage_history(file_path)
        if not history:
            return {'error': 'No history available'}
        
        df = pd.DataFrame(history)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)
        
        # Resample to daily frequency
        daily_counts = df.resample('D').size()
        
        # Simple moving average prediction
        window = min(7, len(daily_counts))
        if window > 0:
            avg_usage = daily_counts.rolling(window=window).mean().iloc[-1]
            trend = (daily_counts.iloc[-1] - daily_counts.iloc[-window]) / window if window > 1 else 0
            
            predictions = []
            for day in range(1, days + 1):
                predicted_usage = max(0, avg_usage + trend * day)
                predictions.append({
                    'day': (datetime.now() + timedelta(days=day)).isoformat(),
                    'predicted_usage': float(predicted_usage)
                })
            
            return {
                'file': file_path,
                'predictions': predictions,
                'confidence': self._calculate_prediction_confidence(daily_counts)
            }
        
        return {'error': 'Insufficient data for prediction'}
    
    def suggest_optimizations(self) -> List[Dict[str, Any]]:
        """Suggest optimizations based on ML analysis."""
        suggestions = []
        
        # Analyze file clusters
        clusters = self.find_file_clusters()
        for cluster_name, files in clusters.items():
            if len(files) > 1:
                suggestions.append({
                    'type': 'cluster_optimization',
                    'files': files,
                    'suggestion': 'Consider consolidating these related files',
                    'confidence': 0.8
                })
        
        # Analyze usage patterns
        features = self._extract_file_features()
        if not features.empty:
            for file_path in features.index:
                prediction = self.predict_file_usage(file_path)
                if 'predictions' in prediction:
                    avg_predicted_usage = np.mean([p['predicted_usage'] for p in prediction['predictions']])
                    if avg_predicted_usage < 0.1:  # Very low predicted usage
                        suggestions.append({
                            'type': 'usage_optimization',
                            'file': file_path,
                            'suggestion': 'Consider archiving this rarely used file',
                            'confidence': prediction['confidence']
                        })
        
        return suggestions
    
    def _extract_file_features(self) -> pd.DataFrame:
        """Extract features for ML analysis."""
        features = []
        indices = []
        
        for filepath, metadata in self.scanner.metadata_db.items():
            history = self.tracker.get_file_usage_history(filepath)
            if history:
                # Calculate feature vector
                access_count = sum(1 for log in history if log['type'] == 'accessed')
                mod_count = sum(1 for log in history if log['type'] == 'modified')
                dep_count = len(metadata.dependencies)
                usage_count = metadata.usage_count
                
                # Get timestamps
                timestamps = [datetime.fromisoformat(log['timestamp']) for log in history]
                last_access = max(timestamps)
                first_access = min(timestamps)
                age = (datetime.now() - first_access).days
                
                # Create feature vector
                feature_vector = [
                    access_count,
                    mod_count,
                    dep_count,
                    usage_count,
                    age,
                    (datetime.now() - last_access).days
                ]
                
                features.append(feature_vector)
                indices.append(filepath)
        
        if features:
            df = pd.DataFrame(features, index=indices, columns=[
                'access_count',
                'mod_count',
                'dep_count',
                'usage_count',
                'age',
                'days_since_access'
            ])
            
            # Normalize features
            scaler = StandardScaler()
            return pd.DataFrame(
                scaler.fit_transform(df),
                index=df.index,
                columns=df.columns
            )
        
        return pd.DataFrame()
    
    def _analyze_anomaly_reason(self, file_path: str, features: pd.Series) -> str:
        """Analyze why a file was flagged as anomalous."""
        reasons = []
        
        # Check each feature for extreme values
        if abs(features['access_count']) > 2:  # More than 2 std from mean
            reasons.append('unusual access pattern')
        if abs(features['mod_count']) > 2:
            reasons.append('unusual modification pattern')
        if abs(features['dep_count']) > 2:
            reasons.append('unusual number of dependencies')
        if abs(features['days_since_access']) > 2:
            reasons.append('unusually long period without access')
        
        if not reasons:
            reasons.append('combination of unusual patterns')
        
        return 'Detected ' + ', '.join(reasons)
    
    def _calculate_prediction_confidence(self, usage_data: pd.Series) -> float:
        """Calculate confidence score for usage predictions."""
        if len(usage_data) < 2:
            return 0.5
        
        # Calculate stability of usage pattern
        std = usage_data.std()
        mean = usage_data.mean()
        cv = std / mean if mean > 0 else float('inf')
        
        # Calculate confidence based on coefficient of variation
        confidence = 1 / (1 + cv)
        
        # Adjust confidence based on data amount
        data_factor = min(len(usage_data) / 30, 1)  # Max out at 30 days of data
        
        return float(confidence * data_factor)
    
    def find_duplicates(self):
        """Find duplicate files in the system using content and metadata analysis."""
        duplicates = []
        file_hashes = {}
        
        # Get all files from scanner
        files = self.scanner.get_all_files()
        
        for file in files:
            if not os.path.exists(file['path']):
                continue
                
            # Calculate file hash
            with open(file['path'], 'rb') as f:
                content = f.read()
                file_hash = hashlib.md5(content).hexdigest()
            
            # Get file metadata
            metadata = {
                'size': os.path.getsize(file['path']),
                'modified': os.path.getmtime(file['path']),
                'name': os.path.basename(file['path']),
                'extension': os.path.splitext(file['path'])[1]
            }
            
            # Check for duplicates
            if file_hash in file_hashes:
                # Found a duplicate
                original = file_hashes[file_hash]
                duplicates.append({
                    'original': {
                        'path': original['path'],
                        'metadata': original['metadata']
                    },
                    'duplicate': {
                        'path': file['path'],
                        'metadata': metadata
                    },
                    'similarity': self._calculate_similarity(original['metadata'], metadata),
                    'confidence': 1.0 if file_hash == original['hash'] else 0.9
                })
            else:
                # Store file info
                file_hashes[file_hash] = {
                    'path': file['path'],
                    'hash': file_hash,
                    'metadata': metadata
                }
        
        return duplicates
    
    def _calculate_similarity(self, metadata1, metadata2):
        """Calculate similarity score between two files based on metadata."""
        similarity = 0.0
        
        # Compare file sizes
        if metadata1['size'] == metadata2['size']:
            similarity += 0.3
        
        # Compare file names (excluding extension)
        name1 = os.path.splitext(metadata1['name'])[0]
        name2 = os.path.splitext(metadata2['name'])[0]
        
        # Use Levenshtein distance for name similarity
        name_similarity = 1 - (levenshtein(name1, name2) / max(len(name1), len(name2)))
        similarity += 0.4 * name_similarity
        
        # Compare extensions
        if metadata1['extension'] == metadata2['extension']:
            similarity += 0.3
        
        return similarity

    def find_outdated_files(self):
        """Find outdated files based on usage patterns and content analysis."""
        outdated = []
        
        # Get all files from scanner
        files = self.scanner.get_all_files()
        
        for file in files:
            if not os.path.exists(file['path']):
                continue
            
            # Get file usage history
            usage = self.tracker.get_file_usage(file['path'])
            
            # Calculate metrics
            last_access = usage.get('last_access', 0)
            access_frequency = usage.get('access_frequency', 0)
            modification_frequency = usage.get('modification_frequency', 0)
            
            # Current time
            current_time = time.time()
            
            # Calculate scores
            time_score = 1.0 - min(1.0, (current_time - last_access) / (365 * 24 * 3600))  # Score based on last access
            usage_score = min(1.0, access_frequency / 100)  # Score based on access frequency
            mod_score = min(1.0, modification_frequency / 50)  # Score based on modification frequency
            
            # Weighted average of scores
            total_score = (0.4 * time_score + 0.3 * usage_score + 0.3 * mod_score)
            
            # If score is low, consider file outdated
            if total_score < 0.2:
                outdated.append({
                    'path': file['path'],
                    'last_access': last_access,
                    'access_frequency': access_frequency,
                    'modification_frequency': modification_frequency,
                    'score': total_score,
                    'confidence': 1.0 - total_score
                })
        
        return sorted(outdated, key=lambda x: x['score']) 