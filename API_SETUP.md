# Kosovo Weather App - Setup Guide

## Getting Real Weather Data

The app now uses **real weather data** from OpenWeatherMap API for Pristina, Kosovo.

### Step 1: Get a Free API Key

1. Go to https://openweathermap.org/api
2. Click "Sign Up" (it's free!)
3. Verify your email
4. Go to API Keys section
5. Copy your API key

### Step 2: Configure the API Key

#### Option A: Environment Variable (Recommended)
```bash
# Windows PowerShell
$env:OPENWEATHER_API_KEY="your_api_key_here"

# Then start the server
cd task/backend
python manage.py runserver
```

#### Option B: Edit the Code Directly
Open `task/backend/weather_api/weather_service.py` and replace:
```python
self.api_key = os.getenv('OPENWEATHER_API_KEY', 'YOUR_API_KEY_HERE')
```
with:
```python
self.api_key = 'your_actual_api_key_here'
```

### Step 3: Run the Application

Backend:
```bash
cd task/backend
python manage.py runserver
```

Frontend:
```bash
cd task/frontend
npm run dev
```

## Real Data Sources

The app fetches:
- **Current Weather**: Live conditions for Pristina, Kosovo
- **5-Day Forecast**: Actual forecast from OpenWeatherMap
- **Data includes**: Temperature, humidity, pressure, wind speed, cloud cover

## Fallback Mode

If the API key is not set or there's a network issue, the app will use realistic fallback data based on typical Kosovo winter patterns.

## Note

- Free tier provides current weather and 5-day forecast
- Updates every time you refresh the page
- Data is for Pristina, Kosovo (42.6629°N, 21.1655°E)
