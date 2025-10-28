from django.shortcuts import render, redirect, get_object_or_404
from dispositivos.models import Usuario, Producto, Proveedor, ProductoProveedor
from dispositivos.forms import UsuarioForm, ProveedorForm, ProductoForm, ProductoProveedorForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q
from django.http import HttpResponse
import openpyxl

# -------------------------------------------------------------
# DASHBOARD
# -------------------------------------------------------------
@login_required
def dashboard(request):
    visitas = request.session.get('visitas', 0)
    request.session['visitas'] = visitas + 1

    context = {
        'visitas': visitas,
        'usuarios_count': Usuario.objects.count(),
        'productos_count': Producto.objects.count(),
        'proveedores_count': Proveedor.objects.count(),
        'movimientos_count': ProductoProveedor.objects.count(),
        'ultimos_usuarios': Usuario.objects.order_by('-idUsuario')[:3],
    }
    return render(request, "dispositivos/dashboard.html", context)


# -------------------------------------------------------------
# USUARIOS
# -------------------------------------------------------------
def formularioUsuario(request):
    visitas = request.session.get("visitas", 0)
    request.session['visitas'] = visitas + 1

    search = request.GET.get("buscar", "")
    rol_filter = request.GET.get("rol", "")
    estado_filter = request.GET.get("estado", "")

    usuarios = Usuario.objects.all()
    if search:
        usuarios = usuarios.filter(Q(username__icontains=search) | Q(nombre__icontains=search))
    if rol_filter:
        usuarios = usuarios.filter(rol__iexact=rol_filter)
    if estado_filter:
        usuarios = usuarios.filter(estado__iexact=estado_filter)

    # Exportar a Excel
    if "export_excel" in request.GET:
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Usuarios"
        headers = ["Username", "Email", "Nombre", "Apellido", "Rol", "Estado", "MFA"]
        sheet.append(headers)
        for u in usuarios:
            sheet.append([
                u.username, u.email, u.nombre, u.apellido,
                u.get_rol_display(), u.get_estado_display(), u.get_mfa_habilitado_display()
            ])
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response['Content-Disposition'] = 'attachment; filename="usuarios.xlsx"'
        workbook.save(response)
        return response

    # CRUD
    if request.method == "GET" and "edit_id" in request.GET:
        form = UsuarioForm(instance=get_object_or_404(Usuario, pk=request.GET.get("edit_id")))
        edit_mode = True
    elif request.method == "POST":
        edit_id = request.POST.get("edit_id")
        instance = get_object_or_404(Usuario, pk=edit_id) if edit_id else None
        form = UsuarioForm(request.POST, instance=instance)
        edit_mode = bool(edit_id)
        if form.is_valid():
            form.save()
            return redirect("Formulario")
    elif request.method == "GET" and "delete_id" in request.GET:
        Usuario.objects.filter(pk=request.GET.get("delete_id")).delete()
        return redirect("Formulario")
    else:
        form = UsuarioForm()
        edit_mode = False

    return render(request, "dispositivos/formularioUsuario.html", {
        "visitas": visitas,
        "form": form,
        "usuarios": usuarios,
        "edit_mode": edit_mode,
        "edit_id": request.GET.get("edit_id", ""),
    })


# -------------------------------------------------------------
# PRODUCTOS
# -------------------------------------------------------------
def gestionProductos(request):
    visitas = request.session.get("visitas", 0)
    request.session['visitas'] = visitas + 1

    search = request.GET.get("buscar", "")
    productos = Producto.objects.all()
    if search:
        productos = productos.filter(Q(nombre__icontains=search) | Q(sku__icontains=search))

    # Exportar a Excel
    if "export_excel" in request.GET:
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Productos"
        headers = ["SKU", "Nombre", "Categoría", "Unidad Compra", "Unidad Venta", "IVA", "Stock Mínimo"]
        sheet.append(headers)
        for p in productos:
            sheet.append([
                p.sku, p.nombre, p.categoria, p.uom_compra, p.uom_venta, p.impuesto_iva, p.stock_minimo
            ])
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response['Content-Disposition'] = 'attachment; filename="productos.xlsx"'
        workbook.save(response)
        return response

    # CRUD
    if request.method == "GET" and "edit_id" in request.GET:
        form = ProductoForm(instance=get_object_or_404(Producto, pk=request.GET.get("edit_id")))
        edit_mode = True
    elif request.method == "POST":
        edit_id = request.POST.get("edit_id")
        instance = get_object_or_404(Producto, pk=edit_id) if edit_id else None
        form = ProductoForm(request.POST, instance=instance)
        edit_mode = bool(edit_id)
        if form.is_valid():
            form.save()
            return redirect("Productos")
    elif request.method == "GET" and "delete_id" in request.GET:
        Producto.objects.filter(pk=request.GET.get("delete_id")).delete()
        return redirect("Productos")
    else:
        form = ProductoForm()
        edit_mode = False

    return render(request, "dispositivos/gestionProductos.html", {
        "visitas": visitas,
        "form": form,
        "productos": productos,
        "edit_mode": edit_mode,
        "edit_id": request.GET.get("edit_id", ""),
    })


