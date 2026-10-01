# ==============================================================================
# EVA 1: FORMULARIOS Y VALIDACIONES DE SEGURIDAD (forms.py)
# ==============================================================================
# ENUNCIADO EVA 1:
# "Registro de usuarios:
#  - Nombre de usuario.
#  - Correo electrónico.
#  - Contraseña.
#  - Confirmación de contraseña.
#  - Validación de usuario único.
#  - Validación de correo único.
#  - Contraseña de mínimo 8 caracteres.
#  - Al menos una letra mayúscula.
#  - Al menos un número."
#
# En Django, los formularios (forms.ModelForm) centralizan la recepción de datos,
# la sanitización de entradas, las validaciones de negocio y la conversión hacia
# objetos del modelo de base de datos.
# ==============================================================================

import re
from django import forms
from django.contrib.auth.validators import UnicodeUsernameValidator
from .models import Usuario


class RegistroUsuarioForm(forms.ModelForm):
    """
    Formulario basado en modelo (ModelForm) para crear nuevos usuarios.
    Combina los campos nativos del modelo Usuario con campos virtuales de contraseña
    y métodos de validación estricta (clean_<campo> y clean general).
    """

    # Campo de nombre de usuario con validador de caracteres permitidos
    username = forms.CharField(
        label='Nombre de usuario',
        max_length=150,
        validators=[UnicodeUsernameValidator()],
        help_text='Máximo 150 caracteres. Solo letras, números y @/./+/-/_ (sin espacios).',
        widget=forms.TextInput(attrs={
            'placeholder': 'Ej: juan_perez',
            'class': 'form-control',
            'autocomplete': 'username'
        }),
        error_messages={
            'invalid': 'Nombre de usuario inválido. No uses espacios ni símbolos no permitidos.'
        }
    )

    # Campo de correo electrónico con validación automática de formato RFC
    email = forms.EmailField(
        label='Correo electrónico',
        help_text='Ingresa un correo válido (ej: usuario@inacap.cl).',
        widget=forms.EmailInput(attrs={
            'placeholder': 'ejemplo@correo.com',
            'class': 'form-control',
            'autocomplete': 'email'
        })
    )

    # Widgets PasswordInput ocultan los caracteres tipeados en pantalla (••••••••)
    contrasena = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Mínimo 8 caracteres, 1 mayúscula, 1 número',
            'class': 'form-control',
            'autocomplete': 'new-password'
        }),
        help_text='Mínimo 8 caracteres, al menos 1 letra mayúscula y 1 número.'
    )

    confirmacion_contrasena = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repite exactamente tu contraseña',
            'class': 'form-control',
            'autocomplete': 'new-password'
        }),
        help_text='Ambas contraseñas deben ser idénticas.'
    )

    class Meta:
        """Metadatos del formulario que lo vinculan con el modelo Usuario."""
        model = Usuario
        fields = ['username', 'email']

    # --------------------------------------------------------------------------
    # 1. VALIDACIÓN INDIVIDUAL DE CONTRASEÑA (clean_contrasena)
    # --------------------------------------------------------------------------
    def clean_contrasena(self):
        r"""
        Aplica las 3 reglas de complejidad exigidas en la pauta de EVA 1:
        1. Mínimo 8 caracteres de longitud.
        2. Al menos una letra mayúscula (Expresión Regular r'[A-Z]').
        3. Al menos un dígito numérico (Expresión Regular r'\d').
        
        Si alguna falla, levanta un ValidationError que Django asocia al campo.
        """
        contrasena = self.cleaned_data.get('contrasena')

        # Regla 1: Longitud mínima
        if len(contrasena) < 8:
            raise forms.ValidationError(
                'La contraseña debe tener mínimo 8 caracteres.'
            )

        # Regla 2: Presencia de al menos una letra mayúscula
        if not re.search(r'[A-Z]', contrasena):
            raise forms.ValidationError(
                'La contraseña debe tener al menos una letra mayúscula (A-Z).'
            )

        # Regla 3: Presencia de al menos un número
        if not re.search(r'\d', contrasena):
            raise forms.ValidationError(
                'La contraseña debe tener al menos un número (0-9).'
            )

        return contrasena

    # --------------------------------------------------------------------------
    # 2. VALIDACIÓN GENERAL CRUZADA (clean)
    # --------------------------------------------------------------------------
    def clean(self):
        """
        Validación cruzada entre múltiples campos.
        Compara que 'contrasena' y 'confirmacion_contrasena' coincidan exactamente.
        """
        datos_limpios = super().clean()
        contrasena = datos_limpios.get('contrasena')
        confirmacion = datos_limpios.get('confirmacion_contrasena')

        if contrasena and confirmacion:
            if contrasena != confirmacion:
                raise forms.ValidationError(
                    'Las contraseñas no coinciden. Por favor verifícalas antes de continuar.'
                )

        return datos_limpios

    # --------------------------------------------------------------------------
    # 3. GUARDADO SEGURO CON HASHING (save)
    # --------------------------------------------------------------------------
    def save(self, commit=True):
        """
        Sobrescribe el método save() para HASHEAR (encriptar unidireccionalmente)
        la contraseña antes de persistir el registro en la base de datos.
        
        ¿POR QUÉ commit=False?
        commit=False crea el objeto en memoria RAM sin disparar aún el INSERT en SQL.
        Esto nos permite usar set_password(), que toma la contraseña en texto plano,
        aplica el algoritmo criptográfico PBKDF2 con SHA-256 y un salt aleatorio,
        y almacena únicamente el hash resultante (ej: 'pbkdf2_sha256$720000$...').
        NUNCA se debe almacenar una contraseña en texto plano.
        """
        usuario = super().save(commit=False)
        usuario.set_password(self.cleaned_data['contrasena'])

        if commit:
            usuario.save()

        return usuario