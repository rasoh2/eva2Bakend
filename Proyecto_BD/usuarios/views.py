# ==============================================================================
# EVA 1 Y EVA 2 (ETAPA 1): VISTAS DE AUTENTICACIÓN Y SEGURIDAD (views.py)
# ==============================================================================
# Este módulo gestiona todo el ciclo de vida de las sesiones y la seguridad:
# 1. Registro de usuarios con validaciones de complejidad.
# 2. Inicio de sesión con algoritmo de bloqueo de 3 intentos fallidos en BD.
# 3. Desbloqueo de cuentas bloqueadas.
# 4. Cierre seguro de sesión (logout).
# ==============================================================================

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import RegistroUsuarioForm
from .models import Usuario


# ------------------------------------------------------------------------------
# 1. VISTA: REGISTRO DE USUARIOS (EVA 1)
# ------------------------------------------------------------------------------
def registrar_usuario(request):
    """
    Controla el proceso de alta/creación de una nueva cuenta de usuario.
    - GET: Entrega el formulario 'RegistroUsuarioForm' vacío al template.
    - POST: Recibe los datos, los valida contra las reglas de forms.py y models.py.
      Si es válido: hashea la contraseña, guarda en BD y redirige al login con mensaje.
      Si es inválido: re-renderiza el formulario mostrando los errores específicos.
    """
    if request.method == 'POST':
        formulario = RegistroUsuarioForm(request.POST)
        if formulario.is_valid():
            # Dispara save() que encripta la contraseña con PBKDF2 y persiste en SQLite
            formulario.save()
            messages.success(
                request,
                '¡Usuario registrado exitosamente! Ya puedes iniciar sesión con tus credenciales.'
            )
            return redirect('iniciar_sesion')
    else:
        formulario = RegistroUsuarioForm()

    return render(
        request,
        'usuarios/registro.html',
        {'formulario': formulario}
    )


# ------------------------------------------------------------------------------
# 2. VISTA: INICIO DE SESIÓN CON CONTROL DE INTENTOS FALLIDOS (EVA 1)
# ------------------------------------------------------------------------------
def iniciar_sesion(request):
    """
    Implementa el Algoritmo de Seguridad exigido en la pauta de EVA 1:
    
    [PASO 1] - VERIFICACIÓN DE ESTADO PREVIO:
      Busca al usuario por su 'username'. Si existe y su campo 'bloqueado' es True,
      rechaza el acceso de inmediato:
      "Clave bloqueada. Ha superado el máximo de intentos permitidos."
    
    [PASO 2] - AUTENTICACIÓN CON DJANGO:
      Invoca authenticate(request, username, password). Compara el hash seguro.
    
    [PASO 3] - AUTENTICACIÓN EXITOSA:
      - Reinicia el contador de 'intentos_fallidos' a 0.
      - Inicia la sesión HTTP con login(request, usuario).
      - Redirige a la vista principal (index) o a la URL previa solicitada (next).
    
    [PASO 4] - AUTENTICACIÓN FALLIDA:
      - Si el usuario existe en la BD: incrementa intentos_fallidos + 1.
        * Si alcanza 3 intentos: cambia bloqueado = True en la BD SQLite.
        * Si aún le quedan intentos: informa los intentos restantes (ej: 2 restantes).
      - Si el usuario no existe: emite mensaje genérico para evitar enumeración.
    """
    if request.method == 'POST':
        nombre_usuario = request.POST.get('username', '').strip()
        contrasena = request.POST.get('password', '')

        # Consulta ORM para obtener el usuario
        usuario = Usuario.objects.filter(username=nombre_usuario).first()

        # PASO 1: Comprobar si la cuenta ya se encuentra bloqueada en la Base de Datos
        if usuario and usuario.bloqueado:
            messages.error(
                request,
                'Clave bloqueada. Ha superado el máximo de intentos permitidos.'
            )
            return render(
                request,
                'usuarios/login.html',
                {
                    'cuenta_bloqueada': True,
                    'usuario_bloqueado': usuario.username
                }
            )

        # PASO 2: Intentar la autenticación criptográfica
        usuario_autenticado = authenticate(
            request,
            username=nombre_usuario,
            password=contrasena
        )

        # PASO 3: ÉXITO - Las credenciales son correctas
        if usuario_autenticado is not None:
            # Regla de negocio: Al acertar la clave, se reinicia el contador de errores
            usuario_autenticado.intentos_fallidos = 0
            usuario_autenticado.save(update_fields=['intentos_fallidos'])

            # Crea la cookie de sesión cifrada en el navegador del cliente
            login(request, usuario_autenticado)

            # Redirección inteligente: si venía intentando entrar a una página protegida (next)
            next_url = request.POST.get('next') or request.GET.get('next')
            if next_url:
                return redirect(next_url)
            
            # De lo contrario va al menú principal del CRUD de productos
            return redirect('index')

        # PASO 4: FALLO - Contraseña equivocada o usuario inexistente
        if usuario:
            # El usuario existe pero la contraseña fue incorrecta: sumar intento fallido
            usuario.intentos_fallidos += 1

            if usuario.intentos_fallidos >= 3:
                # Regla de seguridad: Al 3er fallo consecutivo se bloquea la cuenta en la BD
                usuario.bloqueado = True
                usuario.save(update_fields=['intentos_fallidos', 'bloqueado'])
                
                messages.error(
                    request,
                    'Clave bloqueada. Ha superado el máximo de intentos permitidos.'
                )
                return render(
                    request,
                    'usuarios/login.html',
                    {
                        'cuenta_bloqueada': True,
                        'usuario_bloqueado': usuario.username
                    }
                )
            else:
                # Aún tiene 1 o 2 intentos restantes
                usuario.save(update_fields=['intentos_fallidos'])
                restantes = 3 - usuario.intentos_fallidos
                messages.error(
                    request,
                    f'Usuario o contraseña incorrectos. Te quedan {restantes} intento(s) antes del bloqueo.'
                )
        else:
            # Buenas prácticas de ciberseguridad: no confirmar si el usuario existe o no
            messages.error(
                request,
                'Usuario o contraseña incorrectos.'
            )

    return render(request, 'usuarios/login.html')


