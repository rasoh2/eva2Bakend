# ==============================================================================
# CÓDIGO EXTRAÍDO E INTEGRADO DESDE EVA 1 (MÓDULO DE AUTENTICACIÓN)
# Modelo de Usuario personalizado con control de intentos fallidos y bloqueo.
# ==============================================================================

from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    """
    Modelo de Usuario Personalizado.
    Hereda de AbstractUser para mantener todos los campos nativos de Django
    (username, password, first_name, last_name, etc.) y añadir campos
    personalizados requeridos para la lógica de seguridad y bloqueo.
    """

    # Campo de correo electrónico único obligatorio para evitar duplicados
    email = models.EmailField(unique=True)

    # Contador de intentos fallidos de inicio de sesión consecutivos (comienza en 0)
    intentos_fallidos = models.PositiveSmallIntegerField(default=0)

    # Booleano que indica si la cuenta está suspendida por exceder 3 intentos
    bloqueado = models.BooleanField(default=False)