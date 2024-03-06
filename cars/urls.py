from django.urls import path
from . import views

urlpatterns = [
    path('new_car/', views.add_new_car, name='add_new_car'),
    path('toggle_favourite_car/', views.async_toggle_favourite_car, name='toggle_favourite_car_url'),
]
