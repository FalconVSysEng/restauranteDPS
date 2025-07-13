from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('gestion.urls')),
    path('login/', views.logear, name='logear'),
    path('logout/', views.cerrar_sesion, name='cerrar_sesion'),
    path('usuarios/', include('usuarios.urls')),
    path('reservas/', include('reservas.urls')),
]
