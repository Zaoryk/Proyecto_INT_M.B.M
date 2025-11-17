from django.urls import path
from .views import health, info

urlpatterns = [
    path('health/', health, name="health"),
    path("info/", info, name="info")
]
