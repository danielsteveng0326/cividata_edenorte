from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from login.models import PerfilUsuario


class Command(BaseCommand):
    help = 'Configura el perfil del superusuario existente'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Configurando perfiles de superusuarios...'))
        
        # Obtener todos los superusuarios
        superusers = User.objects.filter(is_superuser=True)
        
        if not superusers.exists():
            self.stdout.write(self.style.ERROR('No se encontraron superusuarios en el sistema'))
            self.stdout.write('Crea uno con: python manage.py createsuperuser')
            return
        
        for user in superusers:
            self.stdout.write(f'\nConfigurando usuario: {user.username}')
            
            # Crear o actualizar perfil
            perfil, created = PerfilUsuario.objects.get_or_create(
                user=user,
                defaults={
                    'numero_id': user.username,
                    'es_superusuario_sistema': True,
                    'puede_gestionar_usuarios': True,
                    'password_temporal': False,
                    'activo': True
                }
            )
            
            if not created:
                # Actualizar perfil existente
                perfil.numero_id = user.username if not perfil.numero_id else perfil.numero_id
                perfil.es_superusuario_sistema = True
                perfil.puede_gestionar_usuarios = True
                perfil.password_temporal = False
                perfil.activo = True
                perfil.save()
                self.stdout.write(self.style.SUCCESS(f'✓ Perfil actualizado para: {user.username}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'✓ Perfil creado para: {user.username}'))
            
            # Mostrar información
            self.stdout.write(f'  - Email: {user.email}')
            self.stdout.write(f'  - Número ID: {perfil.numero_id}')
            self.stdout.write(f'  - Superusuario del sistema: {perfil.es_superusuario_sistema}')
            self.stdout.write(f'  - Puede gestionar usuarios: {perfil.puede_gestionar_usuarios}')
        
        self.stdout.write(self.style.SUCCESS('\n✓ Configuración completada'))
        self.stdout.write(self.style.WARNING('\nAhora puedes acceder a:'))
        self.stdout.write('  http://localhost:8000/login/usuarios/')
