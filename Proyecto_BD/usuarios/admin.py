from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

# Registramos nuestro modelo Usuario personalizado en el panel de administración de Django
@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    """
    Personalización de la interfaz del Admin para el modelo Usuario.
    Muestra los campos personalizados (intentos_fallidos, bloqueado) en las listas y formularios del Admin.
    """
    list_display = ('username', 'email', 'intentos_fallidos', 'bloqueado', 'is_staff')
    list_filter = ('bloqueado', 'is_staff', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        ('Control de Intentos y Bloqueo', {'fields': ('intentos_fallidos', 'bloqueado')}),
    )

