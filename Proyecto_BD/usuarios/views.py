# ==============================================================================
# CÓDIGO EXTRAÍDO E INTEGRADO DESDE EVA 1 (MÓDULO DE AUTENTICACIÓN)
# Vistas de Registro, Inicio de Sesión, Desbloqueo y Cierre de Sesión.
# ==============================================================================

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import RegistroUsuarioForm
from .models import Usuario


def registrar_usuario(request):
    """
    Vista para procesar el registro de un nuevo usuario.
    Maneja tanto la petición GET (mostrar formulario) como POST (guardar usuario).
    """
    if request.method == 'POST':
        # Instanciamos el formulario con los datos enviados por el usuario
        formulario = RegistroUsuarioForm(request.POST)

        # triggers las validaciones definidas en forms.py (clean_contrasena, clean, etc.)
        if formulario.is_valid():
            formulario.save()  # Encripta y guarda el usuario en la BD
            messages.success(
                request,
                'Usuario registrado correctamente. Ya puedes iniciar sesión.'
            )
            return redirect('iniciar_sesion')
    else:
        # Petición GET: mostramos el formulario vacío
        formulario = RegistroUsuarioForm()

    return render(
        request,
        'usuarios/registro.html',
        {'formulario': formulario}
    )


def iniciar_sesion(request):
    """
    Vista de Login con Control de Intentos Fallidos y Bloqueo de Cuenta.
    Paso 1: Verificar si el usuario existe y si ya está bloqueado.
    Paso 2: Intentar autenticar con authenticate().
    Paso 3: Si tiene éxito -> reiniciar intentos a 0 e iniciar sesión.
    Paso 4: Si falla -> incrementar intentos_fallidos + 1 y bloquear si llega a 3.
    """
    if request.method == 'POST':
        nombre_usuario = request.POST.get('username')
        contrasena = request.POST.get('password')

        # Buscamos en la BD si existe un usuario con ese username
        usuario = Usuario.objects.filter(
            username=nombre_usuario
        ).first()

        # PASO 1: Verificar si la cuenta ya está bloqueada antes de autenticar
        if usuario and usuario.bloqueado:
            messages.error(
                request,
                'Clave bloqueada. Ha superado el máximo de intentos permitidos.'
            )
            return render(
                request,
                'usuarios/login.html',
                {'cuenta_bloqueada': True, 'usuario_bloqueado': usuario.username}
            )

        # PASO 2: Intentar autenticación con Django authenticate()
        # Valida que la contraseña coincida con el hash guardado en la BD
        usuario_autenticado = authenticate(
            request,
            username=nombre_usuario,
            password=contrasena
        )

        # PASO 3: ÉXITO EN LA AUTENTICACIÓN
        if usuario_autenticado is not None:
            # Si inició sesión exitosamente, se reinician los intentos fallidos a 0
            usuario_autenticado.intentos_fallidos = 0
            # update_fields optimiza la consulta SQL actualizando solo esta columna
            usuario_autenticado.save(update_fields=['intentos_fallidos'])

            # Inicia la sesión HTTP (guarda el ID del usuario en la sesión)
            login(request, usuario_autenticado)
            next_url = request.POST.get('next') or request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('index')

        # PASO 4: FALLO EN LA AUTENTICACIÓN
        if usuario:
            # El usuario existe, pero la contraseña fue incorrecta -> Aumentar contador
            usuario.intentos_fallidos += 1

            # Si alcanza 3 o más intentos fallidos, se bloquea la cuenta
            if usuario.intentos_fallidos >= 3:
                usuario.bloqueado = True
                usuario.save(
                    update_fields=['intentos_fallidos', 'bloqueado']
                )
                messages.error(
                    request,
                    'Clave bloqueada. Ha superado el máximo de intentos permitidos.'
                )
                return render(
                    request,
                    'usuarios/login.html',
                    {'cuenta_bloqueada': True, 'usuario_bloqueado': usuario.username}
                )
            else:
                # Si le quedan intentos (ej: 1 o 2 fallos), solo guardamos el contador
                usuario.save(update_fields=['intentos_fallidos'])
                mensajes_restantes = 3 - usuario.intentos_fallidos
                messages.error(
                    request,
                    f'Usuario o contraseña incorrectos. '
                    f'Intentos restantes: {mensajes_restantes}.'
                )
        else:
            # Principio de Seguridad: No revelar si el usuario existe o no para evitar enumeración
            messages.error(
                request,
                'Usuario o contraseña incorrectos.'
            )

    return render(request, 'usuarios/login.html')


def desbloquear_usuario(request):
    """
    Vista para desbloquear la cuenta de un usuario bloqueado.
    Permite ingresar el nombre de usuario o recibirlo desde la página de login.
    """
    if request.method == 'POST':
        nombre_usuario = request.POST.get('username')
        usuario = Usuario.objects.filter(username=nombre_usuario).first()

        if usuario:
            if usuario.bloqueado or usuario.intentos_fallidos > 0:
                usuario.bloqueado = False
                usuario.intentos_fallidos = 0
                usuario.save(update_fields=['bloqueado', 'intentos_fallidos'])
                messages.success(
                    request,
                    f'La cuenta de "{nombre_usuario}" ha sido desbloqueada exitosamente. Ya puedes iniciar sesión.'
                )
            else:
                messages.info(
                    request,
                    f'La cuenta de "{nombre_usuario}" ya se encontraba activa.'
                )
            return redirect('iniciar_sesion')
        else:
            messages.error(
                request,
                'El nombre de usuario ingresado no existe.'
            )

    usuario_predeterminado = request.GET.get('usuario', '')
    return render(
        request,
        'usuarios/desbloquear.html',
        {'usuario_predeterminado': usuario_predeterminado}
    )


@login_required
def inicio(request):
    """
    Dashboard o Vista Principal del sistema.
    Protegida con el decorador @login_required.
    Si un usuario no autenticado intenta acceder, Django lo redirige a LOGIN_URL ('/login/').
    """
    return render(request, 'usuarios/inicio.html')


def cerrar_sesion(request):
    """
    Vista para cerrar la sesión activa del usuario (destruye las cookies de sesión).
    """
    logout(request)
    return redirect('iniciar_sesion')
