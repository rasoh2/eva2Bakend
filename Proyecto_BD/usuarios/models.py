# ==============================================================================
# EVA 1 Y EVA 2 (ETAPA 1): MODELO DE USUARIO PERSONALIZADO (models.py)
# ==============================================================================
# ENUNCIADO EVA 1:
# "Registro de usuarios: Nombre de usuario, Correo electrónico, Contraseña...
#  Validación de usuario único. Validación de correo único.
#  Control de intentos fallidos: Registrar intentos incorrectos.
#  Al tercer intento fallido: 'Clave bloqueada. Ha superado el máximo de intentos permitidos.'
#  Idealmente, el bloqueo debería quedar almacenado en la base de datos y no solamente
#  en JavaScript, porque es una regla de seguridad del backend."
#
# ETAPA 1 (EVA 2):
# "Proyecto LOGIN (EVA1), el cual debe incluir manejo de usuarios con BD."
#
# ¿POR QUÉ HEREDAMOS DE AbstractUser?
# Django provee 'AbstractUser', una clase base que incluye toda la infraestructura
# probada de autenticación: hashing seguro de contraseñas (PBKDF2), gestión de permisos,
# campos username, first_name, last_name, is_staff, is_active, etc.
# Al heredar de AbstractUser, evitamos reinventar la rueda y únicamente agregamos
# las columnas que nuestra aplicación necesita específicamente.
# ==============================================================================

from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    """
    Modelo de Usuario Personalizado para el sistema.
    Extiende AbstractUser para registrar intentos fallidos y estado de bloqueo
    directamente en la tabla de la base de datos relacional (db.sqlite3).
    """

    # 1. Correo electrónico único obligatorio (Requisito EVA 1)
    # unique=True: Crea un índice UNIQUE a nivel de BD; si se intenta registrar
    # un correo ya existente, la base de datos o el formulario rechazan la operación.
    email = models.EmailField(
        unique=True,
        verbose_name="Correo Electrónico",
        help_text="Dirección de correo electrónico única para cada cuenta."
    )

    # 2. Contador de intentos fallidos consecutivos de inicio de sesión (Requisito EVA 1)
    # Inicia en 0. Se incrementa +1 cada vez que se ingresa una contraseña incorrecta.
    # Si el login es exitoso, vuelve inmediatamente a 0.
    intentos_fallidos = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Intentos Fallidos",
        help_text="Contador de fallos de contraseña consecutivos. Máximo permitido: 3."
    )

    # 3. Bandera de bloqueo de cuenta en base de datos (Requisito EVA 1)
    # Se establece en True cuando 'intentos_fallidos' alcanza o supera 3.
    # Mientras esté en True, el usuario no podrá autenticarse hasta ser desbloqueado.
    bloqueado = models.BooleanField(
        default=False,
        verbose_name="Cuenta Bloqueada",
        help_text="Indica si la cuenta ha sido suspendida por exceso de intentos fallidos."
    )

    class Meta:
        verbose_name = "Usuario del Sistema"
        verbose_name_plural = "Usuarios del Sistema"

    def __str__(self):
        """Representación legible del usuario (ej: 'admin (Activo)' o 'pedro (BLOQUEADO)')"""
        estado = "BLOQUEADO" if self.bloqueado else "Activo"
        return f"{self.username} ({self.email}) - [{estado}]"