from django.shortcuts import render, redirect, get_object_or_404
from dispositivos.models import Usuario, Producto, Proveedor, ProductoProveedor
from dispositivos.forms import UsuarioForm, ProveedorForm, ProductoForm, ProductoProveedorForm
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.utils import timezone

@login_required
def dashboard(request):
    visitas = request.session.get('visitas', 0)
    request.session['visitas'] = visitas + 1
    
    # Conteo de registros
    usuarios_count = Usuario.objects.count()
    productos_count = Producto.objects.count()
    proveedores_count = Proveedor.objects.count()
    movimientos_count = ProductoProveedor.objects.count()
    
    # Últimos movimientos/actividad para el timeline
    
    # Últimos usuarios creados
    ultimos_usuarios = Usuario.objects.order_by('-idUsuario')[:3]
    
    context = {
        'visitas': visitas,
        'usuarios_count': usuarios_count,
        'productos_count': productos_count,
        'proveedores_count': proveedores_count,
        'movimientos_count': movimientos_count,
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

    # Editar producto
    if request.method == "GET" and "edit_id" in request.GET:
        producto_to_edit = get_object_or_404(Producto, pk=request.GET.get("edit_id"))
        form = ProductoForm(instance=producto_to_edit)
        edit_mode = True
    # Crear o actualizar producto
    elif request.method == "POST":
        edit_id = request.POST.get("edit_id")
        if edit_id:
            instance = get_object_or_404(Producto, pk=edit_id)
            form = ProductoForm(request.POST, instance=instance)
            edit_mode = True
        else:
            form = ProductoForm(request.POST)
            edit_mode = False
        if form.is_valid():
            form.save()
            return redirect("Productos")
    # Eliminar producto
    elif request.method == "GET" and "delete_id" in request.GET:
        Producto.objects.filter(pk=request.GET.get("delete_id")).delete()
        return redirect("Productos")
    else:
        form = ProductoForm()
        edit_mode = False

    productos = Producto.objects.all()
    return render(request, "dispositivos/gestionProductos.html", {
        "visitas": visitas,
        "form": form,
        "productos": productos,
        "edit_mode": edit_mode if "edit_mode" in locals() else False,
        "edit_id": request.GET.get("edit_id") if "edit_id" in request.GET else "",
    })

def gestionProveedores(request):
    visitas = request.session.get("visitas", 0)
    request.session['visitas'] = visitas + 1

    # Editar proveedor
    if request.method == "GET" and "edit_id" in request.GET:
        proveedor_to_edit = get_object_or_404(Proveedor, pk=request.GET.get("edit_id"))
        form = ProveedorForm(instance=proveedor_to_edit)
        edit_mode = True
    # Crear o actualizar proveedor
    elif request.method == "POST":
        edit_id = request.POST.get("edit_id")
        if edit_id:
            instance = get_object_or_404(Proveedor, pk=edit_id)
            form = ProveedorForm(request.POST, instance=instance)
            edit_mode = True
        else:
            form = ProveedorForm(request.POST)
            edit_mode = False
        if form.is_valid():
            form.save()
            return redirect("Proveedores")
    # Eliminar proveedor
    elif request.method == "GET" and "delete_id" in request.GET:
        Proveedor.objects.filter(pk=request.GET.get("delete_id")).delete()
        return redirect("Proveedores")
    else:
        form = ProveedorForm()
        edit_mode = False

    proveedores = Proveedor.objects.all()
    return render(request, "dispositivos/gestionProveedores.html", {
        "visitas": visitas,
        "form": form,
        "proveedores": proveedores,
        "edit_mode": edit_mode if "edit_mode" in locals() else False,
        "edit_id": request.GET.get("edit_id") if "edit_id" in request.GET else "",
    })

def moduloTransaccional(request):
    visitas = request.session.get("visitas", 0)
    request.session['visitas'] = visitas + 1

    # Editar movimiento
    if request.method == "GET" and "edit_id" in request.GET:
        movimiento_to_edit = get_object_or_404(ProductoProveedor, pk=request.GET.get("edit_id"))
        form = ProductoProveedorForm(instance=movimiento_to_edit)
        edit_mode = True
    # Crear o actualizar movimiento
    elif request.method == "POST":
        edit_id = request.POST.get("edit_id")
        if edit_id:
            instance = get_object_or_404(ProductoProveedor, pk=edit_id)
            form = ProductoProveedorForm(request.POST, instance=instance)
            edit_mode = True
        else:
            form = ProductoProveedorForm(request.POST)
            edit_mode = False
        if form.is_valid():
            form.save()
            return redirect("Transaccional")
    # Eliminar movimiento
    elif request.method == "GET" and "delete_id" in request.GET:
        ProductoProveedor.objects.filter(pk=request.GET.get("delete_id")).delete()
        return redirect("Transaccional")
    else:
        form = ProductoProveedorForm()
        edit_mode = False

    movimientos = ProductoProveedor.objects.select_related('producto', 'proveedor').all()
    
    # Métricas
    movimientos_hoy = ProductoProveedor.objects.filter(fecha_movimiento__date=timezone.now().date()).count()
    productos_count = Producto.objects.count()
    
    return render(request, "dispositivos/moduloTransaccional.html", {
        "visitas": visitas,
        "form": form,
        "movimientos": movimientos,
        "movimientos_hoy": movimientos_hoy,
        "productos_count": productos_count,
        "edit_mode": edit_mode if "edit_mode" in locals() else False,
        "edit_id": request.GET.get("edit_id") if "edit_id" in request.GET else "",
    })