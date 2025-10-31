# catalogo/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # catálogo
    path('productos/', views.productos, name='productos'),
    path('producto/<int:pk>/', views.detalle_producto, name='detalle_producto'),

    # carrito
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

    # CRUD productos propio (no choca con /admin/)
    path('panel/products/', views.product_list, name='product_list'),
    path('panel/products/create/', views.product_create, name='product_create'),
    path('panel/products/<int:pk>/update/', views.product_update, name='product_update'),
    path('panel/products/<int:pk>/delete/', views.product_delete, name='product_delete'),
]
