from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import PerfilUsuario, Modulo
import secrets
import string


class CrearUsuarioForm(forms.ModelForm):
    """Formulario para crear nuevos usuarios con perfil"""
    
    first_name = forms.CharField(
        max_length=150,
        required=True,
        label='Nombres',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombres del usuario'})
    )
    last_name = forms.CharField(
        max_length=150,
        required=True,
        label='Apellidos',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos del usuario'})
    )
    email = forms.EmailField(
        required=True,
        label='Correo Electrónico',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'})
    )
    numero_id = forms.CharField(
        max_length=20,
        required=True,
        label='Número de Identificación',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de cédula o ID'})
    )
    telefono = forms.CharField(
        max_length=20,
        required=False,
        label='Teléfono',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono de contacto'})
    )
    cargo = forms.CharField(
        max_length=100,
        required=False,
        label='Cargo',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cargo en la empresa'})
    )
    departamento = forms.CharField(
        max_length=100,
        required=False,
        label='Departamento',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Departamento o área'})
    )
    modulos_permitidos = forms.ModelMultipleChoiceField(
        queryset=Modulo.objects.filter(activo=True),
        required=False,
        label='Módulos Permitidos',
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        help_text='Selecciona los módulos a los que tendrá acceso este usuario'
    )
    puede_gestionar_usuarios = forms.BooleanField(
        required=False,
        label='Puede Gestionar Usuarios',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        help_text='Permite que este usuario pueda crear y gestionar otros usuarios'
    )
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.password_temporal = self.generar_password_temporal()
    
    def generar_password_temporal(self):
        """Genera una contraseña temporal aleatoria"""
        caracteres = string.ascii_letters + string.digits + "!@#$%"
        return ''.join(secrets.choice(caracteres) for _ in range(12))
    
    def clean_numero_id(self):
        numero_id = self.cleaned_data.get('numero_id')
        if PerfilUsuario.objects.filter(numero_id=numero_id).exists():
            raise forms.ValidationError('Ya existe un usuario con este número de identificación.')
        return numero_id
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Ya existe un usuario con este correo electrónico.')
        return email
    
    def save(self, commit=True, creado_por=None):
        user = super().save(commit=False)
        user.username = self.cleaned_data['numero_id']
        user.set_password(self.password_temporal)
        
        if commit:
            user.save()
            
            perfil, created = PerfilUsuario.objects.get_or_create(user=user)
            perfil.numero_id = self.cleaned_data['numero_id']
            perfil.telefono = self.cleaned_data.get('telefono', '')
            perfil.cargo = self.cleaned_data.get('cargo', '')
            perfil.departamento = self.cleaned_data.get('departamento', '')
            perfil.password_temporal = True
            perfil.puede_gestionar_usuarios = self.cleaned_data.get('puede_gestionar_usuarios', False)
            perfil.creado_por = creado_por
            perfil.save()
            
            modulos = self.cleaned_data.get('modulos_permitidos')
            if modulos:
                perfil.modulos_permitidos.set(modulos)
        
        return user


