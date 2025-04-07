import requests
import logging
import joblib  # To load the ML model
import numpy as np
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import SymptomRecord
from .forms import SymptomForm

# ✅ Initialize logging for debugging
logger = logging.getLogger(__name__)

# ✅ Load the ML Model
MODEL_PATH = "ml_model/asthma_model.pkl"
try:
    model = joblib.load(MODEL_PATH)
    logger.info("ML model loaded successfully!")
except Exception as e:
    logger.error(f"Error loading ML model: {e}")
    model = None

# ✅ API Key for Weather and Air Quality
API_KEY = "4072e5bec3379cdfdcfe47bd7238a762"
CITY = "Nairobi"

# ✅ Fetch AQI
def get_air_quality(lat, lon):
    try:
        url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
        response = requests.get(url)
        data = response.json()

        logger.info(f"AQI API Response: {data}")
        return data["list"][0]["main"]["aqi"] if "list" in data else None
    except Exception as e:
        logger.error(f"Error fetching AQI: {e}")
        return None

# ✅ Fetch Weather
def get_weather_data(city_name):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        logger.info(f"Weather API Response: {data}")
        return (data["main"]["temp"], data["weather"][0]["description"]) if "main" in data else (None, None)
    except Exception as e:
        logger.error(f"Error fetching weather data: {e}")
        return None, None

# ✅ Home View
def home(request):
    return render(request, "prediction/home.html")

# ✅ Predictor View
def predictor(request):
    lat, lon = -1.286389, 36.817223  # Nairobi coordinates
    air_quality = get_air_quality(lat, lon)
    weather = get_weather_data(CITY)

    return render(request, "prediction/predictor.html", {
        "aqi": air_quality,
        "weather": weather
    })

# ✅ Log Symptoms & Predict Asthma
def symptom_form(request):
    if request.method == "POST":
        form = SymptomForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            age = int(data["age"])
            respiratory_rate = int(data["respiratory_rate"])
            oxygen_saturation = int(data["oxygen_saturation"])

            # Count the symptoms
            symptoms = sum([
                int(data["cough"]),
                int(data["wheezing"]),
                int(data["chest_tightness"]),
                int(data["shortness_of_breath"]),
                int(data["nighttime_symptoms"])
            ])

            # Flags for abnormal vitals
            abnormal_respiratory_rate = (
                (age >= 18 and respiratory_rate > 20) or
                (6 <= age < 18 and respiratory_rate > 30) or
                (age < 6 and respiratory_rate > 40)
            )

            low_oxygen = oxygen_saturation < 92

            # Clinically guided prediction
            if symptoms >= 2 and (abnormal_respiratory_rate or low_oxygen):
                prediction = "Asthma"
            else:
                prediction = "No Asthma"

            # Save record to database
            SymptomRecord.objects.create(
                age=age,
                temperature=data["temperature"],
                respiratory_rate=respiratory_rate,
                heart_rate=data["heart_rate"],
                oxygen_saturation=oxygen_saturation,
                cough=data["cough"],
                wheezing=data["wheezing"],
                chest_tightness=data["chest_tightness"],
                shortness_of_breath=data["shortness_of_breath"],
                nighttime_symptoms=data["nighttime_symptoms"],
                asthma_prediction=prediction
            )
    else:
        form = SymptomForm()

    return render(request, "prediction/symptom_form.html", {"form": form})

# ✅ Records View
def records(request):
    records = SymptomRecord.objects.all().order_by('-created_at')
    return render(request, "prediction/records.html", {"records": records})

# ✅ Delete Symptom Record
def delete_record(request, record_id):
    record = get_object_or_404(SymptomRecord, id=record_id)
    record.delete()
    messages.success(request, "Record deleted successfully!")
    return redirect("records")

# ✅ Results Page (Weather & AQI Data)
def results(request):
    city_name = "Nairobi"
    lat, lon = -1.286389, 36.817223

    aqi = get_air_quality(lat, lon)
    weather = get_weather_data(city_name)

    return render(request, "prediction/results.html", {"aqi": aqi, "weather": weather})

# ✅ Prediction Result View
def prediction_result(request):
    return render(request, "prediction/prediction_result.html")