# -------------------------------------------------------------
# PROVEEDORES
# -------------------------------------------------------------
def gestionProveedores(request):
    visitas = request.session.get("visitas", 0)
    request.session['visitas'] = visitas + 1

    buscar = request.GET.get('buscar', '')
    proveedores = Proveedor.objects.all()
    if buscar:
        proveedores = proveedores.filter(
            Q(rut_nif__icontains=buscar) | Q(razon_social__icontains=buscar)
        )

    # Exportar a Excel
    if "export_excel" in request.GET:
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Proveedores"
        headers = ["RUT/NIF", "Razón Social", "Estado", "Email", "País"]
        sheet.append(headers)
        for p in proveedores:
            sheet.append([
                p.rut_nif, p.razon_social, p.get_estado_display(), p.email, p.pais
            ])
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response['Content-Disposition'] = 'attachment; filename="proveedores.xlsx"'
        workbook.save(response)
        return response

    # CRUD
    if request.method == "GET" and "edit_id" in request.GET:
        form = ProveedorForm(instance=get_object_or_404(Proveedor, pk=request.GET.get("edit_id")))
        edit_mode = True
    elif request.method == "POST":
        edit_id = request.POST.get("edit_id")
        instance = get_object_or_404(Proveedor, pk=edit_id) if edit_id else None
        form = ProveedorForm(request.POST, instance=instance)
        edit_mode = bool(edit_id)
        if form.is_valid():
            form.save()
            return redirect("Proveedores")
    elif request.method == "GET" and "delete_id" in request.GET:
        Proveedor.objects.filter(pk=request.GET.get("delete_id")).delete()
        return redirect("Proveedores")
    else:
        form = ProveedorForm()
        edit_mode = False

    return render(request, "dispositivos/gestionProveedores.html", {
        "visitas": visitas,
        "form": form,
        "proveedores": proveedores,
        "edit_mode": edit_mode,
        "edit_id": request.GET.get("edit_id", ""),
        "buscar": buscar,
    })


# -------------------------------------------------------------
# PRODUCTO - PROVEEDOR (MOVIMIENTOS)
# -------------------------------------------------------------
def moduloTransaccional(request):
    visitas = request.session.get("visitas", 0)
    request.session['visitas'] = visitas + 1

    search = request.GET.get("buscar", "")
    tipo = request.GET.get("tipo", "")
    movimientos = ProductoProveedor.objects.select_related('producto', 'proveedor').all()

    if search:
        movimientos = movimientos.filter(Q(producto__sku__icontains=search) | Q(producto__nombre__icontains=search))
    if tipo:
        movimientos = movimientos.filter(tipo_movimiento__iexact=tipo)

    # Exportar a Excel
    if "export_excel" in request.GET:
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Movimientos"
        headers = ["Fecha", "Tipo", "Producto", "Proveedor", "Cantidad"]
        sheet.append(headers)
        for m in movimientos:
            sheet.append([
                timezone.localtime(m.fecha_movimiento).strftime("%Y-%m-%d %H:%M"),
                m.get_tipo_movimiento_display(),
                m.producto.nombre,
                m.proveedor.razon_social,
                m.cantidad,
            ])
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response['Content-Disposition'] = 'attachment; filename="movimientos.xlsx"'
        workbook.save(response)
        return response

    # CRUD
    if request.method == "GET" and "edit_id" in request.GET:
        form = ProductoProveedorForm(instance=get_object_or_404(ProductoProveedor, pk=request.GET.get("edit_id")))
        edit_mode = True
    elif request.method == "POST":
        edit_id = request.POST.get("edit_id")
        instance = get_object_or_404(ProductoProveedor, pk=edit_id) if edit_id else None
        form = ProductoProveedorForm(request.POST, instance=instance)
        edit_mode = bool(edit_id)
        if form.is_valid():
            form.save()
            return redirect("Transaccional")
    elif request.method == "GET" and "delete_id" in request.GET:
        ProductoProveedor.objects.filter(pk=request.GET.get("delete_id")).delete()
        return redirect("Transaccional")
    else:
        form = ProductoProveedorForm()
        edit_mode = False

    movimientos_hoy = ProductoProveedor.objects.filter(
        fecha_movimiento__date=timezone.now().date()
    ).count()

    return render(request, "dispositivos/moduloTransaccional.html", {
        "visitas": visitas,
        "form": form,
        "movimientos": movimientos,
        "movimientos_hoy": movimientos_hoy,
        "productos_count": Producto.objects.count(),
        "edit_mode": edit_mode,
        "edit_id": request.GET.get("edit_id", ""),
    })
