from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .ml_model import WeatherPredictor
from .weather_service import WeatherService
import os
from pathlib import Path

# Initialize predictor and weather service
predictor = WeatherPredictor()
weather_service = WeatherService()

# Get the path to the CSV file
BASE_DIR = Path(__file__).resolve().parent.parent.parent
CSV_PATH = os.path.join(BASE_DIR, 'kosovo_weather_data.csv')

# Train the model on startup
try:
    predictor.load_and_train(CSV_PATH)
except Exception as e:
    print(f"Error loading model: {e}")

@api_view(['GET'])
def predict_today(request):
    """Predict if it will rain or snow today using real weather data"""
    try:
        # Get real current weather for Kosovo
        current = weather_service.get_current_weather()
        
        result = predictor.predict(
            current['temperature'],
            current['humidity'],
            current['pressure'],
            current['wind_speed'],
            current['cloud_cover']
        )
        
        # Determine message
        if result['will_snow']:
            message = 'Snow expected today'
        elif result['will_rain']:
            message = 'Rain expected today'
        else:
            message = 'No rain or snow expected today'
        
        return Response({
            'day': 'Monday',
            'date': '2026-01-12',
            'will_rain': result['will_rain'],
            'rain_probability': result['rain_probability'],
            'will_snow': result['will_snow'],
            'snow_probability': result['snow_probability'],
            'temperature': current['temperature'],
            'humidity': current['humidity'],
            'cloud_cover': current['cloud_cover'],
            'description': current.get('description', ''),
            'message': message,
            'data_source': 'Kosovo Climate Dataset (58 historical days)'
        })
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def predict_week(request):
    """Predict rain and snow for Monday to Friday using real forecast data"""
    try:
        # Get real 5-day forecast for Kosovo
        forecasts = weather_service.get_forecast()
        
        predictions = []
        for forecast in forecasts:
            result = predictor.predict(
                forecast['temperature'],
                forecast['humidity'],
                forecast['pressure'],
                forecast['wind_speed'],
                forecast['cloud_cover']
            )
            
            predictions.append({
                'day': forecast['day'],
                'date': forecast['date'],
                'will_rain': result['will_rain'],
                'rain_probability': result['rain_probability'],
                'will_snow': result['will_snow'],
                'snow_probability': result['snow_probability'],
                'temperature': forecast['temperature'],
                'humidity': forecast['humidity'],
                'cloud_cover': forecast['cloud_cover'],
                'description': forecast.get('description', '')
            })
        
        return Response({
            'predictions': predictions,
            'location': 'Pristina, Kosovo',
            'generated_at': '2026-01-12',
            'data_source': 'Kosovo Climate Dataset (58 historical days)'
        })
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def health_check(request):
    """Health check endpoint"""
    return Response({'status': 'ok', 'message': 'Weather API is running'})
