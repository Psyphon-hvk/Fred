from django.urls import path
from .views import home, symptom_form, records, delete_record, prediction_result, results, predictor

urlpatterns = [
    path('', home, name='home'),  
    path('log-symptoms/', symptom_form, name='symptom_form'),  
    path('records/', records, name='records'),  
    path('records/delete/<int:record_id>/', delete_record, name='delete_record'),  
    path('result/', prediction_result, name='prediction_result'),  
    path('prediction/results/', results, name='results'),  
    path('predictor/', predictor, name='predictor'),
]
