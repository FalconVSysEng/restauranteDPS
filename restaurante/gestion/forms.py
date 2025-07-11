from django import forms
from .models import Plato, Mesa

# Plato
class PlatoForm(forms.ModelForm):
    class Meta:
        model = Plato
        fields = ['nombre', 'descripcion', 'tipo']

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if len(nombre) < 3:
            raise forms.ValidationError("El nombre del plato debe tener al menos 3 caracteres.")
        return nombre

    def clean_tipo(self):
        tipo = self.cleaned_data.get('tipo')
        if not tipo:
            raise forms.ValidationError("Debe especificar el tipo del plato.")
        return tipo


# Mesa
class MesaForm(forms.ModelForm):
    class Meta:
        model = Mesa
        fields = ['capacidad', 'ubicacion']

    def clean_capacidad(self):
        capacidad = self.cleaned_data.get('capacidad')
        if capacidad <= 0:
            raise forms.ValidationError("La capacidad de la mesa debe ser mayor a cero.")
        return capacidad

    def clean_ubicacion(self):
        ubicacion = self.cleaned_data.get('ubicacion')
        if not ubicacion:
            raise forms.ValidationError("Debe especificar la ubicación de la mesa.")
        return ubicacion