class EditarUsuarioForm(forms.ModelForm):
    """Formulario para editar usuarios existentes"""
    
    first_name = forms.CharField(
        max_length=150,
        required=True,
        label='Nombres',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=150,
        required=True,
        label='Apellidos',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        required=True,
        label='Correo Electrónico',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    telefono = forms.CharField(
        max_length=20,
        required=False,
        label='Teléfono',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    cargo = forms.CharField(
        max_length=100,
        required=False,
        label='Cargo',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    departamento = forms.CharField(
        max_length=100,
        required=False,
        label='Departamento',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    modulos_permitidos = forms.ModelMultipleChoiceField(
        queryset=Modulo.objects.filter(activo=True),
        required=False,
        label='Módulos Permitidos',
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'})
    )
    puede_gestionar_usuarios = forms.BooleanField(
        required=False,
        label='Puede Gestionar Usuarios',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    activo = forms.BooleanField(
        required=False,
        label='Usuario Activo',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
    
    def __init__(self, *args, **kwargs):
        self.perfil = kwargs.pop('perfil', None)
        super().__init__(*args, **kwargs)
        
        if self.perfil:
            self.fields['telefono'].initial = self.perfil.telefono
            self.fields['cargo'].initial = self.perfil.cargo
            self.fields['departamento'].initial = self.perfil.departamento
            self.fields['modulos_permitidos'].initial = self.perfil.modulos_permitidos.all()
            self.fields['puede_gestionar_usuarios'].initial = self.perfil.puede_gestionar_usuarios
            self.fields['activo'].initial = self.perfil.activo
    
    def save(self, commit=True):
        user = super().save(commit=commit)
        
        if commit and self.perfil:
            self.perfil.telefono = self.cleaned_data.get('telefono', '')
            self.perfil.cargo = self.cleaned_data.get('cargo', '')
            self.perfil.departamento = self.cleaned_data.get('departamento', '')
            self.perfil.puede_gestionar_usuarios = self.cleaned_data.get('puede_gestionar_usuarios', False)
            self.perfil.activo = self.cleaned_data.get('activo', True)
            self.perfil.save()
            
            modulos = self.cleaned_data.get('modulos_permitidos')
            if modulos is not None:
                self.perfil.modulos_permitidos.set(modulos)
        
        return user


class CambiarPasswordForm(PasswordChangeForm):
    """Formulario para cambio de contraseña (incluye contraseña actual)"""
    
    old_password = forms.CharField(
        label='Contraseña Actual',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu contraseña actual'})
    )
    new_password1 = forms.CharField(
        label='Nueva Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu nueva contraseña'})
    )
    new_password2 = forms.CharField(
        label='Confirmar Nueva Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirma tu nueva contraseña'})
    )


class PrimerCambioPasswordForm(forms.Form):
    """Formulario para el primer cambio de contraseña obligatorio"""
    
    password_temporal = forms.CharField(
        label='Contraseña Temporal',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa la contraseña temporal'})
    )
    new_password1 = forms.CharField(
        label='Nueva Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu nueva contraseña'}),
        help_text='Mínimo 8 caracteres, debe incluir letras y números'
    )
    new_password2 = forms.CharField(
        label='Confirmar Nueva Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirma tu nueva contraseña'})
    )
    
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
    
    def clean_password_temporal(self):
        password_temporal = self.cleaned_data.get('password_temporal')
        if not self.user.check_password(password_temporal):
            raise forms.ValidationError('La contraseña temporal es incorrecta.')
        return password_temporal
    
    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')
        
        if new_password1 and new_password2:
            if new_password1 != new_password2:
                raise forms.ValidationError('Las contraseñas no coinciden.')
            
            if len(new_password1) < 8:
                raise forms.ValidationError('La contraseña debe tener al menos 8 caracteres.')
        
        return cleaned_data
    
    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.save()
            if hasattr(self.user, 'perfil'):
                self.user.perfil.password_temporal = False
                from django.utils import timezone
                self.user.perfil.fecha_cambio_password = timezone.now()
                self.user.perfil.save()
        return self.user


class ResetearPasswordForm(forms.Form):
    """Formulario para resetear contraseña de un usuario (solo admin)"""
    
    generar_nueva = forms.BooleanField(
        required=False,
        initial=True,
        label='Generar nueva contraseña temporal',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.password_temporal = self.generar_password_temporal()
    
    def generar_password_temporal(self):
        """Genera una contraseña temporal aleatoria"""
        caracteres = string.ascii_letters + string.digits + "!@#$%"
        return ''.join(secrets.choice(caracteres) for _ in range(12))
    
    def save(self, commit=True):
        if self.cleaned_data.get('generar_nueva'):
            self.user.set_password(self.password_temporal)
            if commit:
                self.user.save()
                if hasattr(self.user, 'perfil'):
                    self.user.perfil.password_temporal = True
                    self.user.perfil.save()
        return self.user
