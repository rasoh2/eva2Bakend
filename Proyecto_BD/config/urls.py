from django.contrib import admin
from django.urls import path, include
from productos import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Módulo de Autenticación y Usuarios (EVA 1)
    path('', include('usuarios.urls')),

    # Módulo CRUD de Productos (EVA 2)
    path('', views.mostrarIndex, name='index'),
    path('form_registrar', views.mostrarFormRegistrar, name='form_registrar'),
    path('insertar', views.insertarProducto, name='insertar'),
    path('listado', views.mostrarListado, name='listado'),
    path('form_actualizar/<int:id>', views.mostrarFormActualizar, name='form_actualizar'),
    path('actualizar/<int:id>', views.actualizarProducto, name='actualizar'),
    path('eliminar/<int:id>', views.eliminarProducto, name='eliminar'),
]
