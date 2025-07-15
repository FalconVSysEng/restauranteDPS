from django.urls import path
from . import views


urlpatterns = [
    path('', views.reservas, name='reservas'),
    path('nueva/', views.nueva_reserva, name='nueva_reserva'),
    path('disponibilidad/', views.consultar_disponibilidad, name='consultar_disponibilidad'),
    path('seleccionar_mesa/<int:mesa_id>/', views.seleccionar_mesa, name='seleccionar_mesa'),
    path('registrar/', views.registrar_reserva, name='registrar_reserva'),
    path('detalle/<int:reserva_id>/', views.detalle_reserva, name='detalle_reserva'),
    path('obtener_cliente/', views.obtener_cliente, name='obtener_cliente'),
    path("comprobante/<int:reserva_id>/", views.generar_pdf_reserva, name="generar_pdf_reserva"),
    path('cancelar/<int:id>/', views.cancelar_reserva, name='cancelar_reserva'),

        # 👤 CLIENTES
    path('clientes/', views.clientes, name='clientes'),
    path('clientes/nuevo/', views.nuevo_cliente, name='nuevo_cliente'),
    path('clientes/editar/<int:id>/', views.editar_cliente, name='editar_cliente'),
    path('clientes/desactivar/<int:id>/', views.desactivar_cliente, name='desactivar_cliente'),
]