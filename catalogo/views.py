# catalogo/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

from .models import Producto, Carrito, ItemCarrito
from django import forms
from .forms import ProductoForm

# -----------------------------
# Helpers
# -----------------------------
def _get_cart_from_session(request):
    """
    Devuelve el carrito asociado a la sesión o None si no hay.
    """
    carrito_id = request.session.get('carrito_id')
    if carrito_id:
        try:
            return Carrito.objects.get(pk=carrito_id)
        except Carrito.DoesNotExist:
            # carrito viejo: lo sacamos de la sesión
            request.session.pop('carrito_id', None)
    return None


def _cart_totals(carrito: Carrito):
    items = carrito.items.select_related("producto")
    subtotal = sum(it.producto.precio * it.cantidad for it in items)
    total_items = sum(it.cantidad for it in items)
    impuestos = 0
    total = subtotal + impuestos
    return {
        "subtotal": subtotal,
        "impuestos": impuestos,
        "total": total,
        "total_items": total_items,
    }


# -----------------------------
# Vistas públicas / catálogo
# -----------------------------
def index(request):
    return render(request, "catalogo/index.html", {})


def productos(request):
    prods = Producto.objects.all().order_by("id")
    carrito = _get_cart_from_session(request)
    return render(request, "catalogo/productos.html", {
        "productos": prods,
        "carrito_existe": bool(carrito),
    })


# -----------------------------
# Carrito (sin id en la URL)
# -----------------------------
@login_required
def nuevo_carrito(request):
    """
    Crea un carrito solo si no hay uno en sesión.
    """
    carrito = _get_cart_from_session(request)
    if carrito:
        return redirect("ver_carrito")

    carrito = Carrito.objects.create()
    request.session['carrito_id'] = carrito.id
    messages.success(request, "Carrito creado.")

    next_url = request.GET.get('next')
    if next_url:
        return redirect(next_url)
    return redirect("ver_carrito")


@login_required
def ver_carrito(request):
    carrito = _get_cart_from_session(request)
    if not carrito:
        # si no hay carrito, mandamos a crear uno o a productos
        return redirect("nuevo_carrito")
    totals = _cart_totals(carrito)
    return render(request, "catalogo/carrito.html", {
        "carrito": carrito,
        "totals": totals,
    })


@login_required
def agregar(request, producto_id):
    """
    Agrega 1 unidad de un producto al carrito ACTUAL (el de la sesión).
    Si no hay carrito, lo crea.
    """
    carrito = _get_cart_from_session(request)
    if not carrito:
        carrito = Carrito.objects.create()
        request.session['carrito_id'] = carrito.id

    producto = get_object_or_404(Producto, pk=producto_id)

    item = carrito.items.filter(producto=producto).first()
    nueva_cant = (item.cantidad + 1) if item else 1

    # validamos stock
    if producto.stock is not None and nueva_cant > producto.stock:
        messages.warning(request, "No hay stock suficiente para este producto.")
        return redirect("ver_carrito")

    # si pasó la validación, guardamos
    if item:
        item.cantidad = nueva_cant
        item.save()
    else:
        ItemCarrito.objects.create(carrito=carrito, producto=producto, cantidad=1)

    messages.success(request, f"Agregado: {producto.nombre}")
    return redirect("ver_carrito")


@login_required
def quitar(request, item_id):
    carrito = _get_cart_from_session(request)
    if not carrito:
        return redirect("ver_carrito")

    item = get_object_or_404(ItemCarrito, pk=item_id, carrito=carrito)
    item.delete()
    messages.info(request, "Producto eliminado del carrito.")
    return redirect("ver_carrito")


@login_required
@require_POST
def cambiar_cantidad(request, item_id):
    carrito = _get_cart_from_session(request)
    if not carrito:
        return redirect("ver_carrito")

    item = get_object_or_404(ItemCarrito, pk=item_id, carrito=carrito)
    try:
        nueva = int(request.POST.get("cantidad", item.cantidad))
    except (TypeError, ValueError):
        messages.error(request, "Cantidad inválida.")
        return redirect("ver_carrito")

    if nueva <= 0:
        item.delete()
        messages.info(request, "Ítem eliminado.")
    else:
        item.cantidad = nueva
        item.save()
        messages.success(request, "Cantidad actualizada.")
    return redirect("ver_carrito")


@login_required
def vaciar_carrito(request):
    carrito = _get_cart_from_session(request)
    if carrito:
        carrito.items.all().delete()
        messages.info(request, "Carrito vaciado.")
    return redirect("ver_carrito")


# -----------------------------
# Detalle producto
# -----------------------------
def detalle_producto(request, pk):
    p = get_object_or_404(Producto, pk=pk)
    carrito = _get_cart_from_session(request)
    return render(request, "catalogo/detalle_producto.html", {
        "producto": p,
        "carrito_existe": bool(carrito),
    })


# -----------------------------
# Auth
# -----------------------------
def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Cuenta creada correctamente.")
            return redirect("productos")
    else:
        form = UserCreationForm()
    return render(request, "catalogo/auth/signup.html", {"form": form})
    # ojo: según tu estructura era templates/auth/..., no templates/catalogo/auth/...


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Has iniciado sesión.")
            return redirect("productos")
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
    else:
        form = AuthenticationForm()
    return render(request, "catalogo/auth/login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.info(request, "Sesión cerrada.")
    return redirect("index")


@login_required
def product_list(request):
    productos = Producto.objects.all().order_by("id")
    return render(request, "catalogo/products/list.html", {
        "productos": productos,
    })

@login_required
def product_create(request):
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado correctamente.")
            return redirect("product_list")
    else:
        form = ProductoForm()
    return render(request, "catalogo/products/form.html", {
        "form": form,
        "title": "Nuevo producto",
    })

@login_required
def product_update(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado.")
            return redirect("product_list")
    else:
        form = ProductoForm(instance=producto)
    return render(request, "catalogo/products/form.html", {
        "form": form,
        "title": "Editar producto",
    })

@login_required
def product_delete(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == "POST":
        producto.delete()
        messages.info(request, "Producto eliminado.")
        return redirect("product_list")
    return render(request, "catalogo/products/confirm_delete.html", {
        "producto": producto,
    })