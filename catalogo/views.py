from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto, Carrito, ItemCarrito

def index(request):
    return render(request, "catalogo/index.html", {})

def productos(request):
    prods = Producto.objects.all()
    carrito_id = request.session.get('carrito_id')  # <- leer carrito activo (si existe)
    return render(request, "catalogo/productos.html", {
        "productos": prods,
        "carrito_id": carrito_id,
    })

def nuevo_carrito(request):
    # Si ya hay carrito en sesión, no crear otro.
    carrito_id = request.session.get('carrito_id')
    if carrito_id:
        return redirect("ver_carrito", carrito_id=carrito_id)

    c = Carrito.objects.create()
    request.session['carrito_id'] = c.id

    # Si venimos desde productos, volver allá
    next_url = request.GET.get('next')
    if next_url:
        return redirect(next_url)
    return redirect("ver_carrito", carrito_id=c.id)

def ver_carrito(request, carrito_id):
    carrito = get_object_or_404(Carrito, pk=carrito_id)
    # Sincroniza la sesión con este carrito
    request.session['carrito_id'] = carrito.id
    return render(request, "catalogo/carrito.html", {"carrito": carrito})

def agregar(request, carrito_id, producto_id):
    # Asegura que la sesión apunte a este carrito
    request.session['carrito_id'] = carrito_id

    carrito = get_object_or_404(Carrito, pk=carrito_id)
    producto = get_object_or_404(Producto, pk=producto_id)

    item = carrito.items.filter(producto=producto).first()
    if item:
        item.cantidad += 1
        item.save()
    else:
        ItemCarrito.objects.create(carrito=carrito, producto=producto, cantidad=1)

    return redirect("ver_carrito", carrito_id=carrito.id)

def quitar(request, carrito_id, item_id):
    carrito = get_object_or_404(Carrito, pk=carrito_id)
    item = get_object_or_404(ItemCarrito, pk=item_id, carrito=carrito)
    item.delete()
    return redirect("ver_carrito", carrito_id=carrito.id)