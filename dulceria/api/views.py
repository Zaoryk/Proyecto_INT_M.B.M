from django.shortcuts import render
from django.http import JsonResponse

def health(request):
    return JsonResponse({"status": "ok"})

def info(request):
    return JsonResponse({"proyecto": "EcoEnergy", "version":"1.0","autor":"Marlon Tabilo, Marcos Changala"})