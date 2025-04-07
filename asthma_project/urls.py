from django.contrib import admin
from django.urls import path, include
from prediction import views  # Import the home view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # Make sure this line is present
    path('prediction/', include('prediction.urls')),  # Include app URLs
]
