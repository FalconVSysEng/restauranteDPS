from django import forms
from django.utils import timezone
from datetime import timedelta, time
from .models import Cliente
from .models import Reserva

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
            'tipo_cliente', 'dni', 'ruc', 'nombres', 'apellidos',
            'razon_social', 'telefono', 'correo', 'direccion', 'estado'
        ]
        widgets = {
            'tipo_cliente': forms.Select(attrs={'class': 'form-control'}),
            'dni': forms.TextInput(attrs={'class': 'form-control'}),
            'ruc': forms.TextInput(attrs={'class': 'form-control'}),
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'razon_social': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}), 
        }

    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo_cliente')
        dni = (cleaned_data.get('dni') or '').strip()
        ruc = (cleaned_data.get('ruc') or '').strip()
        nombres = (cleaned_data.get('nombres') or '').strip()
        apellidos = (cleaned_data.get('apellidos') or '').strip()
        razon_social = (cleaned_data.get('razon_social') or '').strip()
        telefono = (cleaned_data.get('telefono') or '').strip()

        if tipo == 'persona':
            if not dni:
                raise forms.ValidationError("Para clientes persona, debe completar el DNI.")
            if not nombres:
                raise forms.ValidationError("Para clientes persona, debe completar los nombres.")
            if not apellidos:
                raise forms.ValidationError("Para clientes persona, debe completar los apellidos.")
            if not dni.isdigit() or len(dni) != 8:
                raise forms.ValidationError("El DNI debe tener exactamente 8 dígitos numéricos.")

        elif tipo == 'empresa':
            if not ruc:
                raise forms.ValidationError("Para clientes empresa, debe completar el RUC.")
            if not razon_social:
                raise forms.ValidationError("Para clientes empresa, debe completar la razón social.")
            if not ruc.isdigit() or len(ruc) != 11:
                raise forms.ValidationError("El RUC debe tener exactamente 11 dígitos numéricos.")

        # validación del teléfono para ambos tipos
        if telefono:
            if not telefono.isdigit() or len(telefono) != 9:
                raise forms.ValidationError("El teléfono debe tener exactamente 9 dígitos numéricos.")

        return cleaned_data


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['fecha_hora', 'cant_personas']
        widgets = {
            'fecha_hora': forms.DateTimeInput(attrs={
                'type': 'datetime-local', 'class': 'form-control'
            }),
            'cant_personas': forms.NumberInput(attrs={
                'class': 'form-control', 'placeholder': 'Cantidad de personas'
            }),
        }

    def clean_fecha_hora(self):
        fecha_hora = self.cleaned_data.get('fecha_hora')
        ahora = timezone.now()

        if not fecha_hora:
            raise forms.ValidationError("Debe especificar fecha y hora.")

        # No fechas anteriores
        if fecha_hora < ahora:
            raise forms.ValidationError("No se puede reservar en una fecha pasada.")

        # mínimo un día de antelación
        if fecha_hora < (ahora + timedelta(days=1)):
            raise forms.ValidationError("Las reservas deben hacerse al menos con un día de antelación.")

        # rango horario 8:00–21:00
        hora = fecha_hora.time()
        if hora < time(12, 0) or hora > time(21, 0):
            raise forms.ValidationError("Las reservas solo están disponibles entre las 12:00 y las 21:00.")

        return fecha_hora