from django.db import models
from usuarios.models import Usuario
from gestion.models import Plato, Mesa

class Cliente(models.Model):
    TIPO_CLIENTE_CHOICES = [
        ('persona', 'Persona'),
        ('empresa', 'Empresa'),
    ]
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]

    tipo_cliente = models.CharField(max_length=10, choices=TIPO_CLIENTE_CHOICES, default='persona')
    dni = models.CharField(max_length=8, null=True, blank=True) 
    ruc = models.CharField(max_length=11, null=True, blank=True)
    nombres = models.CharField(max_length=100, null=True, blank=True)
    apellidos = models.CharField(max_length=100, null=True, blank=True)
    razon_social = models.CharField(max_length=200, null=True, blank=True)
    telefono = models.CharField(max_length=9, null=True, blank=True)
    correo = models.EmailField(null=True, blank=True)
    direccion = models.TextField(null=True, blank=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='activo')

    def __str__(self):
        if self.tipo_cliente == 'persona':
            return f"{self.nombres} {self.apellidos}"
        else:
            return f"{self.razon_social}"


class Reserva(models.Model):
    METODO_PAGO_CHOICES = [
        ('Efectivo', 'Efectivo'),
        ('Tarjeta de débito', 'Tarjeta de débito'),
        ('Tarjeta de crédito', 'Tarjeta de crédito'),
        ('Yape/Plin', 'Yape/Plin'),
    ]
    ESTADO_RESERVA_CHOICES = [
        ('confirmada', 'Confirmada'),
        ('en_curso', 'En curso'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
        ('no_asistio', 'No asistió'),
    ]
    fecha_hora = models.DateTimeField()
    cant_personas = models.PositiveIntegerField()
    metodo_pago = models.CharField(max_length=50, choices=METODO_PAGO_CHOICES)
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_RESERVA_CHOICES,
        default='confirmada'
    )
    tipo = models.CharField(max_length=50)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    empleado = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)
    mesa = models.ForeignKey('gestion.Mesa', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Reserva {self.id} - {self.fecha_hora}"

class DetalleReserva(models.Model):
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE)
    plato = models.ForeignKey(Plato, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    monto = models.DecimalField(max_digits=10, decimal_places=2, default=0)  

    def save(self, *args, **kwargs):
        self.monto = self.cantidad * self.plato.precio
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.cantidad} x {self.plato.nombre} (Reserva {self.reserva.id})"  
