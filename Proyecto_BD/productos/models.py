# ==============================================================================
# EVA 2 - GUÍA 01 (UNIDAD 2): DEFINICIÓN DE MODELOS Y ORM EN DJANGO
# ==============================================================================
# En Django, los "Modelos" son clases de Python que representan tablas de la BD.
# El ORM (Object-Relational Mapping) de Django se encarga de traducir esta clase
# en sentencias SQL compatibles con SQLite, MySQL o PostgreSQL.
#
# Según la Guía 1 (Paso IV):
# "Dentro de models.py creamos la siguiente clase... una clase es una tabla de la BD"
# "El id lo crea por defecto el Framework Django trabajando para ti"
# Tabla generada en SQLite: 'productos_producto' (nombre_app + '_' + nombre_clase)
# ==============================================================================

from django.db import models


class Producto(models.Model):
    """
    Modelo que representa un Producto en el inventario.
    Campos requeridos por la pauta de evaluación EVA 2 (Etapa 2):
    - id: Llave primaria (Primary Key) autoincremental creada automáticamente por Django.
    - nombre: Texto con el nombre descriptivo del producto (máximo 100 caracteres).
    - marca: Cadena de texto indicando la marca del producto (ej: 'A cuenta', 'Lider', 'Jumbo').
    - precio: Número entero que representa el valor monetario (no permite nulos).
    """

    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    precio = models.IntegerField(null=False)

    def __str__(self):
        """
        Representación en texto legible del objeto Producto.
        Facilita la visualización en el panel administrativo o en la consola de depuración.
        """
        return f"{self.nombre} ({self.marca}) - ${self.precio}"