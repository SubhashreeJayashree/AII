"""
Machine Learning Prediction Engine
Predicts future CPU/RAM usage using Linear Regression and Time Series
"""
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
import os
import pickle

class SystemPredictor:
    def __init__(self):
        self.model = None
        self.rf_model = None
        self.is_trained = False
        
    def train_model(self, data_file="data/metrics.csv"):
        """Train prediction models on historical data"""
        try:
            if not os.path.exists(data_file):
                print(f"Data file {data_file} not found. Model will use default predictions.")
                return False
            
            df = pd.read_csv(data_file, names=["timestamp", "cpu", "ram", "disk"])
            
            if len(df) < 10:
                print("Insufficient data for training. Need at least 10 records.")
                return False
            
            # Use last 100 records for training (or all if less)
            df = df.tail(100)
            
            # Prepare features (current CPU, RAM, Disk)
            X = df[["cpu", "ram", "disk"]].values
            
            # Target: next CPU usage (shifted by 1)
            y_cpu = df["cpu"].shift(-1).dropna().values
            X_cpu = X[:-1]
            
            # Train Linear Regression model
            if len(X_cpu) > 0 and len(y_cpu) > 0:
                self.model = LinearRegression()
                self.model.fit(X_cpu, y_cpu)
                
                # Train Random Forest for better accuracy
                self.rf_model = RandomForestRegressor(n_estimators=50, random_state=42)
                self.rf_model.fit(X_cpu, y_cpu)
                
                self.is_trained = True
                
                # Save model
                os.makedirs("models", exist_ok=True)
                with open("models/predictor.pkl", "wb") as f:
                    pickle.dump(self.model, f)
                with open("models/rf_predictor.pkl", "wb") as f:
                    pickle.dump(self.rf_model, f)
                
                print("Models trained successfully!")
                return True
        except Exception as e:
            print(f"Error training model: {e}")
            return False
    
    def predict_cpu(self, cpu, ram, disk):
        """Predict next CPU usage"""
        if not self.is_trained or self.model is None:
            # Default prediction: assume current CPU continues
            return float(cpu)
        
        try:
            # Use Random Forest if available (more accurate)
            if self.rf_model:
                prediction = self.rf_model.predict([[cpu, ram, disk]])[0]
            else:
                prediction = self.model.predict([[cpu, ram, disk]])[0]
            
            # Clamp prediction between 0 and 100
            return max(0, min(100, float(prediction)))
        except Exception as e:
            print(f"Error in prediction: {e}")
            return float(cpu)
    
    def predict_ram(self, cpu, ram, disk):
        """Predict next RAM usage"""
        if not self.is_trained or self.model is None:
            return float(ram)
        
        try:
            # For RAM, we can use similar approach
            # In a more advanced version, train separate model for RAM
            prediction = self.model.predict([[cpu, ram, disk]])[0]
            return max(0, min(100, float(prediction)))
        except:
            return float(ram)
    
    def load_model(self):
        """Load pre-trained model from file"""
        try:
            if os.path.exists("models/predictor.pkl"):
                with open("models/predictor.pkl", "rb") as f:
                    self.model = pickle.load(f)
                self.is_trained = True
                return True
        except Exception as e:
            print(f"Error loading model: {e}")
        return False

def train_model():
    """Convenience function to train model"""
    predictor = SystemPredictor()
    predictor.train_model()
    return predictor

def predict(model, cpu, ram, disk):
    """Convenience function for prediction"""
    if isinstance(model, SystemPredictor):
        return model.predict_cpu(cpu, ram, disk)
    return float(cpu)
