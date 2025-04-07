import requests
from django.conf import settings

API_KEY = settings.OPENWEATHER_API_KEY

def get_air_quality(lat, lon):
    try:
        url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
        response = requests.get(url)
        data = response.json()
        
        print("AQI API Response:", data)  # Debugging output
        
        if "list" in data:
            aqi = data["list"][0]["main"]["aqi"]
            return aqi
        else:
            return None
    except Exception as e:
        print(f"Error fetching AQI: {e}")
        return None

def get_weather_data(city_name):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        print("Weather API Response:", data)  # Debugging output

        if "main" in data:
            temperature = data["main"]["temp"]
            weather_description = data["weather"][0]["description"]
            return temperature, weather_description
        else:
            return None, None
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return None, None
