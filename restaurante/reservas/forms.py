from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
            'tipo_cliente', 'dni', 'ruc', 'nombres', 'apellidos',
            'razon_social', 'telefono', 'correo', 'direccion'
        ]

    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo_cliente')
        dni = cleaned_data.get('dni')
        ruc = cleaned_data.get('ruc')
        nombres = cleaned_data.get('nombres')
        apellidos = cleaned_data.get('apellidos')
        razon_social = cleaned_data.get('razon_social')

        if tipo == 'persona':
            if not (dni and nombres and apellidos):
                raise forms.ValidationError("Para clientes persona, debe completar DNI, nombres y apellidos.")
            if len(dni) != 8 or not dni.isdigit():
                raise forms.ValidationError("El DNI debe tener 8 dígitos numéricos.")
        elif tipo == 'empresa':
            if not (ruc and razon_social):
                raise forms.ValidationError("Para clientes empresa, debe completar RUC y razón social.")
            if len(ruc) != 11 or not ruc.isdigit():
                raise forms.ValidationError("El RUC debe tener 11 dígitos numéricos.")
