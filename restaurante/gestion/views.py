from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from usuarios.models import Usuario
from .models import Plato, Mesa
from reservas.models import Reserva, Cliente
from .forms import PlatoForm, MesaForm, ClienteForm


def platos(request):
    platos = Plato.objects.all()
    return render(request, 'platos.html', {'platos': platos})

def nuevo_plato(request):
    form = PlatoForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            plato = form.save(commit=False)
            plato.save()
            messages.success(request, 'Plato creado exitosamente')
            return redirect('platos')
        else:
            messages.error(request, 'Error al crear el plato. Por favor, revisa los datos ingresados.')
    return render(request, 'formsplato.html', {'form': form, 'accion': 'Crear'})


def mesas(request):
    mesas = Mesa.objects.all()
    return render(request, 'mesas.html', {'mesas': mesas})

def nueva_mesa(request):
    form = MesaForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            mesa = form.save(commit=False)
            mesa.save()
            messages.success(request, 'Mesa creada exitosamente')
            return redirect('mesas')
        else:
            messages.error(request, 'Error al crear la mesa. Por favor, revisa los datos ingresados.')
    return render(request, 'formsmesa.html', {'form': form, 'accion': 'Crear'})

# Editar Plato
def editar_plato(request, id):
    plato = Plato.objects.get(id=id)
    form = PlatoForm(request.POST or None, instance=plato)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Plato actualizado correctamente')
            return redirect('platos')
        else:
            messages.error(request, 'Error al actualizar el plato.')
    return render(request, 'formsplato.html', {'form': form, 'accion': 'Editar'})

# Eliminar Plato
def eliminar_plato(request, id):
    plato = Plato.objects.get(id=id)
    plato.delete()
    messages.success(request, 'Plato eliminado correctamente')
    return redirect('platos')

def desactivar_plato(request, id):
    plato = get_object_or_404(Plato, id=id)
    plato.estado = 'inactivo'
    plato.save()
    messages.success(request, 'Plato desactivado correctamente')
    return redirect('platos')


# Editar Mesa
def editar_mesa(request, id):
    mesa = Mesa.objects.get(id=id)
    form = MesaForm(request.POST or None, instance=mesa)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Mesa actualizada correctamente')
            return redirect('mesas')
        else:
            messages.error(request, 'Error al actualizar la mesa.')
    return render(request, 'formsmesa.html', {'form': form, 'accion': 'Editar'})

# Eliminar Mesa
def eliminar_mesa(request, id):
    mesa = Mesa.objects.get(id=id)
    mesa.delete()
    messages.success(request, 'Mesa eliminada correctamente')
    return redirect('mesas')

def desactivar_mesa(request, id):
    mesa = get_object_or_404(Mesa, id=id)
    mesa.estado = 'inactivo'
    mesa.save()
    messages.success(request, 'Mesa desactivado correctamente')
    return redirect('mesas')


@login_required
def home(request):
    usuarios = Usuario.objects.all()
    reservas = Reserva.objects.filter(
        fecha_hora__gt=timezone.now()
    ).count()
    platos = Plato.objects.count()
    mesas = Mesa.objects.count()
    return render(request, 'inicio.html', {
        'usuarios': usuarios,
        'reservas': reservas,
        'platos': platos,
        'mesas': mesas,
    })

