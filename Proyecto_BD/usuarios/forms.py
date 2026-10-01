# ==============================================================================
# CÓDIGO EXTRAÍDO E INTEGRADO DESDE EVA 1 (MÓDULO DE AUTENTICACIÓN)
# Formularios y validaciones de contraseña para registro de usuarios.
# ==============================================================================

import re
from django import forms
from django.contrib.auth.validators import UnicodeUsernameValidator
from .models import Usuario



class RegistroUsuarioForm(forms.ModelForm):
    """
    Formulario basado en modelo (ModelForm) para registrar nuevos usuarios.
    Define campos personalizados para las contraseñas y validaciones estrictas.
    """

    # Campo de nombre de usuario con validador de caracteres permitidos (sin espacios)
    username = forms.CharField(
        label='Nombre de usuario',
        max_length=150,
        validators=[UnicodeUsernameValidator()],
        help_text=(
            'Usa hasta 150 caracteres: letras, números y @, ., +, -, _.'
        ),
        error_messages={
            'invalid': (
                'Ingresa un nombre de usuario válido. No uses espacios; '
                'solo se permiten letras, números y @, ., +, -, _.'
            ),
        },
    )

    # Widget PasswordInput oculta el texto en el navegador (••••••••)
    contrasena = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput
    )

    confirmacion_contrasena = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput
    )

    class Meta:
        # Vincula este formulario directamente con nuestro modelo Usuario
        model = Usuario
        fields = ['username', 'email']
        labels = {
            'username': 'Nombre de usuario',
            'email': 'Correo electrónico',
        }

    def clean_contrasena(self):
        """
        Validación individual del campo 'contrasena'.
        Django llama automáticamente a los métodos clean_<nombre_campo>().
        """
        contrasena = self.cleaned_data.get('contrasena')

        # Regla 1: Longitud mínima de 8 caracteres
        if len(contrasena) < 8:
            raise forms.ValidationError(
                'La contraseña debe tener mínimo 8 caracteres.'
            )

        # Regla 2: Al menos 1 letra mayúscula usando Expresión Regular (Regex)
        if not re.search(r'[A-Z]', contrasena):
            raise forms.ValidationError(
                'La contraseña debe tener al menos una letra mayúscula.'
            )

        # Regla 3: Al menos 1 dígito numérico
        if not re.search(r'\d', contrasena):
            raise forms.ValidationError(
                'La contraseña debe tener al menos un número.'
            )

        # Siempre debemos retornar el dato limpio
        return contrasena

    def clean(self):
        """
        Validación general/cruzada del formulario.
        Se usa para comparar dos o más campos entre sí (contrasena vs confirmacion).
        """
        datos_limpios = super().clean()
        contrasena = datos_limpios.get('contrasena')
        confirmacion_contrasena = datos_limpios.get('confirmacion_contrasena')

        # Si ambos campos existen y son válidos individualmente, comprobamos si coinciden
        if contrasena and confirmacion_contrasena:
            if contrasena != confirmacion_contrasena:
                raise forms.ValidationError(
                    'Las contraseñas no coinciden.'
                )

        return datos_limpios

    def save(self, commit=True):
        """
        Sobrescribimos el método save() para encriptar la contraseña antes de guardar en la BD.
        """
        # commit=False crea la instancia en memoria sin guardarla aún en SQLite
        usuario = super().save(commit=False)

        # set_password() aplica el algoritmo de hashing (PBKDF2 por defecto en Django)
        # NUNCA se debe guardar la contraseña en texto plano por seguridad
        usuario.set_password(self.cleaned_data['contrasena'])

        # Si commit es True, persistimos la instancia en la Base de Datos
        if commit:
            usuario.save()

        return usuario