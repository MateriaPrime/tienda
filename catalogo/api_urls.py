from rest_framework.routers import DefaultRouter
from .api_views import ProductoViewSet

router = DefaultRouter()
router.register(r'productos', ProductoViewSet, basename='api-productos')

urlpatterns = router.urls
