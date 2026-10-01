# Eva 2 - Programación Back End (eva2Backend)

Proyecto completo para la Evaluación Sumativa N° 2 de Programación Back End (INACAP).
Integra el sistema de autenticación de la **Eva 1** con el CRUD de productos de la **Eva 2**.

---

## 🚀 Características Principales

1. **Módulo de Autenticación (Eva 1):**
   - Modelo de usuario personalizado (`Usuario`) heredado de `AbstractUser`.
   - Control de seguridad: suspensión/bloqueo de cuenta tras 3 intentos fallidos consecutivos.
   - Vistas de Registro, Inicio de Sesión, Desbloqueo y Cierre de Sesión.

2. **Módulo CRUD de Productos (Eva 2):**
   - Modelo `Producto` con atributos: ID, Nombre, Marca, Precio.
   - Operaciones CRUD completas:
     - **Crear:** Formulario de registro con validaciones y alertas de Bootstrap.
     - **Leer:** Listado de productos dinámico en tabla responsiva.
     - **Actualizar:** Edición de productos existentes.
     - **Eliminar:** Borrado individual con confirmación en JavaScript.

3. **Seguridad y Enlace (Etapa 3):**
   - Vistas del CRUD protegidas con el decorador `@login_required`.
   - Acceso restringido: requiere iniciar sesión antes de acceder a la gestión de productos.

---

## ⚙️ Instalación y Ejecución

1. **Crear y activar entorno virtual (opcional pero recomendado):**
   ```bash
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

2. **Instalar dependencias:**
   ```bash
   pip install django
   ```

3. **Aplicar migraciones:**
   ```bash
   cd Proyecto_BD
   python manage.py migrate
   ```

4. **Ejecutar el servidor:**
   ```bash
   python manage.py runserver
   ```

5. **Abrir en el navegador:**
   - [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 👤 Credenciales de Prueba

- **Superusuario:** `admin`
- **Contraseña:** `admin123`
