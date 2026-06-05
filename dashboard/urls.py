from django.urls import path
from . import views

urlpatterns = [
    path('', views.accueil, name='dashboard_accueil'),
    path('api/stats/', views.dashboard_api, name='dashboard_api'),
]
