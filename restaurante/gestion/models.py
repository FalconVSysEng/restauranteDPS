from django.db import models


class Plato(models.Model):
    TIPO_CHOICES = [
        ('Entrada', 'Entrada'),
        ('Fondo', 'Fondo'),
        ('Bebida', 'Bebida'),
        ('Postre', 'Postre'),
    ]
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='activo')
    def __str__(self):
        return self.nombre


class Mesa(models.Model):
    UBICACION_CHOICES = [
        ('Piso1', 'Piso1'),
        ('Piso2', 'Piso2'),
        ('Terraza', 'Terraza'),
    ]
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]
    capacidad = models.IntegerField()
    ubicacion = models.CharField(max_length=100, choices=UBICACION_CHOICES)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='activo')

    def __str__(self):
        return f"Mesa {self.id} - {self.ubicacion}"


