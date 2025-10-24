from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    visitas = request.session.get('visitas', 0)
    request.session['visitas'] = visitas + 1
    return render(request, "dispositivos/dashboard.html")

def formularioUsuario(request):
    visitas = request.session.get("visitas", 0)
    request.session['visitas'] = visitas + 1
    return render(request, "dispositivos/formularioUsuario.html")

def gestionProductos(request):
    visitas = request.session.get("visitas", 0)
    request.session['visitas'] = visitas + 1
    return render(request, "dispositivos/gestionProductos.html")

def gestionProveedores(request):
    visitas = request.session.get("visitas", 0)
    request.session['visitas'] = visitas + 1
    return render(request, "dispositivos/gestionProveedores.html")

def moduloTransaccional(request):
    visitas = request.session.get("visitas", 0)
    request.session['visitas'] = visitas + 1
    return render(request, "dispositivos/moduloTransaccional.html")