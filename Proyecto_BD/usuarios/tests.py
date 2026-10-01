# ==============================================================================
# PRUEBAS AUTOMATIZADAS DEL MÓDULO DE USUARIOS Y SEGURIDAD (usuarios/tests.py)
# ==============================================================================
# Estas pruebas verifican automáticamente el cumplimiento de los requerimientos
# de EVA 1 y EVA 2 (Etapa 1):
# 1. Reglas de validación de contraseñas (8 caracteres, 1 mayúscula, 1 número).
# 2. Algoritmo de bloqueo al tercer intento fallido en base de datos.
# 3. Restablecimiento de cuenta mediante la vista de desbloqueo.
# ==============================================================================

from django.test import TestCase, Client
from django.urls import reverse
from usuarios.models import Usuario
from usuarios.forms import RegistroUsuarioForm


class UsuarioSeguridadTests(TestCase):
    """Batería de pruebas unitarias y de integración para autenticación y seguridad."""

    def setUp(self):
        """Prepara el entorno creando un cliente HTTP y un usuario de prueba."""
        self.client = Client()
        self.usuario = Usuario.objects.create_user(
            username='pedro_prueba',
            email='pedro@inacap.cl',
            password='Password123'
        )

    def test_modelo_usuario_campos_por_defecto(self):
        """Verifica que el modelo cree los campos con sus valores por defecto (EVA 1)."""
        self.assertEqual(self.usuario.intentos_fallidos, 0)
        self.assertFalse(self.usuario.bloqueado)
        self.assertEqual(self.usuario.email, 'pedro@inacap.cl')

    def test_validacion_contrasena_invalida(self):
        """Prueba que el formulario rechace contraseñas que no cumplen los requisitos de EVA 1."""
        # Caso 1: Menos de 8 caracteres
        f1 = RegistroUsuarioForm(data={
            'username': 'nuevo1',
            'email': 'nuevo1@correo.com',
            'contrasena': 'Abc1',
            'confirmacion_contrasena': 'Abc1'
        })
        self.assertFalse(f1.is_valid())
        self.assertIn('La contraseña debe tener mínimo 8 caracteres.', str(f1.errors))

        # Caso 2: Sin mayúscula
        f2 = RegistroUsuarioForm(data={
            'username': 'nuevo2',
            'email': 'nuevo2@correo.com',
            'contrasena': 'password123',
            'confirmacion_contrasena': 'password123'
        })
        self.assertFalse(f2.is_valid())
        self.assertIn('al menos una letra mayúscula', str(f2.errors))

        # Caso 3: Sin números
        f3 = RegistroUsuarioForm(data={
            'username': 'nuevo3',
            'email': 'nuevo3@correo.com',
            'contrasena': 'PasswordSinNumero',
            'confirmacion_contrasena': 'PasswordSinNumero'
        })
        self.assertFalse(f3.is_valid())
        self.assertIn('al menos un número', str(f3.errors))

        # Caso 4: Contraseñas no coinciden
        f4 = RegistroUsuarioForm(data={
            'username': 'nuevo4',
            'email': 'nuevo4@correo.com',
            'contrasena': 'Password123',
            'confirmacion_contrasena': 'PasswordDistinta999'
        })
        self.assertFalse(f4.is_valid())
        self.assertIn('Las contraseñas no coinciden', str(f4.errors))

    def test_login_exitoso_y_reinicio_de_intentos(self):
        """Verifica que un login válido ingrese y reinicie los intentos fallidos a 0."""
        # Simulamos que tenía un intento fallido previo
        self.usuario.intentos_fallidos = 1
        self.usuario.save()

        respuesta = self.client.post(reverse('iniciar_sesion'), {
            'username': 'pedro_prueba',
            'password': 'Password123'
        })
        # Debe redirigir a index (302)
        self.assertEqual(respuesta.status_code, 302)

        # Recargamos el usuario desde la BD SQLite
        self.usuario.refresh_from_db()
        self.assertEqual(self.usuario.intentos_fallidos, 0)
        self.assertFalse(self.usuario.bloqueado)

    def test_bloqueo_al_tercer_intento_fallido(self):
        """
        Verifica el requisito central de EVA 1:
        Al 3er fallo consecutivo de contraseña, el campo 'bloqueado' pasa a True en la BD.
        """
        url_login = reverse('iniciar_sesion')

        # Intento fallido 1
        self.client.post(url_login, {'username': 'pedro_prueba', 'password': 'ClaveErronea1'})
        self.usuario.refresh_from_db()
        self.assertEqual(self.usuario.intentos_fallidos, 1)
        self.assertFalse(self.usuario.bloqueado)

        # Intento fallido 2
        self.client.post(url_login, {'username': 'pedro_prueba', 'password': 'ClaveErronea2'})
        self.usuario.refresh_from_db()
        self.assertEqual(self.usuario.intentos_fallidos, 2)
        self.assertFalse(self.usuario.bloqueado)

        # Intento fallido 3 -> DEBE BLOQUEARSE
        self.client.post(url_login, {'username': 'pedro_prueba', 'password': 'ClaveErronea3'})
        self.usuario.refresh_from_db()
        self.assertEqual(self.usuario.intentos_fallidos, 3)
        self.assertTrue(self.usuario.bloqueado)

        # Intento con contraseña correcta mientras está bloqueado -> DEBE SER RECHAZADO
        resp_bloqueado = self.client.post(url_login, {'username': 'pedro_prueba', 'password': 'Password123'})
        self.assertContains(resp_bloqueado, 'Clave bloqueada. Ha superado el máximo de intentos permitidos.')

    def test_desbloqueo_de_cuenta(self):
        """Verifica que la vista de desbloqueo reactive la cuenta y reinicie intentos."""
        # Bloqueamos intencionalmente la cuenta
        self.usuario.bloqueado = True
        self.usuario.intentos_fallidos = 3
        self.usuario.save()

        # Enviamos solicitud POST de desbloqueo
        resp = self.client.post(reverse('desbloquear_usuario'), {
            'username': 'pedro_prueba'
        })
        self.assertEqual(resp.status_code, 302)

        # Verificamos que en la BD el estado sea activo
        self.usuario.refresh_from_db()
        self.assertFalse(self.usuario.bloqueado)
        self.assertEqual(self.usuario.intentos_fallidos, 0)
