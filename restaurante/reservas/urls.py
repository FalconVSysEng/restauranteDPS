from django.urls import path
from . import views


urlpatterns = [
    path('', views.reservas, name='reservas'),
    path('nueva/', views.nueva_reserva, name='nueva_reserva'),
    path('disponibilidad/', views.consultar_disponibilidad, name='consultar_disponibilidad'),
    path('seleccionar_mesa/<int:mesa_id>/', views.seleccionar_mesa, name='seleccionar_mesa'),
    path('registrar/', views.registrar_reserva, name='registrar_reserva'),
]