import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import os
from datetime import datetime, timedelta

class WeatherPredictor:
    def __init__(self):
        self.rain_model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.snow_model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
        
    def load_and_train(self, csv_path):
        """Load data from CSV and train the models for rain and snow"""
        df = pd.read_csv(csv_path)
        
        # Prepare features and targets
        X = df[['temperature', 'humidity', 'pressure', 'wind_speed', 'cloud_cover']].values
        y_rain = df['rain'].values
        y_snow = df['snow'].values
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train both models
        self.rain_model.fit(X_scaled, y_rain)
        self.snow_model.fit(X_scaled, y_snow)
        self.is_trained = True
        
    def predict(self, temperature, humidity, pressure, wind_speed, cloud_cover):
        """Predict if it will rain or snow"""
        if not self.is_trained:
            raise Exception("Model not trained yet")
        
        features = np.array([[temperature, humidity, pressure, wind_speed, cloud_cover]])
        features_scaled = self.scaler.transform(features)
        
        rain_prediction = self.rain_model.predict(features_scaled)[0]
        rain_probability = self.rain_model.predict_proba(features_scaled)[0]
        
        snow_prediction = self.snow_model.predict(features_scaled)[0]
        snow_probability = self.snow_model.predict_proba(features_scaled)[0]
        
        return {
            'will_rain': bool(rain_prediction),
            'rain_probability': float(rain_probability[1]),
            'will_snow': bool(snow_prediction),
            'snow_probability': float(snow_probability[1])
        }
    
    def predict_week(self, csv_path):
        """Predict rain for the next 5 days (Mon-Fri)"""
        # Read the CSV to get the latest data patterns
        df = pd.read_csv(csv_path)
        
        # Generate predictions for Monday to Friday
        predictions = []
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        
        # Get today's date (Monday, Jan 12, 2026)
        today = datetime(2026, 1, 12)
        
        # Use last row as a base for predictions with slight variations
        if len(df) > 0:
            last_row = df.iloc[-1]
            
            for i, day in enumerate(days):
                date = today + timedelta(days=i)
                
                # Add slight variations to simulate changing weather
                temp_variation = np.random.uniform(-2, 2)
                humidity_variation = np.random.uniform(-5, 5)
                pressure_variation = np.random.uniform(-2, 2)
                wind_variation = np.random.uniform(-2, 2)
                cloud_variation = np.random.uniform(-10, 10)
                
                temp = float(last_row['temperature']) + temp_variation
                humidity = max(0, min(100, float(last_row['humidity']) + humidity_variation))
                pressure = float(last_row['pressure']) + pressure_variation
                wind = max(0, float(last_row['wind_speed']) + wind_variation)
                cloud = max(0, min(100, float(last_row['cloud_cover']) + cloud_variation))
                
                result = self.predict(temp, humidity, pressure, wind, cloud)
                
                predictions.append({
                    'day': day,
                    'date': date.strftime('%Y-%m-%d'),
                    'will_rain': result['will_rain'],
                    'probability': result['probability'],
                    'temperature': round(temp, 1),
                    'humidity': round(humidity, 1),
                    'cloud_cover': round(cloud, 1)
                })
        
        return predictions
