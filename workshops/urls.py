from django.urls import path
from . import views

urlpatterns = [
    path('new_workshop/', views.async_add_workshop, name='add_new_workshop_url'),
]
