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


class ReservaForm(forms.Form):
    fecha = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    hora = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    cant_personas = forms.IntegerField(min_value=1)