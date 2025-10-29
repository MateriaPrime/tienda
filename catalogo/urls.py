from django.urls import path
from catalogo import views

urlpatterns = [
    path('', views.index, name="index"),
    path('productos/', views.productos, name="productos"),
    path('carrito/<int:carrito_id>/', views.ver_carrito, name="ver_carrito"),
    path('carrito/<int:carrito_id>/agregar/<int:producto_id>/', views.agregar, name="agregar"),
    path('carrito/<int:carrito_id>/quitar/<int:item_id>/', views.quitar, name="quitar"),
    path('carrito/nuevo/', views.nuevo_carrito, name="nuevo_carrito"),
]
