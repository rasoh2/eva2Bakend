# ==============================================================================
# EVA 2 - GUÍAS 02 Y 03 (UNIDAD 2): VISTAS DEL MÓDULO CRUD DE PRODUCTOS
# ==============================================================================
# Este archivo contiene las funciones que procesan las peticiones HTTP y ejecutan
# la lógica de negocio (CRUD: Create, Read, Update, Delete) sobre la base de datos.
#
# ETAPA 3 (EVA 2 - ENLACE DE SEGURIDAD):
# Todas las vistas del módulo de productos están decoradas con `@login_required`.
# Si un usuario anónimo intenta acceder a cualquier URL de productos, Django
# intercepta la petición y lo redirige automáticamente a '/login/' (LOGIN_URL).
# ==============================================================================

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from productos.models import Producto


# ------------------------------------------------------------------------------
# 1. VISTA: MENÚ PRINCIPAL / INDEX (Guía 2 - Paso 4)
# ------------------------------------------------------------------------------
@login_required
def mostrarIndex(request):
    """
    Renderiza la página principal (index.html) del módulo de productos.
    Muestra botones de acceso directo al registro y al listado, además de
    información del usuario autenticado (request.user).
    """
    return render(request, 'index.html')


# ------------------------------------------------------------------------------
# 2. VISTA: LISTADO DE PRODUCTOS - READ (Guía 2 - Paso 4 y Guía 3)
# ------------------------------------------------------------------------------
@login_required
def mostrarListado(request):
    """
    Operación READ (Leer / Consultar) del CRUD.
    Obtiene todos los registros de la tabla 'productos_producto' usando el ORM:
    Producto.objects.all() equivale a ejecutar: SELECT * FROM productos_producto;
    Los envía como diccionario de contexto {'productos': productos} al template 'listado.html'.
    """
    productos = Producto.objects.all()
    return render(request, 'listado.html', {'productos': productos})


# ------------------------------------------------------------------------------
# 3. VISTA: MOSTRAR FORMULARIO DE REGISTRO (Guía 2 - Paso 4)
# ------------------------------------------------------------------------------
@login_required
def mostrarFormRegistrar(request):
    """
    Muestra la plantilla vacía 'form_registrar.html' para ingresar un nuevo producto.
    Se ejecuta al recibir una petición HTTP GET.
    """
    return render(request, 'form_registrar.html')


# ------------------------------------------------------------------------------
# 4. VISTA: INSERTAR PRODUCTO EN LA BASE DE DATOS - CREATE (Guía 3 - Paso 3)
# ------------------------------------------------------------------------------
@login_required
def insertarProducto(request):
    """
    Operación CREATE (Crear / Insertar) del CRUD.
    Se activa cuando el usuario presiona el botón 'Guardar Datos' en el formulario.
    1. Verifica que el método HTTP sea POST.
    2. Extrae los valores de los inputs por su atributo 'name':
       - 'txtnom': Nombre del producto.
       - 'cbomar': Marca seleccionada en el <select>.
       - 'txtpre': Precio ingresado en el input numérico.
    3. Crea una instancia de Producto con los datos recibidos.
    4. Ejecuta pro.save(), que genera la sentencia SQL INSERT INTO.
    5. Retorna al template con una alerta de éxito ('msjOk') o error ('msjErr').
    """
    if request.method == 'POST':
        # Extracción de parámetros enviados en el cuerpo del formulario
        nom = request.POST.get('txtnom')
        mar = request.POST.get('cbomar')
        pre = request.POST.get('txtpre')

        # Instanciación y guardado del registro en la BD SQLite3
        pro = Producto(nombre=nom, marca=mar, precio=pre)
        pro.save()

        # Mensaje de confirmación transmitido al template (alerta Bootstrap)
        datos = {'msjOk': 'Registro grabado exitosamente'}
        return render(request, 'form_registrar.html', datos)
    else:
        # En caso de acceso indebido mediante GET directamente a la URL /insertar
        datos = {'msjErr': 'La solicitud no se puede procesar !!'}
        return render(request, 'form_registrar.html', datos)


# ------------------------------------------------------------------------------
# 5. VISTA: MOSTRAR FORMULARIO DE ACTUALIZACIÓN (Guía 2 & Guía 3)
# ------------------------------------------------------------------------------
@login_required
def mostrarFormActualizar(request, id):
    """
    Carga el formulario de edición ('form_actualizar.html') pre-llenado con los
    datos del producto seleccionado por su 'id'.
    get_object_or_404 busca el producto en la BD; si no existe, devuelve error 404
    de forma segura en lugar de provocar una excepción no controlada.
    """
    pro = get_object_or_404(Producto, id=id)
    return render(request, 'form_actualizar.html', {'producto': pro})


# ------------------------------------------------------------------------------
# 6. VISTA: ACTUALIZAR PRODUCTO EN LA BASE DE DATOS - UPDATE (Guía 3)
# ------------------------------------------------------------------------------
@login_required
def actualizarProducto(request, id):
    """
    Operación UPDATE (Modificar / Actualizar) del CRUD.
    1. Obtiene la instancia existente del producto según el 'id' recibido en la URL.
    2. Sobrescribe los atributos (nombre, marca, precio) con los nuevos valores del POST.
    3. Llama a pro.save(), que genera la sentencia SQL UPDATE.
    4. Redirige al usuario a la vista de 'listado' para visualizar los cambios aplicados.
    """
    if request.method == 'POST':
        pro = get_object_or_404(Producto, id=id)
        pro.nombre = request.POST.get('txtnom')
        pro.marca = request.POST.get('cbomar')
        pro.precio = request.POST.get('txtpre')
        pro.save()
        return redirect('listado')
    return redirect('listado')


# ------------------------------------------------------------------------------
# 7. VISTA: ELIMINAR PRODUCTO DE LA BASE DE DATOS - DELETE (Guía 3)
# ------------------------------------------------------------------------------
@login_required
def eliminarProducto(request, id):
    """
    Operación DELETE (Eliminar / Borrar) del CRUD.
    1. Localiza el producto por su 'id'.
    2. Ejecuta pro.delete(), que ejecuta la sentencia SQL DELETE FROM productos_producto WHERE id = ...
    3. Redirige al usuario a la vista de 'listado' donde el producto ya no figurará.
    """
    pro = get_object_or_404(Producto, id=id)
    pro.delete()
    return redirect('listado')