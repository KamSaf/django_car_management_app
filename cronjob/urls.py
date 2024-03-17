from django.urls import path
from . import views

urlpatterns = [
    path('refresh_fuel_prices/', views.async_refresh_fuel_prices, name='refresh_fuel_prices'),
]
