from dispositivos.models import Usuario

def usuario_avatar(request):
    if request.user.is_authenticated:
        try:
            usuario = Usuario.objects.get(username=request.user.username)
            return {'usuario_actual': usuario}
        except Usuario.DoesNotExist:
            return {'usuario_actual': None}
    return {'usuario_actual': None}