# ------------------------------------------------------------------------------
# 3. VISTA: DESBLOQUEO DE CUENTA (EVA 1)
# ------------------------------------------------------------------------------
def desbloquear_usuario(request):
    """
    Permite restablecer una cuenta suspendida tras superar los 3 intentos.
    Al confirmar el nombre de usuario, restablece:
    - bloqueado = False
    - intentos_fallidos = 0
    y persiste la modificación en la base de datos SQLite.
    """
    if request.method == 'POST':
        nombre_usuario = request.POST.get('username', '').strip()
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
                    f'La cuenta de "{nombre_usuario}" ya se encontraba activa y sin bloqueos.'
                )
            return redirect('iniciar_sesion')
        else:
            messages.error(
                request,
                f'El nombre de usuario "{nombre_usuario}" no existe en la base de datos.'
            )

    # Si se pasó el nombre de usuario por parámetro GET (ej: ?usuario=pedro), se pre-llena
    usuario_predeterminado = request.GET.get('usuario', '')
    return render(
        request,
        'usuarios/desbloquear.html',
        {'usuario_predeterminado': usuario_predeterminado}
    )


# ------------------------------------------------------------------------------
# 4. VISTA: INICIO / DASHBOARD ALTERNATIVO DE USUARIOS (EVA 1)
# ------------------------------------------------------------------------------
@login_required
def inicio(request):
    """
    Vista alternativa de bienvenida para el módulo de usuarios.
    Protegida mediante @login_required.
    """
    return render(request, 'usuarios/inicio.html')


# ------------------------------------------------------------------------------
# 5. VISTA: CIERRE DE SESIÓN (LOGOUT)
# ------------------------------------------------------------------------------
def cerrar_sesion(request):
    """
    Cierra la sesión activa:
    1. Invalida la sesión actual en la tabla 'django_session'.
    2. Elimina la cookie 'sessionid' del cliente.
    3. Redirige a la pantalla de login con un mensaje informativo.
    """
    logout(request)
    messages.info(request, 'Has cerrado tu sesión de forma segura.')
    return redirect('iniciar_sesion')