from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Modulo, PerfilUsuario


class PerfilUsuarioInline(admin.StackedInline):
    model = PerfilUsuario
    can_delete = False
    verbose_name_plural = 'Perfil'
    fk_name = 'user'
    filter_horizontal = ('modulos_permitidos',)


class UserAdmin(BaseUserAdmin):
    inlines = (PerfilUsuarioInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_numero_id')
    
    def get_numero_id(self, obj):
        return obj.perfil.numero_id if hasattr(obj, 'perfil') else '-'
    get_numero_id.short_description = 'Número ID'


@admin.register(Modulo)
class ModuloAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codigo', 'activo', 'orden')
    list_filter = ('activo',)
    search_fields = ('nombre', 'codigo')
    ordering = ('orden', 'nombre')


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('user', 'numero_id', 'cargo', 'es_superusuario_sistema', 'activo', 'fecha_creacion')
    list_filter = ('es_superusuario_sistema', 'puede_gestionar_usuarios', 'activo', 'password_temporal')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'numero_id', 'cargo')
    filter_horizontal = ('modulos_permitidos',)
    readonly_fields = ('fecha_creacion', 'fecha_modificacion')


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
