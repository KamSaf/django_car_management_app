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
    path('welcome', main_views.welcome, name='welcome_page'),
    path('about', main_views.about, name='about_page'),
    path('register/', user_views.register, name='register_page'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login_page'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout_page'),
    # path('profile/', user_views.profile, name='profile'),
    path('', include('cars.urls')),
    # path('', include('users.urls')),
    # path('', include('enties.urls')),
    # path('', include('workshops.urls')),
    # path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout')
]
