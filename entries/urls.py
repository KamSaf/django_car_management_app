from django.urls import path
from . import views

urlpatterns = [
    path('entry/', views.async_add_entry, name='add_new_entry_url'),
]
