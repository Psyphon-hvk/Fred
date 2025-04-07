from django.db import models

class SymptomRecord(models.Model):
    age = models.CharField(max_length=20)  # Store selected age range
    temperature = models.FloatField()
    respiratory_rate = models.IntegerField()
    heart_rate = models.IntegerField()
    oxygen_saturation = models.IntegerField()
    
    # Symptoms (Boolean fields)
    cough = models.BooleanField(default=False)
    wheezing = models.BooleanField(default=False)
    chest_tightness = models.BooleanField(default=False)
    shortness_of_breath = models.BooleanField(default=False)
    nighttime_symptoms = models.BooleanField(default=False)
    
    # Prediction result
    asthma_prediction = models.CharField(max_length=10, choices=[("Asthma", "Asthma"), ("No Asthma", "No Asthma")])

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Record {self.id} - {self.created_at.strftime('%Y-%m-%d')} - Asthma: {'Yes' if self.asthma_prediction else 'No'}"
