from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import viewsets
from dispositivos.models import Proveedor, Producto
from .serializers import ProveedorSerializer, ProductoSerializer
from rest_framework.permissions import IsAuthenticated
class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated]

def health(request):
    return JsonResponse({"status": "ok"})

def info(request):
    return JsonResponse({"proyecto": "Lilis", "version":"1.0","autor":"Marlon Tabilo, Marcos Changala,Benjamin "})