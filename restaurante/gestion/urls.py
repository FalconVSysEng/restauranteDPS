from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # 🧑‍🍳 PLATOS
    path('platos/', views.platos, name='platos'),
    path('platos/nuevo/', views.nuevo_plato, name='nuevo_plato'),
    path('platos/editar/<int:id>/', views.editar_plato, name='editar_plato'),
    path('platos/eliminar/<int:id>/', views.eliminar_plato, name='eliminar_plato'),

    # 🍽 MESAS
    path('mesas/', views.mesas, name='mesas'),
    path('mesas/nueva/', views.nueva_mesa, name='nueva_mesa'),
    path('mesas/editar/<int:id>/', views.editar_mesa, name='editar_mesa'),
    path('mesas/eliminar/<int:id>/', views.eliminar_mesa, name='eliminar_mesa'),

    # 👤 CLIENTES
    path('clientes/', views.clientes, name='clientes'),
    path('clientes/nuevo/', views.nuevo_cliente, name='nuevo_cliente'),
    path('clientes/editar/<int:id>/', views.editar_cliente, name='editar_cliente'),
    path('clientes/eliminar/<int:id>/', views.eliminar_cliente, name='eliminar_cliente'),
]
