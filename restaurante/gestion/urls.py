from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # 🧑‍🍳 PLATOS
    path('platos/', views.platos, name='platos'),
    path('platos/nuevo/', views.nuevo_plato, name='nuevo_plato'),
    path('platos/editar/<int:id>/', views.editar_plato, name='editar_plato'),
    path('platos/desactivar/<int:id>/', views.desactivar_plato, name='desactivar_plato'),

    # 🍽 MESAS
    path('mesas/', views.mesas, name='mesas'),
    path('mesas/nueva/', views.nueva_mesa, name='nueva_mesa'),
    path('mesas/editar/<int:id>/', views.editar_mesa, name='editar_mesa'),
    path('mesas/desactivar/<int:id>/', views.desactivar_mesa, name='desactivar_mesa'),


]
