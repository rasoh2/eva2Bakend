# ==============================================================================
# EVA 1: RUTAS DEL MÓDULO DE AUTENTICACIÓN Y USUARIOS (urls.py)
# ==============================================================================
# Este archivo define las URLs específicas para la aplicación 'usuarios'.
# Es incluido en el archivo principal 'config/urls.py' mediante include('usuarios.urls').
#
# Cada path() vincula una cadena de URL relativa con una función en 'views.py'
# y le asigna un 'name' único para permitir la resolución inversa mediante {% url '...' %}.
# ==============================================================================

from django.urls import path
from . import views

urlpatterns = [
    # Ruta: /registro/ -> Muestra y procesa el formulario de alta de nuevo usuario
    path('registro/', views.registrar_usuario, name='registrar_usuario'),

    # Ruta: /login/ -> Formulario de inicio de sesión con control de 3 intentos fallidos
    path('login/', views.iniciar_sesion, name='iniciar_sesion'),

    # Ruta: /logout/ -> Finaliza la sesión del usuario y redirige al login
    path('logout/', views.cerrar_sesion, name='cerrar_sesion'),

    # Ruta: /desbloquear/ -> Formulario para rehabilitar cuentas suspendidas por fallos
    path('desbloquear/', views.desbloquear_usuario, name='desbloquear_usuario'),

    # Ruta: /inicio/ -> Dashboard interno de bienvenida del usuario
    path('inicio/', views.inicio, name='inicio'),
]