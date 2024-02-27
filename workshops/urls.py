from django.urls import path
from . import views

urlpatterns = [
    path('new_workshop/', views.async_add_workshop, name='add_new_workshop_url'),
    path('workshop_details/<int:workshop_id>/', views.async_load_workshop_details, name='workshop_details_url'),
    path('edit_workshop/<int:workshop_id>/', views.async_edit_workshop, name='edit_workshop_details_url'),
    path('toggle_favourite/<int:workshop_id>/', views.async_toggle_favourite_workshop, name='toggle_favourite_workshop_url'),
    path('load_favourite_workshops/', views.async_load_favourite_workshops_list, name='load_favourite_workshops_list_url'),
    path('load_workshops/', views.async_load_workshops_list, name='load_workshops_list_url'),
    path('delete_workshop/<int:workshop_id>/', views.async_delete_workshop, name='delete_workshop_url'),
    path('refresh_workshop_data/<int:workshop_id>/', views.async_refresh_workshop_data, name='refresh_workshop_data_url'),
]
