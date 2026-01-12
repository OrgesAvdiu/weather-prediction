'use client';

import { useState, useEffect } from 'react';

interface TodayWeather {
  day: string;
  date: string;
  will_rain: boolean;
  rain_probability: number;
  will_snow: boolean;
  snow_probability: number;
  temperature: number;
  humidity: number;
  cloud_cover: number;
  message: string;
}

interface WeekPrediction {
  day: string;
  date: string;
  will_rain: boolean;
  rain_probability: number;
  will_snow: boolean;
  snow_probability: number;
  temperature: number;
  humidity: number;
  cloud_cover: number;
}

export default function Home() {
  const [todayWeather, setTodayWeather] = useState<TodayWeather | null>(null);
  const [weekWeather, setWeekWeather] = useState<WeekPrediction[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showWeek, setShowWeek] = useState(false);

  useEffect(() => {
    fetchTodayWeather();
  }, []);

  const fetchTodayWeather = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/weather/today/');
      if (!response.ok) throw new Error('Failed to fetch weather data');
      const data = await response.json();
      setTodayWeather(data);
      setLoading(false);
    } catch (err) {
      setError('Unable to connect to weather service. Make sure the backend is running.');
      setLoading(false);
    }
  };

  const fetchWeekWeather = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/weather/week/');
      if (!response.ok) throw new Error('Failed to fetch weekly weather data');
      const data = await response.json();
      setWeekWeather(data.predictions);
      setShowWeek(true);
    } catch (err) {
      setError('Unable to fetch weekly forecast');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-400 via-blue-500 to-blue-600 p-8">
      <div className="max-w-4xl mx-auto">
        <header className="text-center mb-12">
          <h1 className="text-5xl font-bold text-white mb-2">Kosovo Weather</h1>
          <p className="text-blue-100 text-lg">Rain Prediction System</p>
        </header>

        {loading && (
          <div className="text-center text-white text-xl">
            <div className="animate-pulse">Loading weather data...</div>
          </div>
        )}

        {error && (
          <div className="bg-red-500 text-white p-4 rounded-lg mb-6">
            {error}
          </div>
        )}

        {todayWeather && !loading && (
          <div className="bg-white rounded-2xl shadow-2xl p-8 mb-8">
            <div className="text-center mb-6">
              <h2 className="text-3xl font-bold text-gray-800 mb-2">Today - {todayWeather.day}</h2>
              <p className="text-gray-600">{todayWeather.date}</p>
            </div>

            <div className="flex items-center justify-center mb-8">
              {todayWeather.will_snow ? (
                <div className="text-center">
                  <div className="text-8xl mb-4">❄️</div>
                  <p className="text-2xl font-semibold text-blue-600">Snow Expected</p>
                  <p className="text-gray-600 mt-2">{(todayWeather.snow_probability * 100).toFixed(0)}% chance</p>
                </div>
              ) : todayWeather.will_rain ? (
                <div className="text-center">
                  <div className="text-8xl mb-4">🌧️</div>
                  <p className="text-2xl font-semibold text-blue-600">Rain Expected</p>
                  <p className="text-gray-600 mt-2">{(todayWeather.rain_probability * 100).toFixed(0)}% chance</p>
                </div>
              ) : (
                <div className="text-center">
                  <div className="text-8xl mb-4">☀️</div>
                  <p className="text-2xl font-semibold text-yellow-600">No Rain or Snow</p>
                  <p className="text-gray-600 mt-2">Clear weather expected</p>
                </div>
              )}
            </div>

            <div className="grid grid-cols-3 gap-4 mb-6">
              <div className="bg-blue-50 p-4 rounded-lg text-center">
                <p className="text-gray-600 text-sm">Temperature</p>
                <p className="text-2xl font-bold text-blue-600">{todayWeather.temperature}°C</p>
              </div>
              <div className="bg-blue-50 p-4 rounded-lg text-center">
                <p className="text-gray-600 text-sm">Humidity</p>
                <p className="text-2xl font-bold text-blue-600">{todayWeather.humidity}%</p>
              </div>
              <div className="bg-blue-50 p-4 rounded-lg text-center">
                <p className="text-gray-600 text-sm">Cloud Cover</p>
                <p className="text-2xl font-bold text-blue-600">{todayWeather.cloud_cover}%</p>
              </div>
            </div>

            <button
              onClick={fetchWeekWeather}
              className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition duration-200"
            >
              {showWeek ? 'Refresh' : 'Show'} 5-Day Forecast (Mon-Fri)
            </button>
          </div>
        )}

        {showWeek && weekWeather.length > 0 && (
          <div className="bg-white rounded-2xl shadow-2xl p-8">
            <h3 className="text-2xl font-bold text-gray-800 mb-6 text-center">Weekly Forecast</h3>
            <div className="grid gap-4">
              {weekWeather.map((day, index) => (
                <div
                  key={index}
                  className={`border-2 rounded-lg p-4 ${
                    day.will_snow ? 'border-cyan-300 bg-cyan-50' : day.will_rain ? 'border-blue-300 bg-blue-50' : 'border-yellow-300 bg-yellow-50'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex-1">
                      <h4 className="font-bold text-lg text-gray-800">{day.day}</h4>
                      <p className="text-sm text-gray-600">{day.date}</p>
                    </div>
                    <div className="text-5xl mx-4">
                      {day.will_snow ? '❄️' : day.will_rain ? '🌧️' : '☀️'}
                    </div>
                    <div className="flex-1 text-right">
                      <p className="font-semibold text-gray-800">
                        {day.will_snow ? 'Snow' : day.will_rain ? 'Rain' : 'Clear'}
                      </p>
                      <p className="text-sm text-gray-600">
                        {day.will_snow 
                          ? `${(day.snow_probability * 100).toFixed(0)}% snow` 
                          : day.will_rain 
                          ? `${(day.rain_probability * 100).toFixed(0)}% rain`
                          : 'No precipitation'}
                      </p>
                      <p className="text-sm text-gray-600 mt-1">
                        {day.temperature}°C | {day.humidity}% humidity
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
