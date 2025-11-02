from django.core.management.base import BaseCommand
from dispositivos.models import Usuario
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Sincroniza usuarios de la tabla usuario con auth_user y hashea contraseñas'

    def handle(self, *args, **options):
        self.stdout.write('Iniciando sincronización de usuarios...')
        
        usuarios = Usuario.objects.all()
        sincronizados = 0
        errores = 0
        
        for usuario in usuarios:
            try:
                # Hashear contraseña si no está hasheada
                if usuario.password and not usuario.password.startswith('pbkdf2_'):
                    self.stdout.write(f'Hasheando contraseña de {usuario.username}...')
                    usuario.set_password(usuario.password)
                    usuario.save(update_fields=['password'])
                
                # Sincronizar con auth_user
                auth_user = usuario.sync_to_auth_user()
                
                if auth_user:
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ Usuario sincronizado: {usuario.username}')
                    )
                    sincronizados += 1
                else:
                    self.stdout.write(
                        self.style.WARNING(f'⚠ Error al sincronizar: {usuario.username}')
                    )
                    errores += 1
                    
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ Error con {usuario.username}: {e}')
                )
                errores += 1
        
        self.stdout.write("\n" + "="*60)
        self.stdout.write(self.style.SUCCESS(f'Sincronización completada'))
        self.stdout.write(f'Usuarios sincronizados: {sincronizados}')
        self.stdout.write(f'Errores: {errores}')
        self.stdout.write("="*60)