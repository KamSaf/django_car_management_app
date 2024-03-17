from django.urls import path
from . import views

urlpatterns = [
    path('<int:car_id>/', views.render_graphs, name='render_graphs'),
]
