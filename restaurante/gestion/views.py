from django.shortcuts import render, redirect
from usuarios.models import Usuario
from .models import Plato, Mesa
from reservas.models import Reserva
from django.contrib import messages
from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import PlatoForm, MesaForm


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


@login_required
def home(request):
    usuarios = Usuario.objects.all()
    reservas = Reserva.objects.count()
    platos = Plato.objects.count()
    mesas = Mesa.objects.count()
    return render(request, 'inicio.html', {
        'usuarios': usuarios,
        'reservas': reservas,
        'platos': platos,
        'mesas': mesas,
    })

