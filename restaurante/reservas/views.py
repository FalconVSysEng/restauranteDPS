from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import ValidationError
from .models import Reserva, DetalleReserva, Cliente
from gestion.models import Plato, Mesa
from .forms import ReservaForm, ClienteForm
from datetime import datetime
from django.db import transaction

def reservas(request):
    reservas = Reserva.objects.all()
    return render(request, 'reservas.html', {'reservas': reservas})

def nueva_reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():

            datos = form.cleaned_data
            fecha_hora = datos['fecha_hora']

            reserva_data = {
                'fecha': fecha_hora.date().isoformat(),  # "2025-07-13"
                'hora': fecha_hora.time().strftime("%H:%M"),    # "14:30"
                'cant_personas': datos['cant_personas']
            }
            request.session['reserva'] = reserva_data # Guarda datos en sesión
            return redirect('consultar_disponibilidad')
    else:
        form = ReservaForm()
    return render(request, 'nueva_reserva.html', {'form': form})

def consultar_disponibilidad(request):
    datos = request.session.get('reserva')
    fecha_hora = datetime.strptime(
        f"{datos['fecha']} {datos['hora']}",
        "%Y-%m-%d %H:%M"   
    )
    if not datos:
        return redirect('nueva_reserva')
    cant = datos['cant_personas']
    mesas_ocupadas = Reserva.objects.filter(fecha_hora=fecha_hora).values_list('mesa_id', flat=True)
    mesas_disponibles = Mesa.objects.filter(capacidad__gte=cant).exclude(id__in=mesas_ocupadas)

    return render(request, 'disponibilidad.html', {
        'mesas': mesas_disponibles,
        'fecha_hora': fecha_hora,
        'cant_personas': cant
    })


def seleccionar_mesa(request, mesa_id):
    reserva = request.session.get('reserva')
    if not reserva:
        return redirect('nueva_reserva') 

    reserva['mesa_id'] = mesa_id
    request.session['reserva'] = reserva 
    platos = Plato.objects.all()
    return render(request, 'seleccionar_datos.html', {'platos': platos})

@transaction.atomic
def registrar_reserva(request):
    if request.method == 'POST':
        datos_reserva = request.session.get('reserva')
        # 🔐 Verificamos que exista la sesión
        if not datos_reserva:
            messages.error(request, "No hay datos de la reserva. Inicia nuevamente el proceso.")
            return redirect('nueva_reserva')

        mesa_id = datos_reserva.get('mesa_id')
        if not mesa_id:
            messages.error(request, "No se seleccionó ninguna mesa.")
            return redirect('consultar_disponibilidad')

        mesa = get_object_or_404(Mesa, id=mesa_id)
        fecha_hora = datetime.strptime(f"{datos_reserva['fecha']} {datos_reserva['hora']}", "%Y-%m-%d %H:%M")
        cant = datos_reserva['cant_personas']

        # Datos del cliente desde POST
        tipo_cliente = request.POST.get('tipo_cliente')
        dni = (request.POST.get('dni') or '').strip()
        ruc = (request.POST.get('ruc') or '').strip()
        nombres = (request.POST.get('nombres') or '').strip()
        apellidos = (request.POST.get('apellidos') or '').strip()
        razon_social = (request.POST.get('razon_social') or '').strip()
        telefono = (request.POST.get('telefono') or '').strip()
        correo = (request.POST.get('correo') or '').strip()
        direccion = (request.POST.get('direccion') or '').strip()

        # intenta buscar cliente existente
        cliente = None
        if dni:
            cliente = Cliente.objects.filter(dni=dni).first()
        if not cliente and ruc:
            cliente = Cliente.objects.filter(ruc=ruc).first()

        if cliente:
            pass
        else:
            if tipo_cliente == 'persona':
                if not dni:
                    raise ValidationError("Debe ingresar el DNI.")
                if not nombres:
                    raise ValidationError("Debe ingresar los nombres.")
                if not apellidos:
                    raise ValidationError("Debe ingresar los apellidos.")
                if not dni.isdigit() or len(dni) != 8:
                    raise ValidationError("El DNI debe tener exactamente 8 dígitos.")
            elif tipo_cliente == 'empresa':
                if not ruc:
                    raise ValidationError("Debe ingresar el RUC.")
                if not razon_social:
                    raise ValidationError("Debe ingresar la razón social.")
                if not ruc.isdigit() or len(ruc) != 11:
                    raise ValidationError("El RUC debe tener exactamente 11 dígitos.")

            # validar teléfono si lo envían
            if telefono and not telefono.isdigit():
                raise ValidationError("El teléfono debe contener solo números.")

            # crear cliente porque no existía
            cliente = Cliente.objects.create(
                tipo_cliente=tipo_cliente,
                dni=dni if dni else None,
                ruc=ruc if ruc else None,
                nombres=nombres,
                apellidos=apellidos,
                razon_social=razon_social,
                telefono=telefono,
                correo=correo,
                direccion=direccion
            )

        reserva = Reserva.objects.create(
            fecha_hora=fecha_hora,
            cant_personas=cant,
            metodo_pago='Pendiente',
            estado='Pendiente',
            tipo='En restaurante',
            total=0, 
            cliente=cliente,
            empleado=request.user,
            mesa=mesa
        )

        # Carrito
        total = 0
        for key, value in request.POST.items():
            if key.startswith('plato_'):
                plato_id = int(key.split('_')[1])
                cantidad = int(value)
                if cantidad > 0:
                    plato = get_object_or_404(Plato, id=plato_id)
                    DetalleReserva.objects.create(
                        reserva=reserva,
                        plato=plato,
                        cantidad=cantidad
                    )
                    total += cantidad * plato.precio 

        reserva.total = total
        reserva.save()
        del request.session['reserva']

        return redirect('reservas')
    else:
        return redirect('nueva_reserva')
    
def clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes.html', {'clientes': clientes})

def nuevo_cliente(request):
    form = ClienteForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.save()
            messages.success(request, 'Cliente creado exitosamente')
            return redirect('clientes')
        else:
            messages.error(request, 'Error al crear el cliente. Por favor, revisa los datos ingresados.')
    return render(request, 'formscliente.html', {'form': form, 'accion': 'Crear'})

def detalle_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    detalles = DetalleReserva.objects.filter(reserva=reserva)
    return render(request, 'detalle_reserva.html', {
        'reserva': reserva,
        'detalles': detalles
    })