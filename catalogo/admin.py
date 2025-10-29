from django.contrib import admin
from .models import Producto, Carrito, ItemCarrito

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "precio")
    search_fields = ("nombre",)
    list_filter = ("precio",)

admin.site.register(Carrito)
admin.site.register(ItemCarrito)
