"""
========================================================================================
ENRUTADOR PRINCIPAL DEL PROYECTO: config/urls.py
========================================================================================
Este archivo define el mapeo entre las URLs que el usuario ingresa en el navegador
y las funciones de vista (views) que responderán a esas peticiones.

¿CÓMO FUNCIONA EL ENRUTAMIENTO EN DJANGO?
1. Cuando llega una petición HTTP (ej: http://127.0.0.1:8000/listado), Django lee
   ROOT_URLCONF definido en settings.py ('config.urls').
2. Recorre la lista 'urlpatterns' de arriba hacia abajo buscando la primera coincidencia.
3. Si la ruta coincide, ejecuta la función asociada pasándole el objeto 'request'.

¿QUÉ CONECTA ESTE ARCHIVO?
- include('usuarios.urls'): Conecta todas las rutas del módulo de autenticación (EVA 1).
- Rutas de productos: Conecta las vistas CRUD de la Guía 2 y Guía 3 (EVA 2).
========================================================================================
"""

from django.contrib import admin
from django.urls import path, include
from productos import views

urlpatterns = [
    # --------------------------------------------------------------------------
    # Panel de administración nativo de Django
    # --------------------------------------------------------------------------
    path('admin/', admin.site.urls),

    # --------------------------------------------------------------------------
    # MÓDULO DE AUTENTICACIÓN Y SEGURIDAD (EVA 1)
    # Incluye las rutas delegadas a la app 'usuarios' (/login/, /registro/, etc.)
    # --------------------------------------------------------------------------
    path('', include('usuarios.urls')),

    # --------------------------------------------------------------------------
    # MÓDULO CRUD DE PRODUCTOS (EVA 2 - GUÍAS 1, 2 Y 3)
    # --------------------------------------------------------------------------
    # Guía 2 - Paso 5: Vista de inicio / menú principal
    path('', views.mostrarIndex, name='index'),

    # Guía 2 & 3: Mostrar formulario para registrar un nuevo producto
    path('form_registrar', views.mostrarFormRegistrar, name='form_registrar'),

    # Guía 3 - Paso 3: Procesa el POST del formulario para guardar en la BD SQLite
    path('insertar', views.insertarProducto, name='insertar'),

    # Guía 2 & 3: Muestra la tabla con todos los productos registrados en la BD
    path('listado', views.mostrarListado, name='listado'),

    # Guía 2 & 3: Carga el formulario con los datos del producto seleccionado por su ID
    path('form_actualizar/<int:id>', views.mostrarFormActualizar, name='form_actualizar'),

    # Guía 3: Procesa la actualización de los datos del producto en la BD
    path('actualizar/<int:id>', views.actualizarProducto, name='actualizar'),

    # Guía 3: Elimina el registro del producto identificado por su ID
    path('eliminar/<int:id>', views.eliminarProducto, name='eliminar'),
]
