# catalogo/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # catálogo
    path('productos/', views.productos, name='productos'),
    path('producto/<int:pk>/', views.detalle_producto, name='detalle_producto'),

    # carrito (sin id en la URL)
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/nuevo/', views.nuevo_carrito, name='nuevo_carrito'),
    path('carrito/agregar/<int:producto_id>/', views.agregar, name='agregar'),
    path('carrito/quitar/<int:item_id>/', views.quitar, name='quitar'),
    path('carrito/cambiar/<int:item_id>/', views.cambiar_cantidad, name='cambiar_cantidad'),
    path('carrito/vaciar/', views.vaciar_carrito, name='vaciar_carrito'),

    # auth
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
]
