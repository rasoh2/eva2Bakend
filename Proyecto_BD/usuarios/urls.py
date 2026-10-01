# ==============================================================================
# CÓDIGO EXTRAÍDO E INTEGRADO DESDE EVA 1 (MÓDULO DE AUTENTICACIÓN)
# Rutas de navegación para autenticación de usuarios.
# ==============================================================================

from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.registrar_usuario, name='registrar_usuario'),
    path('login/', views.iniciar_sesion, name='iniciar_sesion'),
    path('logout/', views.cerrar_sesion, name='cerrar_sesion'),
    path('desbloquear/', views.desbloquear_usuario, name='desbloquear_usuario'),
]