"""
========================================================================================
ARCHIVO DE CONFIGURACIÓN PRINCIPAL DE DJANGO: settings.py
========================================================================================
Este archivo contiene todos los parámetros de configuración del proyecto "Proyecto_BD".

¿QUÉ VIENE POR DEFECTO?
- Clave secreta (SECRET_KEY), modo depuración (DEBUG=True).
- Lista inicial de aplicaciones del núcleo de Django (admin, auth, sessions, messages, etc.).
- Middlewares estándar de seguridad, sesiones y autenticación.
- Motor de plantillas (TEMPLATES) y configuración de base de datos SQLite3.
- Validadores de contraseñas nativos e internacionalización.

¿QUÉ DESARROLLAMOS / CONFIGURAMOS NOSOTROS?
1. Registro de nuestras dos aplicaciones en INSTALLED_APPS:
   - 'usuarios': Creada en EVA 1 para autenticación y control de bloqueos.
   - 'productos': Creada en EVA 2 (Guía 1 Unidad 2) para el CRUD de productos.
2. Definición del modelo de usuario personalizado:
   - AUTH_USER_MODEL = 'usuarios.Usuario' (permite añadir los campos intentos_fallidos y bloqueado).
3. Rutas de redirección para la Etapa 3 (Enlace de seguridad):
   - LOGIN_URL: Ruta donde Django redirige a usuarios no autenticados cuando intentan entrar al CRUD.
   - LOGIN_REDIRECT_URL: Ruta a donde va el usuario tras logearse exitosamente.
   - LOGOUT_REDIRECT_URL: Ruta a donde va tras cerrar sesión.
========================================================================================
"""

from pathlib import Path

# BASE_DIR: Ruta absoluta hacia la raíz del proyecto Django (/Proyecto_BD)
# Se utiliza para construir rutas relativas a archivos como la BD SQLite o carpetas de templates.
BASE_DIR = Path(__file__).resolve().parent.parent


# ==============================================================================
# 1. AJUSTES BÁSICOS DE SEGURIDAD Y ENTORNO (Vienen por defecto de Django)
# ==============================================================================

# Clave criptográfica para firmas de cookies y tokens CSRF.
SECRET_KEY = 'django-insecure-ccds^176v^v(c=@-sh(1i_gg2r+#@tzki1#va-6o(!4@#_!0@p'

# DEBUG=True: Muestra errores detallados en pantalla durante el desarrollo.
# IMPORTANTE: En producción real debe cambiarse a False para no exponer código ni variables.
DEBUG = True

# Dominios autorizados para servir la aplicación. Vacío [] permite localhost/127.0.0.1 en modo DEBUG.
ALLOWED_HOSTS = []


# ==============================================================================
# 2. APLICACIONES INSTALADAS (INSTALLED_APPS)
# ==============================================================================
INSTALLED_APPS = [
    # --- Aplicaciones nativas provistas por defecto por Django ---
    'django.contrib.admin',         # Panel de administración interactivo
    'django.contrib.auth',          # Framework base de autenticación y permisos
    'django.contrib.contenttypes',   # Sistema de tipos de contenido para modelos
    'django.contrib.sessions',       # Manejo de sesiones de usuario HTTP
    'django.contrib.messages',       # Framework para mensajes temporales (flash messages)
    'django.contrib.staticfiles',    # Manejo de archivos estáticos (CSS, JS, imágenes)

    # --- Aplicaciones desarrolladas por nosotros ---
    # EVA 1: Módulo de gestión de usuarios, registro, login y bloqueo por 3 intentos
    'usuarios',
    
    # EVA 2 (Guía 1 - Paso II): Módulo CRUD de productos (ID, Nombre, Marca, Precio)
    'productos',
]


# ==============================================================================
# 3. MIDDLEWARES (Capas intermedias de procesamiento de peticiones HTTP)
# ==============================================================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',            # Seguridad HTTP básica
    'django.contrib.sessions.middleware.SessionMiddleware',      # Habilita sesiones basadas en cookies
    'django.middleware.common.CommonMiddleware',                # Manejo común de URLs y barras finales
    'django.middleware.csrf.CsrfViewMiddleware',                # Protección contra ataques CSRF (Cross-Site Request Forgery)
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Asocia el usuario autenticado a request.user
    'django.contrib.messages.middleware.MessageMiddleware',      # Permite guardar mensajes entre peticiones
    'django.middleware.clickjacking.XFrameOptionsMiddleware',    # Protección contra ataques de secuestro de clic
]

# Archivo de enrutamiento principal donde se definen las rutas globales
ROOT_URLCONF = 'config.urls'


# ==============================================================================
# 4. MOTOR DE PLANTILLAS / TEMPLATES (Guía 2)
# ==============================================================================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # Carpetas globales de templates (vacío porque usamos APP_DIRS=True)
        'APP_DIRS': True,  # Permite a Django buscar automáticamente dentro de cada carpeta "templates" de cada app
        'OPTIONS': {
            'context_processors': [
                # Procesadores que inyectan variables automáticamente en todos los templates HTML
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',      # Inyecta {{ user }} o {{ request.user }}
                'django.contrib.messages.context_processors.messages',  # Inyecta la lista {{ messages }}
            ],
        },
    },
]

# Punto de entrada para servidores web WSGI en producción
WSGI_APPLICATION = 'config.wsgi.application'


# ==============================================================================
# 5. BASE DE DATOS (Guía 1 - Paso III)
# ==============================================================================
# Por defecto Django incluye SQLite3. No requiere instalar un servidor externo
# y almacena toda la información relacional en el archivo "db.sqlite3".
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ==============================================================================
# 6. VALIDADORES DE CONTRASEÑAS (Por defecto en Django)
# ==============================================================================
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# ==============================================================================
# 7. INTERNACIONALIZACIÓN Y ZONA HORARIA
# ==============================================================================
LANGUAGE_CODE = 'es-cl'  # Idioma en español para formularios y mensajes de validación
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True


# ==============================================================================
# 8. ARCHIVOS ESTÁTICOS (CSS, JAVASCRIPT, IMÁGENES)
# ==============================================================================
STATIC_URL = 'static/'


# ==============================================================================
# 9. CONFIGURACIONES DESARROLLADAS PARA EVA 1 Y EVA 2 (SEGURIDAD Y ENLACE)
# ==============================================================================

# Backend de correo en consola (útil para pruebas de recuperación/notificación sin servidor SMTP)
MAILERS = {
    'default': {
        'BACKEND': 'django.core.mail.backends.console.EmailBackend',
    },
}

# 1. Indicamos a Django que use nuestro modelo personalizado de Usuario heredado de AbstractUser.
# Esto permite que la autenticación gestione los campos de intentos_fallidos y bloqueo en la BD.
AUTH_USER_MODEL = 'usuarios.Usuario'

# 2. Ruta a la que Django redirige cuando un usuario anónimo intenta acceder a una vista protegida con @login_required (Etapa 3 de EVA 2)
LOGIN_URL = '/login/'

# 3. Ruta a la que se redirige al usuario tras completar exitosamente el login
LOGIN_REDIRECT_URL = '/'

# 4. Ruta a la que se redirige tras cerrar sesión
LOGOUT_REDIRECT_URL = '/login/'

