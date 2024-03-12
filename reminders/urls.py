from django.urls import path
from . import views

urlpatterns = [
    path('new_reminder/', views.async_add_reminder, name='add_new_reminder_url'),
    path('delete_reminder/<int:reminder_id>', views.async_delete_reminder, name='delete_reminder_url'),
    path('load_reminders/<int:car_id>', views.async_load_reminders_list, name='load_reminders_list_url'),
    path('load_reminder_details/<int:reminder_id>', views.async_load_reminder_details, name='load_reminder_details_url'),
]
