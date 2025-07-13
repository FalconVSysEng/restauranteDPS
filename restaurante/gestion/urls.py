from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name= 'home'),
    path('platos/', views.platos, name='platos'),
    path('platos/nuevo/', views.nuevo_plato, name='nuevo_plato'), 
    path('mesas/', views.mesas, name='mesas'),
    path('mesas/nueva/', views.nueva_mesa, name='nueva_mesa'), 
]