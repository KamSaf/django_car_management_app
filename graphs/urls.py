from django.urls import path
from . import views

urlpatterns = [
    path('<str:graph>/<int:car_id>/', views.render_graphs, name='render_graphs'),
]
