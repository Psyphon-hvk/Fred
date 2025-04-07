from django import forms
from .models import SymptomRecord

class SymptomForm(forms.ModelForm):
    class Meta:
        model = SymptomRecord
        fields = ['age', 'temperature', 'respiratory_rate', 'heart_rate', 'oxygen_saturation',
                  'cough', 'wheezing', 'chest_tightness', 'shortness_of_breath', 'nighttime_symptoms']

        widgets = {
            #  Use a Number Input for Age
            'age': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '120', 'required': True}),
            
            'temperature': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'respiratory_rate': forms.NumberInput(attrs={'class': 'form-control'}),
            'heart_rate': forms.NumberInput(attrs={'class': 'form-control'}),
            'oxygen_saturation': forms.NumberInput(attrs={'class': 'form-control'}),

            #  Fix: Explicit Checkbox Widgets
            'cough': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'wheezing': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'chest_tightness': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'shortness_of_breath': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'nighttime_symptoms': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
