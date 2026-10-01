# ==============================================================================
# EVA 2: REGISTRO DEL MODELO PRODUCTO EN EL PANEL DE ADMINISTRACIÓN DE DJANGO
# ==============================================================================
# Django incluye por defecto un poderoso panel de administración en /admin/.
# Para que un modelo aparezca y pueda ser gestionado allí, debemos registrarlo
# en admin.py usando admin.site.register() o el decorador @admin.register().
# ==============================================================================

from django.contrib import admin
from productos.models import Producto


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    """
    Configuración personalizada del modelo Producto para el Django Admin.
    Permite visualizar las columnas ID, Nombre, Marca y Precio en forma de tabla,
    añadir barra de búsqueda y filtros laterales.
    """
    list_display = ('id', 'nombre', 'marca', 'precio')
    search_fields = ('nombre', 'marca')
    list_filter = ('marca',)
    ordering = ('id',)
