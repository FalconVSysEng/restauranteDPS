from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import ValidationError
from datetime import datetime
from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import Reserva, DetalleReserva, Cliente
from gestion.models import Plato, Mesa
from .forms import ReservaForm, ClienteForm


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
    mesas_disponibles = Mesa.objects.filter(estado='activo',capacidad__gte=cant).exclude(id__in=mesas_ocupadas)

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
    platos = Plato.objects.filter(estado=True)
    return render(request, 'seleccionar_datos.html', {'platos': platos})

@transaction.atomic
def registrar_reserva(request):
    if request.method == 'POST':
        datos_reserva = request.session.get('reserva')
        if not datos_reserva:
            messages.error(request, "No hay datos de la reserva. Inicia nuevamente el proceso.")
            return redirect('nueva_reserva')

        mesa_id = datos_reserva.get('mesa_id')
        if not mesa_id:
            messages.error(request, "No se seleccionó ninguna mesa.")
            return redirect('consultar_disponibilidad')

        mesa = get_object_or_404(Mesa, id=mesa_id)

        try:
            fecha_hora = datetime.strptime(
                f"{datos_reserva['fecha']} {datos_reserva['hora']}",
                "%Y-%m-%d %H:%M"
            )
        except ValueError:
            messages.error(request, "La fecha u hora no tienen un formato válido.")
            return redirect('nueva_reserva')

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

        metodo_pago = request.POST.get('metodo_pago')

        cliente = None
        if dni:
            cliente = Cliente.objects.filter(dni=dni).first()
        if not cliente and ruc:
            cliente = Cliente.objects.filter(ruc=ruc).first()

        if not cliente:
            # validaciones
            if tipo_cliente == 'persona':
                if not dni:
                    messages.error(request, "Debe ingresar el DNI.")
                    return redirect('consultar_disponibilidad')
                if not nombres:
                    messages.error(request, "Debe ingresar los nombres.")
                    return redirect('consultar_disponibilidad')
                if not apellidos:
                    messages.error(request, "Debe ingresar los apellidos.")
                    return redirect('consultar_disponibilidad')
                if not dni.isdigit() or len(dni) != 8:
                    messages.error(request, "El DNI debe tener exactamente 8 dígitos.")
                    return redirect('consultar_disponibilidad')
            elif tipo_cliente == 'empresa':
                if not ruc:
                    messages.error(request, "Debe ingresar el RUC.")
                    return redirect('consultar_disponibilidad')
                if not razon_social:
                    messages.error(request, "Debe ingresar la razón social.")
                    return redirect('consultar_disponibilidad')
                if not ruc.isdigit() or len(ruc) != 11:
                    messages.error(request, "El RUC debe tener exactamente 11 dígitos.")
                    return redirect('consultar_disponibilidad')

            if telefono and not telefono.isdigit():
                messages.error(request, "El teléfono debe contener solo números.")
                return redirect('consultar_disponibilidad')

            cliente = Cliente.objects.create(
                tipo_cliente=tipo_cliente,
                dni=dni or None,
                ruc=ruc or None,
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
            metodo_pago=metodo_pago,
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

        # limpiar la sesión
        del request.session['reserva']

        messages.success(request, "✅ La reserva se registró correctamente.")
        return redirect('reservas')

    return redirect('nueva_reserva')

def generar_pdf_reserva(request, reserva_id):
    reserva = Reserva.objects.get(pk=reserva_id)
    detalles = reserva.detallereserva_set.all()

    template = get_template("comprobante_reserva.html")
    html = template.render({"reserva": reserva, "detalles": detalles})

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f"attachment; filename=comprobante_reserva_{reserva.id}.pdf"

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse("Error al generar el PDF", status=500)
    return response


def detalle_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    detalles = DetalleReserva.objects.filter(reserva=reserva)
    return render(request, 'detalle_reserva.html', {
        'reserva': reserva,
        'detalles': detalles
    })


def cancelar_reserva(request, id):
    reserva = get_object_or_404(Reserva, id=id)
    reserva.estado = 'cancelada'  
    reserva.save()
    messages.success(request, 'Reserva cancelada correctamente')
    return redirect('reservas')


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

def editar_cliente(request, id):
    cliente = Cliente.objects.get(id=id)
    form = ClienteForm(request.POST or None, instance=cliente)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente actualizado correctamente')
            return redirect('clientes')
        else:
            messages.error(request, 'Error al actualizar el cliente.')
    return render(request, 'formscliente.html', {'form': form, 'accion': 'Editar'})

def desactivar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    cliente.estado = 'inactivo'  
    cliente.save()
    messages.success(request, 'Cliente desactivado correctamente')
    return redirect('clientes')

def obtener_cliente(request):
    dni = request.GET.get('dni', '').strip()
    ruc = request.GET.get('ruc', '').strip()
    cliente = None

    if dni:
        cliente = Cliente.objects.filter(dni=dni, estado=True).first()
    if not cliente and ruc:
        cliente = Cliente.objects.filter(ruc=ruc, estado=True).first()

    if cliente:
        data = {
            'encontrado': True,
            'tipo_cliente': cliente.tipo_cliente,
            'nombres': cliente.nombres,
            'apellidos': cliente.apellidos,
            'razon_social': cliente.razon_social,
            'telefono': cliente.telefono,
            'correo': cliente.correo,
            'direccion': cliente.direccion
        }
    else:
        data = { 'encontrado': False }

    return JsonResponse(data)

