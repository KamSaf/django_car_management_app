"""
URL configuration for car_management_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views as main_views
from users import views as user_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_views.welcome, name='welcome_page'),
    path('home/<int:car_id>/', main_views.home, name='home_page'),
    path('home/', main_views.home, name='home_page'),
    path('about', main_views.about, name='about_page'),
    path('register/', user_views.register, name='register_page'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login_page'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout_url'),
    path('cars/', include('cars.urls')),
    path('users/', include('users.urls')),
    path('entries/', include('entries.urls')),
    path('workshops/', include('workshops.urls')),
    path('reminders/', include('reminders.urls')),
    path('cron/', include('cronjob.urls')),
    path('graphs/', include('graphs.urls')),
    path('navbar_refresh/', main_views.refresh_navbar, name="navbar_refresh_url"),
    path('reports_refresh/<int:car_id>/', main_views.refresh_month_reports, name="navbar_refresh_url"),
]
