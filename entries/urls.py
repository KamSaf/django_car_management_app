from django.urls import path
from . import views

urlpatterns = [
    path('entry/', views.async_add_entry, name='add_new_entry_url'),
    path('load_entries/', views.async_load_entries_list, name='load_entries_list_url'),
    path('load_entry_details/<int:entry_id>', views.async_load_entry_details, name='load_entry_details_url'),
]
