from django.urls import path
from . import views

urlpatterns = [
    path('today/', views.predict_today, name='predict_today'),
    path('week/', views.predict_week, name='predict_week'),
    path('health/', views.health_check, name='health_check'),
]
