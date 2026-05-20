"""
Anomaly Detection Engine
Detects abnormal system behavior and potential issues
"""
from sklearn.ensemble import IsolationForest
import numpy as np
import pandas as pd
import os

class AnomalyDetector:
    def __init__(self):
        self.model = None
        self.is_trained = False
        self.threshold_cpu = 85
        self.threshold_ram = 80
        self.threshold_disk = 90
    
    def detect_anomaly_simple(self, cpu, ram, disk):
        """Simple rule-based anomaly detection"""
        anomalies = []
        
        if cpu > self.threshold_cpu:
            anomalies.append({
                'type': 'CPU',
                'severity': 'HIGH' if cpu > 90 else 'MEDIUM',
                'value': cpu,
                'message': f'CPU usage critically high: {cpu:.1f}%'
            })
        
        if ram > self.threshold_ram:
            anomalies.append({
                'type': 'RAM',
                'severity': 'HIGH' if ram > 90 else 'MEDIUM',
                'value': ram,
                'message': f'RAM usage critically high: {ram:.1f}%'
            })
        
        if disk > self.threshold_disk:
            anomalies.append({
                'type': 'DISK',
                'severity': 'HIGH',
                'value': disk,
                'message': f'Disk storage almost full: {disk:.1f}%'
            })
        
        return {
            'is_anomaly': len(anomalies) > 0,
            'anomalies': anomalies,
            'risk_level': self._calculate_risk_level(anomalies)
        }
    
    def _calculate_risk_level(self, anomalies):
        """Calculate overall risk level"""
        if not anomalies:
            return 'LOW'
        
        high_count = sum(1 for a in anomalies if a['severity'] == 'HIGH')
        if high_count >= 2:
            return 'CRITICAL'
        elif high_count >= 1:
            return 'HIGH'
        else:
            return 'MEDIUM'
    
    def detect_spike(self, current_value, previous_values, threshold=20):
        """Detect sudden spikes in usage"""
        if len(previous_values) < 2:
            return False
        
        avg_previous = np.mean(previous_values[-5:]) if len(previous_values) >= 5 else previous_values[-1]
        
        if current_value - avg_previous > threshold:
            return True
        return False
    
    def train_ml_model(self, data_file="data/metrics.csv"):
        """Train ML-based anomaly detection using Isolation Forest"""
        try:
            if not os.path.exists(data_file):
                return False
            
            df = pd.read_csv(data_file, names=["timestamp", "cpu", "ram", "disk"])
            
            if len(df) < 20:
                return False
            
            # Prepare features
            X = df[["cpu", "ram", "disk"]].values
            
            # Train Isolation Forest
            self.model = IsolationForest(contamination=0.1, random_state=42)
            self.model.fit(X)
            self.is_trained = True
            
            return True
        except Exception as e:
            print(f"Error training anomaly model: {e}")
            return False
    
    def detect_ml_anomaly(self, cpu, ram, disk):
        """Use ML model to detect anomalies"""
        if not self.is_trained or self.model is None:
            return self.detect_anomaly_simple(cpu, ram, disk)
        
        try:
            prediction = self.model.predict([[cpu, ram, disk]])
            is_anomaly = prediction[0] == -1
            
            if is_anomaly:
                return {
                    'is_anomaly': True,
                    'anomalies': [{
                        'type': 'ML_DETECTED',
                        'severity': 'MEDIUM',
                        'message': 'ML model detected unusual pattern'
                    }],
                    'risk_level': 'MEDIUM'
                }
        except Exception as e:
            print(f"Error in ML anomaly detection: {e}")
        
        return self.detect_anomaly_simple(cpu, ram, disk)

def detect_anomaly(cpu, ram, disk):
    """Convenience function for anomaly detection"""
    detector = AnomalyDetector()
    return detector.detect_anomaly_simple(cpu, ram, disk)
