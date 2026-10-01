# ==============================================================================
# PRUEBAS AUTOMATIZADAS DEL MÓDULO CRUD DE PRODUCTOS (productos/tests.py)
# ==============================================================================
# Estas pruebas verifican:
# 1. Enlace de seguridad (Etapa 3 de EVA 2): El CRUD exige sesión iniciada (@login_required).
# 2. Operaciones CRUD (Guía 1 a 3):
#    - Create: Insertar producto en base de datos.
#    - Read: Listar productos existentes.
#    - Update: Modificar un producto por su ID.
#    - Delete: Eliminar un producto por su ID.
# ==============================================================================

from django.test import TestCase, Client
from django.urls import reverse
from usuarios.models import Usuario
from productos.models import Producto


class ProductoCrudTests(TestCase):
    """Batería de pruebas para el módulo de inventario y CRUD de productos."""

    def setUp(self):
        """Crea usuario para pruebas de autenticación y cliente HTTP."""
        self.client = Client()
        self.usuario = Usuario.objects.create_user(
            username='operador',
            email='operador@inacap.cl',
            password='Password123'
        )
        self.producto = Producto.objects.create(
            nombre='Leche Entera 1L',
            marca='Lider',
            precio=1050
        )

    # --------------------------------------------------------------------------
    # ETAPA 3 (EVA 2): Verificación de protección con @login_required
    # --------------------------------------------------------------------------
    def test_rutas_crud_protegidas_sin_login(self):
        """
        Verifica que usuarios anónimos sean redirigidos a /login/
        al intentar entrar al index, listado o formulario de registro.
        """
        rutas = [
            '/',
            '/listado',
            '/form_registrar',
            f'/form_actualizar/{self.producto.id}',
        ]
        for ruta in rutas:
            respuesta = self.client.get(ruta)
            # Debe responder con redirección (302) hacia LOGIN_URL
            self.assertEqual(respuesta.status_code, 302)
            self.assertIn('/login/', respuesta.url)

    # --------------------------------------------------------------------------
    # OPERACIONES CRUD CON SESIÓN INICIADA (Guías 1 a 3)
    # --------------------------------------------------------------------------
    def test_insertar_producto(self):
        """Guía 3: Prueba la inserción de un nuevo registro por POST a /insertar."""
        self.client.force_login(self.usuario)

        respuesta = self.client.post('/insertar', {
            'txtnom': 'Arroz Grado 1',
            'cbomar': 'A cuenta',
            'txtpre': '990'
        })
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, 'Registro grabado exitosamente')

        # Comprobación directa en la base de datos SQLite
        existe = Producto.objects.filter(nombre='Arroz Grado 1', marca='A cuenta').exists()
        self.assertTrue(existe)

    def test_listar_productos(self):
        """Guía 2 & 3: Prueba la visualización de registros en la plantilla listado.html."""
        self.client.force_login(self.usuario)

        respuesta = self.client.get('/listado')
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, 'Leche Entera 1L')
        self.assertContains(respuesta, 'Lider')
        self.assertContains(respuesta, '$1050')

    def test_actualizar_producto(self):
        """Guía 3: Prueba la modificación de un registro existente vía POST."""
        self.client.force_login(self.usuario)

        url_actualizar = f'/actualizar/{self.producto.id}'
        respuesta = self.client.post(url_actualizar, {
            'txtnom': 'Leche Descremada 1L',
            'cbomar': 'Jumbo',
            'txtpre': '1290'
        })
        # Debe redirigir al listado
        self.assertEqual(respuesta.status_code, 302)

        # Verificamos los cambios en SQLite
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.nombre, 'Leche Descremada 1L')
        self.assertEqual(self.producto.marca, 'Jumbo')
        self.assertEqual(self.producto.precio, 1290)

    def test_eliminar_producto(self):
        """Guía 3: Prueba el borrado de un registro en la base de datos."""
        self.client.force_login(self.usuario)

        url_eliminar = f'/eliminar/{self.producto.id}'
        respuesta = self.client.get(url_eliminar)
        self.assertEqual(respuesta.status_code, 302)

        # El producto ya no debe existir en la BD
        existe = Producto.objects.filter(id=self.producto.id).exists()
        self.assertFalse(existe)
