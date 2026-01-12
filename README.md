# Kosovo Weather Prediction App

A full-stack weather prediction application that predicts rain for Kosovo using machine learning.

## Features
- Predicts if it will rain today (Monday, January 12, 2026)
- 5-day forecast (Monday-Friday)
- Machine learning model trained on Kosovo weather data
- Beautiful, responsive UI

## Tech Stack
- **Backend**: Django + Django REST Framework
- **Frontend**: Next.js + TypeScript + Tailwind CSS
- **ML**: scikit-learn (Random Forest Classifier)

## Setup Instructions

### Backend (Django)

1. Navigate to the backend directory:
```bash
cd task/backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the Django server:
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/weather/`

API Endpoints:
- `GET /api/weather/today/` - Get today's rain prediction
- `GET /api/weather/week/` - Get 5-day forecast (Mon-Fri)
- `GET /api/weather/health/` - Health check

### Frontend (Next.js)

1. Navigate to the frontend directory:
```bash
cd task/frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

The app will be available at `http://localhost:3000`

## Dataset

The app uses `kosovo_weather_data.csv` with the following features:
- date
- temperature (°C)
- humidity (%)
- pressure (hPa)
- wind_speed (km/h)
- cloud_cover (%)
- rain (0 = no rain, 1 = rain)

## Usage

1. Start the Django backend server (port 8000)
2. Start the Next.js frontend (port 3000)
3. Open your browser to `http://localhost:3000`
4. View today's rain prediction
5. Click "Show 5-Day Forecast" to see predictions for Monday through Friday
