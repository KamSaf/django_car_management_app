from django.urls import path
from . import views

urlpatterns = [
    path('new_car/', views.add_new_car, name='add_new_car'),
]
