from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
def dashboard(request):
    visitas = request.session.get('visitas', 0)
    request.session['visitas'] = visitas + 1
    return render(request, 'accounts/dashboard.html', {'visitas': visitas})

