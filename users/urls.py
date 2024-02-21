from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.user_profile, name='profile_page'),
    path('delete_user/', views.delete_user, name='delete_user_url'),
    path('edit_user/', views.edit_user, name='edit_user_url'),
]
