from django.urls import path
from . import views


urlpatterns = [
    path('platos/', views.platos, name='platos'),
    path('mesas/', views.mesas, name='mesas'),
]