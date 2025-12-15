from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from login.models import Modulo, PerfilUsuario


class Command(BaseCommand):
    help = 'Inicializa los módulos del sistema y configura el superusuario'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Inicializando módulos del sistema...'))
        
        # Crear módulos
        modulos_data = [
            {
                'codigo': 'contratacion',
                'nombre': 'Contratación',
                'descripcion': 'Módulo de gestión de contratos y contratación',
                'icono': 'fas fa-file-contract',
                'orden': 1
            },
            {
                'codigo': 'asistente_contratacion',
                'nombre': 'Asistente Contratación',
                'descripcion': 'Herramientas asistidas para procesos de contratación',
                'icono': 'fas fa-briefcase',
                'orden': 2
            },
            {
                'codigo': 'paa',
                'nombre': 'PAA',
                'descripcion': 'Plan Anual de Adquisiciones',
                'icono': 'fas fa-calendar-alt',
                'orden': 3
            },
            {
                'codigo': 'docs_contractual',
                'nombre': 'Documentos Contractuales',
                'descripcion': 'Generación automática de documentos contractuales',
                'icono': 'fas fa-file-alt',
                'orden': 4
            },
            {
                'codigo': 'proveedores',
                'nombre': 'Proveedores',
                'descripcion': 'Gestión de proveedores y contratistas',
                'icono': 'fas fa-users',
                'orden': 5
            },
            {
                'codigo': 'reportes',
                'nombre': 'Reportes',
                'descripcion': 'Reportes y estadísticas del sistema',
                'icono': 'fas fa-chart-bar',
                'orden': 6
            },
            {
                'codigo': 'chatbot',
                'nombre': 'Chatbot Emil-IA',
                'descripcion': 'Asistente virtual inteligente',
                'icono': 'fas fa-robot',
                'orden': 7
            },
        ]
        
        for modulo_data in modulos_data:
            modulo, created = Modulo.objects.get_or_create(
                codigo=modulo_data['codigo'],
                defaults={
                    'nombre': modulo_data['nombre'],
                    'descripcion': modulo_data['descripcion'],
                    'icono': modulo_data['icono'],
                    'orden': modulo_data['orden'],
                    'activo': True
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Módulo creado: {modulo.nombre}'))
            else:
                self.stdout.write(f'  Módulo ya existe: {modulo.nombre}')
        
        self.stdout.write(self.style.SUCCESS('\n✓ Módulos inicializados correctamente'))
        
        # Configurar superusuario si existe
        self.stdout.write('\nConfigurando perfiles de usuarios existentes...')
        
        for user in User.objects.all():
            if hasattr(user, 'perfil'):
                perfil = user.perfil
                
                # Si el usuario es superuser de Django, marcarlo como superusuario del sistema
                if user.is_superuser and not perfil.es_superusuario_sistema:
                    perfil.es_superusuario_sistema = True
                    perfil.puede_gestionar_usuarios = True
                    perfil.password_temporal = False
                    
                    # Asignar número de ID si no tiene
                    if not perfil.numero_id:
                        perfil.numero_id = user.username
                    
                    perfil.save()
                    self.stdout.write(self.style.SUCCESS(f'✓ Superusuario configurado: {user.username}'))
        
        self.stdout.write(self.style.SUCCESS('\n✓ Inicialización completada exitosamente'))
        self.stdout.write(self.style.WARNING('\nNOTA: Recuerda ejecutar las migraciones antes de usar este comando:'))
        self.stdout.write('  python manage.py makemigrations')
        self.stdout.write('  python manage.py migrate')
