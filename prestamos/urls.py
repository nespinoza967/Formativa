from django.urls import path

from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('encargado/', views.panel_encargado, name='panel_encargado'),
]
