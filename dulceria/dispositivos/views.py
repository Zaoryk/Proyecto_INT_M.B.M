from django.shortcuts import render, redirect, get_object_or_404
from dispositivos.models import Usuario, Producto, Proveedor, MovimientoInventario
from dispositivos.forms import UsuarioForm
# Create your views here.
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    visitas = request.session.get('visitas', 0)
    request.session['visitas'] = visitas + 1
    
    # Conteo de registros
    usuarios_count = Usuario.objects.count()
    productos_count = Producto.objects.count()
    proveedores_count = Proveedor.objects.count()
    movimientos_count = MovimientoInventario.objects.count()
    
    # Últimos movimientos/actividad para el timeline
    ultimos_movimientos = MovimientoInventario.objects.select_related('producto').order_by('-fecha')[:3]
    
    # Últimos usuarios creados
    ultimos_usuarios = Usuario.objects.order_by('-idUsuario')[:3]
    
    context = {
        'visitas': visitas,
        'usuarios_count': usuarios_count,
        'productos_count': productos_count,
        'proveedores_count': proveedores_count,
        'movimientos_count': movimientos_count,
        'ultimos_movimientos': ultimos_movimientos,
        'ultimos_usuarios': ultimos_usuarios,
    }
    return render(request, "dispositivos/dashboard.html", context)

def formularioUsuario(request):
    visitas = request.session.get("visitas", 0)
    request.session['visitas'] = visitas + 1

    # Editar usuario (por ID en GET)
    if request.method == "GET" and "edit_id" in request.GET:
        user_to_edit = get_object_or_404(Usuario, pk=request.GET.get("edit_id"))
        form = UsuarioForm(instance=user_to_edit)
        edit_mode = True
    # Crear o actualizar usuario
    elif request.method == "POST":
        edit_id = request.POST.get("edit_id")
        if edit_id:
            instance = get_object_or_404(Usuario, pk=edit_id)
            form = UsuarioForm(request.POST, instance=instance)
            edit_mode = True
        else:
            form = UsuarioForm(request.POST)
            edit_mode = False
        if form.is_valid():
            form.save()
            return redirect("Formulario")
    # Eliminar usuario
    elif request.method == "GET" and "delete_id" in request.GET:
        Usuario.objects.filter(pk=request.GET.get("delete_id")).delete()
        return redirect("Formulario")
    else:
        form = UsuarioForm()
        edit_mode = False

    usuarios = Usuario.objects.all()
    return render(request, "dispositivos/formularioUsuario.html", {
        "visitas": visitas,
        "form": form,
        "usuarios": usuarios,
        "edit_mode": edit_mode if "edit_mode" in locals() else False,
        "edit_id": request.GET.get("edit_id") if "edit_id" in request.GET else "",
    })

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