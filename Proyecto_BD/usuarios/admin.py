# ==============================================================================
# EVA 1: INTEGRACIÓN DEL MODELO USUARIO EN EL DJANGO ADMIN (admin.py)
# ==============================================================================
# Al utilizar un modelo de usuario personalizado heredado de AbstractUser, es
# fundamental registrarlo en el panel administrativo extendiendo 'UserAdmin'.
# Esto garantiza que las herramientas de reseteo de contraseñas y permisos de Django
# sigan funcionando y, además, expone nuestros campos 'intentos_fallidos' y 'bloqueado'.
# ==============================================================================

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    """
    Configuración avanzada de la administración para el modelo Usuario.
    Permite a los administradores / docentes:
    1. Ver de un vistazo qué usuarios están bloqueados y cuántos intentos fallidos llevan.
    2. Filtrar rápidamente por estado de bloqueo ('bloqueado').
    3. Editar manualmente estos campos para desbloquear usuarios desde /admin/.
    """

    # Columnas desplegadas en la tabla general de usuarios
    list_display = (
        'username',
        'email',
        'intentos_fallidos',
        'bloqueado',
        'is_staff',
        'is_active',
        'date_joined'
    )

    # Filtros laterales en el panel de administración
    list_filter = ('bloqueado', 'is_staff', 'is_superuser', 'is_active')

    # Búsqueda rápida por username o email
    search_fields = ('username', 'email')

    # Agregamos una sección exclusiva ("Control de Intentos y Bloqueo") al formulario
    # de edición de usuario en el panel admin, sumándose a los fieldsets por defecto de Django.
    fieldsets = UserAdmin.fieldsets + (
        ('Control de Intentos y Bloqueo (EVA 1)', {
            'fields': ('intentos_fallidos', 'bloqueado'),
            'description': 'Campos de auditoría de seguridad para control de ataques de fuerza bruta.'
        }),
    )
