from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib.messages import get_messages
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def logear(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Tu cuenta está inactiva. Contacta al administrador.')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'login.html')


def cerrar_sesion(request):
    logout(request)
    storage = get_messages(request)
    list(storage)
    messages.success(request, 'Has cerrado sesión correctamente')
    return redirect('logear')


