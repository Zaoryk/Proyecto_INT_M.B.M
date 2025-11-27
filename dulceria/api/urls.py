from .views import health, info
from rest_framework import routers
from django.urls import path, include
from .views import ProveedorViewSet, ProductoViewSet

router = routers.DefaultRouter()
router.register(r'proveedores', ProveedorViewSet)
router.register(r'productos', ProductoViewSet)

urlpatterns = [
    path('health/', health, name="health"),
    path("info/", info, name="info"),
    path('', include(router.urls)),
]
