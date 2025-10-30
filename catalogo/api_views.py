from rest_framework import viewsets, permissions
from .models import Producto
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all().order_by('id')
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
