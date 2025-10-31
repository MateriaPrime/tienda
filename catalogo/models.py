from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to="productos/", blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)  # 👈 TIENE QUE ESTAR

    def __str__(self):
        return self.nombre

class Carrito(models.Model):
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Carrito #{self.id}"

class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, related_name="items", on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    @property
    def subtotal(self):
        return self.producto.precio * self.cantidad
