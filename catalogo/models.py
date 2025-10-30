from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=120)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.CharField(max_length=255, blank=True)  # ruta dentro de /static/images/
    stock = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.nombre

class Carrito(models.Model):
    creado = models.DateTimeField(auto_now_add=True)

    def total(self):
        return sum(item.subtotal() for item in self.items.all())

class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, related_name="items", on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.producto.precio * self.cantidad
