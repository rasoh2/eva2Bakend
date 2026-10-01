# 📘 Sistema Integrado Back End (EVA 1 + EVA 2) - INACAP
### Asignatura: Programación Back End | Docente: Javier Eduardo Gutiérrez Osorio

Bienvenido a la documentación técnica oficial del proyecto. Esta guía fue diseñada específicamente para que cualquier **desarrollador Junior**, estudiante o evaluador técnico comprenda a fondo:
1. Cómo está construida la arquitectura del sistema.
2. Qué partes vienen por defecto dentro del Framework Django vs. qué partes fueron desarrolladas a medida.
3. El paso a paso de lo construido en las **Guías 1, 2 y 3 de la Unidad 2**.
4. Cómo se resolvió la **Evaluación Sumativa N° 1 (EVA 1)** y su posterior integración en la **Evaluación Sumativa N° 2 (EVA 2)** mediante el enlace de seguridad de la **Etapa 3**.
5. Un **Banco de Preguntas y Respuestas Técnicas** listo para defender con éxito la interrogación oral de código (30 puntos de la pauta).

---

## 📑 Tabla de Contenidos
1. [Visión General del Proyecto](#-visión-general-del-proyecto)
2. [Arquitectura del Sistema (MVT de Django)](#-arquitectura-del-sistema-mvt-de-django)
3. [¿Qué viene por defecto en Django vs. Qué desarrollamos nosotros?](#-qué-viene-por-defecto-en-django-vs-qué-desarrollamos-nosotros)
4. [Desarrollo Paso a Paso de las Guías de Clase (Unidad 2)](#-desarrollo-paso-a-paso-de-las-guías-de-clase-unidad-2)
   - [Guía 01: Proyecto, Base de Datos, Modelo y Migraciones](#guía-01-proyecto-base-de-datos-modelo-y-migraciones)
   - [Guía 02: Creación de Templates y Enrutamiento](#guía-02-creación-de-templates-y-enrutamiento)
   - [Guía 03: CRUD Completo con Base de Datos y Bootstrap](#guía-03-crud-completo-con-base-de-datos-y-bootstrap)
5. [Módulo de Seguridad y Autenticación (EVA 1)](#-módulo-de-seguridad-y-autenticación-eva-1)
   - [Modelo de Usuario y Bloqueo en Base de Datos](#modelo-de-usuario-y-bloqueo-en-base-de-datos)
   - [Validaciones de Contraseña y Seguridad](#validaciones-de-contraseña-y-seguridad)
   - [Front End y Controles de Interfaz en JavaScript](#front-end-y-controles-de-interfaz-en-javascript)
6. [Enlace de Sistemas (EVA 2 - Etapa 3)](#-enlace-de-sistemas-eva-2---etapa-3)
7. [Mapa de Rutas y Endpoints](#-mapa-de-rutas-y-endpoints)
8. [Instalación, Ejecución y Batería de Pruebas](#-instalación-ejecución-y-batería-de-pruebas)
9. [Banco de Preguntas para la Interrogación Oral (Defensa del Código)](#-banco-de-preguntas-para-la-interrogación-oral-defensa-del-código)

---

## 🎯 Visión General del Proyecto

El proyecto está compuesto por dos grandes aplicaciones integradas bajo un mismo núcleo:

```
                                PROYECTO DJANGO (Proyecto_BD)
                                              │
                     ┌────────────────────────┴────────────────────────┐
                     ▼                                                 ▼
             APP 'usuarios' (EVA 1)                           APP 'productos' (EVA 2)
  - Modelo de Usuario Personalizado                - Modelo de Producto (ID, Nombre, Marca, Precio)
  - Control de 3 intentos fallidos                 - Operaciones CRUD (Create, Read, Update, Delete)
  - Bloqueo y persistencia en SQLite               - Formularios y Alertas Bootstrap 5
  - Validaciones de Contraseña (Regex)             - Confirmación en JavaScript
  - Front End propio con Controles JS              - Vistas protegidas por @login_required (Etapa 3)
```

---

## 🏗 Arquitectura del Sistema (MVT de Django)

Django no utiliza la arquitectura MVC (Model-View-Controller) clásica, sino una variante especializada llamada **MVT (Model - View - Template)**:

```
[ Petición HTTP del Navegador ]
             │
             ▼
     1. config/urls.py  ────────► Analiza la URL solicitada y la despacha
             │
             ▼
     2. views.py (Vista) ◄──────► Ejecuta la lógica de negocio y controla permisos (@login_required)
          │          ▲
          ▼          │
     3. models.py (Modelo) ─────► Consulta / Modifica la Base de Datos SQLite mediante el ORM
          │
          ▼
     4. Template (HTML) ────────► Inyecta variables dinámicas ({% tag %}, {{ var }}) y genera HTML
             │
             ▼
[ Respuesta HTTP al Navegador ]
```

- **M (Modelo - `models.py`):** Define la estructura de las tablas de datos usando clases de Python. El ORM de Django traduce estas clases a sentencias SQL relacionales.
- **V (Vista - `views.py`):** Es la función o controlador lógico que recibe la petición HTTP (`request`), interactúa con los modelos y retorna una respuesta (renderiza un template o redirige con un `redirect`).
- **T (Template - `.html`):** Es la capa de presentación. Utiliza el motor de plantillas de Django (DTL) para mezclar código HTML estándar con variables dinámicas enviadas desde la vista.

---

## ⚖️ ¿Qué viene por defecto en Django vs. Qué desarrollamos nosotros?

Para un programador Junior es vital saber distinguir qué entrega el framework y qué código fue escrito por nosotros:

| Componente | ¿Viene por defecto en Django? | ¿Desarrollado por nosotros? | Detalle / Explicación |
| :--- | :---: | :---: | :--- |
| **`manage.py`** | ✅ Sí | ❌ No | Script utilitario generado por `django-admin startproject` para ejecutar comandos (`runserver`, `migrate`, etc.). |
| **`config/settings.py`** | ✅ Base provista | ✏️ Modificado | Django provee middlewares, secret key y base. **Nosotros agregamos**: registro de apps (`usuarios`, `productos`), `AUTH_USER_MODEL`, `LOGIN_URL`, `LOGIN_REDIRECT_URL` e internacionalización. |
| **`config/urls.py`** | ✅ Base provista | ✏️ Modificado | Django solo trae la ruta `/admin/`. **Nosotros añadimos**: `include('usuarios.urls')` y las 7 rutas CRUD del módulo productos. |
| **App `productos`** | ❌ No | 🔨 Desarrollado | Creada desde cero mediante `python manage.py startapp productos` (Guía 1). |
| **Modelo `Producto`** | ❌ No | 🔨 Desarrollado | Clase en `productos/models.py` con campos `nombre`, `marca` y `precio` (Guía 1). |
| **Vistas CRUD Productos** | ❌ No | 🔨 Desarrollado | Funciones en `productos/views.py`: `mostrarIndex`, `mostrarListado`, `mostrarFormRegistrar`, `insertarProducto`, etc. (Guías 2 y 3). |
| **Templates Productos** | ❌ No | 🔨 Desarrollado | `index.html`, `form_registrar.html`, `listado.html`, `form_actualizar.html` con Bootstrap 5 y JavaScript. |
| **App `usuarios`** | ❌ No | 🔨 Desarrollado | Módulo de autenticación personalizada creado para cumplir con la pauta de EVA 1. |
| **Modelo `Usuario`** | ❌ No | 🔨 Desarrollado | Hereda de `AbstractUser` e incorpora los campos en BD: `intentos_fallidos` y `bloqueado`. |
| **Formulario `RegistroUsuarioForm`** | ❌ No | 🔨 Desarrollado | `forms.ModelForm` con validación Regex de mayúsculas, números, longitud de 8 caracteres y confirmación cruzada. |
| **Lógica de 3 Intentos Fallidos** | ❌ No | 🔨 Desarrollado | Algoritmo en `usuarios/views.py` que bloquea la cuenta en base de datos al tercer error consecutivo. |
| **Mecanismo de Desbloqueo** | ❌ No | 🔨 Desarrollado | Vista `desbloquear_usuario()` y template `desbloquear.html` para rehabilitar accesos suspendidos. |
| **Front End y JavaScript de Seguridad** | ❌ No | 🔨 Desarrollado | Funciones JS para mostrar/ocultar contraseñas, validación en tiempo real de requisitos y advertencia antes del envío. |
| **Panel de Administración (`/admin/`)** | ✅ Sí | ✏️ Personalizado | Django entrega el panel; **nosotros registramos** `ProductoAdmin` y `UsuarioAdmin` mostrando las columnas personalizadas. |
| **Motor de Base de Datos SQLite** | ✅ Sí | ❌ No | Viene integrado en Python y Django (`db.sqlite3`). No requiere servidores externos como MySQL o PostgreSQL. |

---

## 📚 Desarrollo Paso a Paso de las Guías de Clase (Unidad 2)

### Guía 01: Proyecto, Base de Datos, Modelo y Migraciones
1. **Creación del Proyecto:**
   ```bash
   django-admin startproject Proyecto_BD
   cd Proyecto_BD
   ```
2. **Creación de la App de Productos:**
   ```bash
   python manage.py startapp productos
   ```
3. **Registro de la App en `settings.py`:**
   En `INSTALLED_APPS` agregamos `'productos'`.
4. **Construcción del Modelo (`productos/models.py`):**
   ```python
   class Producto(models.Model):
       nombre = models.CharField(max_length=100)
       marca = models.CharField(max_length=100)
       precio = models.IntegerField(null=False)
   ```
5. **Generación y Aplicación de Migraciones:**
   - `python manage.py makemigrations`: Genera el archivo `productos/migrations/0001_initial.py`, traduciendo la clase de Python a un plano de migración.
   - `python manage.py migrate`: Ejecuta la migración en `db.sqlite3`. Crea la tabla `productos_producto` con su campo `id` autoincremental como Primary Key.

### Guía 02: Creación de Templates y Enrutamiento
1. **Estructura de Plantillas:**
   Creamos la carpeta `productos/templates/` conteniendo:
   - `index.html`: Menú inicial de navegación.
   - `form_registrar.html`: Formulario para captura de datos.
   - `listado.html`: Tabla para despliegue de inventario.
   - `form_actualizar.html`: Formulario para edición de registros.
2. **Enrutamiento Inicial:**
   En `config/urls.py` mapeamos las rutas hacia las funciones de `productos/views.py`.

### Guía 03: CRUD Completo con Base de Datos y Bootstrap
1. **Paso de Volver al Index:** Se configuraron enlaces `<a href="/">Volver al Index</a>` en todas las pantallas.
2. **Variables del Formulario (`form_registrar.html`):**
   - `txtnom` -> Nombre del producto.
   - `cbomar` -> Marca elegida en un `<select>` ("A cuenta", "Jumbo", "Lider").
   - `txtpre` -> Precio entero.
3. **Persistencia por POST (`/insertar`):**
   La vista `insertarProducto` captura los datos mediante `request.POST.get(...)`, crea el objeto `Producto` y lo guarda con `pro.save()`.
4. **Alertas de Bootstrap 5:**
   Se incorporaron componentes `alert alert-success` y `alert alert-danger` condicionales para desplegar `msjOk` o `msjErr`.
5. **Confirmación de Eliminación con JavaScript:**
   En `listado.html`:
   ```javascript
   const botonEliminar = (id) => {
       if (window.confirm("¿Está Seguro De Querer Eliminar El Registro?")) {
           window.location.href = "/eliminar/" + id;
       }
   };
   ```

---

## 🛡 Módulo de Seguridad y Autenticación (EVA 1)

### Modelo de Usuario y Bloqueo en Base de Datos
Para responder al enunciado de EVA 1:
> *"Idealmente, el bloqueo debería quedar almacenado en la base de datos y no solamente en JavaScript, porque es una regla de seguridad del backend."*

Heredamos de `AbstractUser` en `usuarios/models.py`:
```python
class Usuario(AbstractUser):
    email = models.EmailField(unique=True)
    intentos_fallidos = models.PositiveSmallIntegerField(default=0)
    bloqueado = models.BooleanField(default=False)
```

**Algoritmo de Bloqueo al 3er Intento (`usuarios/views.py`):**
1. **Comprobación Previa:** Al recibir el formulario de login, verifica si `usuario.bloqueado == True`. Si está bloqueado, rechaza el acceso sin verificar contraseña y muestra: *"Clave bloqueada. Ha superado el máximo de intentos permitidos."*
2. **Intento de Autenticación:** Llama a `authenticate(request, username, password)`.
3. **Si es Exitoso:** Reinicia `intentos_fallidos = 0`, guarda en BD y llama a `login(request, usuario)`.
4. **Si es Erróneo:** Incrementa `intentos_fallidos += 1`.
   - Si llega a 3 fallos consecutivos: cambia `bloqueado = True` y persiste en la base de datos SQLite.
   - Si lleva 1 o 2 fallos: le advierte cuántos intentos le quedan.

### Validaciones de Contraseña y Seguridad
En `usuarios/forms.py` (`RegistroUsuarioForm`):
- **Longitud mínima:** `len(contrasena) >= 8`.
- **Mayúscula obligatoria:** Expresión Regular `re.search(r'[A-Z]', contrasena)`.
- **Número obligatorio:** Expresión Regular `re.search(r'\d', contrasena)`.
- **Contraseñas idénticas:** Validación en el método `clean()` comparando `contrasena == confirmacion_contrasena`.
- **Hashing con PBKDF2:** En el método `save()`, se ejecuta `usuario.set_password(...)` con `commit=False` para encriptar unidireccionalmente la contraseña antes de guardar en SQLite.

### Front End y Controles de Interfaz en JavaScript
En `usuarios/templates/usuarios/registro.html` y `login.html`:
- **Mostrar / Ocultar Contraseña:** Botón interactivo con icono (👁️ / 🙈) que conmuta dinámicamente el atributo `type="password"` a `type="text"`.
- **Requisitos en Tiempo Real:** Caja de advertencia que actualiza en vivo tres indicadores (largo, mayúscula, número) a medida que el usuario escribe.
- **Validación Cruzada en Tiempo Real:** Indica si las contraseñas coinciden (verde) o no (rojo).
- **Validación previa al Submit:** El evento `submit` detiene el envío (`event.preventDefault()`) si no se cumplen los requisitos, mostrando una alerta en pantalla antes de enviar datos al servidor.

---

## 🔗 Enlace de Sistemas (EVA 2 - Etapa 3)

La **Etapa 3** de la Evaluación Sumativa 2 exige:
> *"Enlazar las APP creadas en las etapas 1 y 2, es decir, antes de ingresar al CRUD, la persona debe logearse (se debe registrar si corresponde)"*

Esto se resolvió mediante:
1. **Decorador `@login_required`:**
   Aplicado sobre todas las vistas del CRUD en `productos/views.py`:
   ```python
   @login_required
   def mostrarIndex(request): ...
   
   @login_required
   def mostrarListado(request): ...
   
   @login_required
   def mostrarFormRegistrar(request): ...
   ```
2. **Configuración en `settings.py`:**
   ```python
   AUTH_USER_MODEL = 'usuarios.Usuario'
   LOGIN_URL = '/login/'
   LOGIN_REDIRECT_URL = '/'
   LOGOUT_REDIRECT_URL = '/login/'
   ```
   Si un usuario anónimo intenta ingresar a `/listado`, Django intercepta la petición y lo redirige automáticamente a `/login/?next=/listado`. Una vez que se autentica correctamente, es redirigido directo a la página que deseaba ver.

---

## 🗺 Mapa de Rutas y Endpoints

| URL | Nombre de Ruta | Método | Vista Asociada | ¿Requiere Login? | Descripción |
| :--- | :--- | :---: | :--- | :---: | :--- |
| `/` | `index` | GET | `productos.views.mostrarIndex` | 🔒 Sí | Menú principal de productos con mensaje de bienvenida. |
| `/login/` | `iniciar_sesion` | GET / POST | `usuarios.views.iniciar_sesion` | 🌐 Público | Pantalla de acceso con control de 3 intentos fallidos. |
| `/registro/` | `registrar_usuario` | GET / POST | `usuarios.views.registrar_usuario` | 🌐 Público | Formulario de alta con validación Regex y JS. |
| `/desbloquear/` | `desbloquear_usuario` | GET / POST | `usuarios.views.desbloquear_usuario` | 🌐 Público | Restablecimiento de cuentas bloqueadas. |
| `/logout/` | `cerrar_sesion` | GET | `usuarios.views.cerrar_sesion` | 🔒 Sí | Destruye la sesión activa y redirige al login. |
| `/inicio/` | `inicio` | GET | `usuarios.views.inicio` | 🔒 Sí | Dashboard alternativo del módulo de usuarios. |
| `/form_registrar` | `form_registrar` | GET | `productos.views.mostrarFormRegistrar` | 🔒 Sí | Formulario vacío para ingresar producto. |
| `/insertar` | `insertar` | POST | `productos.views.insertarProducto` | 🔒 Sí | Procesa el guardado del producto en SQLite. |
| `/listado` | `listado` | GET | `productos.views.mostrarListado` | 🔒 Sí | Tabla con todos los productos registrados. |
| `/form_actualizar/<id>`| `form_actualizar` | GET | `productos.views.mostrarFormActualizar` | 🔒 Sí | Formulario de edición con datos precargados. |
| `/actualizar/<id>` | `actualizar` | POST | `productos.views.actualizarProducto` | 🔒 Sí | Guarda los cambios modificados del producto. |
| `/eliminar/<id>` | `eliminar` | GET | `productos.views.eliminarProducto` | 🔒 Sí | Borra el registro tras confirmación en JS. |
| `/admin/` | `admin:index` | GET / POST | Django Admin Site | 🔒 Solo Staff | Panel administrativo nativo de Django. |

---

## ⚙️ Instalación, Ejecución y Batería de Pruebas

### 1. Requisitos Previos
- Python 3.10 o superior instalado.

### 2. Crear y Activar Entorno Virtual (Recomendado)
En PowerShell (Windows):
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Instalar Dependencias
```powershell
pip install django
```

### 4. Aplicar Migraciones de Base de Datos
```powershell
cd Proyecto_BD
python manage.py makemigrations
python manage.py migrate
```

### 5. Ejecutar Batería de Pruebas Automatizadas
El proyecto incluye 10 pruebas unitarias y de integración que validan el 100% de los requerimientos de EVA 1 y EVA 2:
```powershell
python manage.py test
```
*Salida esperada:*
```text
Ran 10 tests in 21.441s
OK
```

### 6. Iniciar el Servidor de Desarrollo
```powershell
python manage.py runserver
```
Ingresa en tu navegador web a: **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

### 7. Credenciales Iniciales de Prueba
- **Superusuario:** `admin` | **Contraseña:** `admin123`
- Puedes registrar cualquier usuario nuevo desde `/registro/`.

---

## 🎓 Banco de Preguntas para la Interrogación Oral (Defensa del Código)

La pauta de evaluación de la **EVA 2** asigna **30 puntos a la Interrogación del código desarrollado**. A continuación se presentan las preguntas más comunes que realiza el docente evaluador y cómo responderlas como un desarrollador profesional:

#### 1. ¿Por qué usamos `AbstractUser` en lugar de crear un modelo de usuario desde cero o usar el que viene por defecto?
> **Respuesta:** "Al heredar de `AbstractUser`, mantenemos toda la lógica interna y segura de autenticación de Django (hashing PBKDF2, grupos, permisos y compatibilidad con el Admin), pero tenemos la libertad de añadir los campos personalizados que exigía la EVA 1: `intentos_fallidos` y `bloqueado`, persistiendo las reglas de negocio en la base de datos."

#### 2. ¿Qué hace el decorador `@login_required` y qué sucede si un usuario anónimo intenta ingresar a una ruta protegida?
> **Respuesta:** "Es un decorador de Django que verifica si `request.user.is_authenticated` es `True`. Si el usuario no ha iniciado sesión, Django detiene la ejecución de la vista y emite una redirección HTTP 302 hacia la URL definida en `LOGIN_URL` (`/login/`), adjuntando el parámetro `?next=<ruta_original>` para que tras autenticarse pueda volver a la página que solicitó."

#### 3. ¿Por qué las contraseñas nunca deben guardarse en texto plano en la base de datos y cómo lo resuelve Django?
> **Respuesta:** "Guardar contraseñas en texto plano es una vulnerabilidad crítica porque cualquier filtración de la base de datos expondría las claves de los usuarios. Django utiliza la función `set_password()`, la cual aplica una función hash criptográfica unidireccional (PBKDF2 con SHA-256 y salt aleatorio). De esta forma, en SQLite solo se almacena el hash resultante y nunca la clave original."

#### 4. ¿Para qué sirve el token `{% csrf_token %}` en los formularios POST?
> **Respuesta:** "Protege la aplicación contra ataques de tipo *Cross-Site Request Forgery* (Falsificación de Petición en Sitios Cruzados). Django genera un token criptográfico único por sesión y lo inserta como campo oculto. Al enviar el formulario, el middleware verifica que el token coincida; si un atacante intenta enviar una petición maliciosa desde otro dominio, el servidor la rechaza con un error HTTP 403 Forbidden."

#### 5. ¿Qué diferencia hay entre `python manage.py makemigrations` y `python manage.py migrate`?
> **Respuesta:** "`makemigrations` inspecciona los cambios realizados en las clases de `models.py` y genera archivos de migración en Python (planos o esquemas de cambio dentro de la carpeta `migrations/`). `migrate`, por su parte, toma esos archivos y ejecuta las sentencias SQL reales (CREATE TABLE, ALTER TABLE, etc.) sobre el motor de base de datos (`db.sqlite3`)."

#### 6. En el formulario registrar producto, ¿cómo viajan los datos desde el HTML hasta guardarse en SQLite?
> **Respuesta:** "En el HTML, cada input tiene un atributo `name` (`txtnom`, `cbomar`, `txtpre`). Al presionar 'Guardar Datos', el navegador envía una petición HTTP POST hacia `/insertar`. En `views.py`, la vista `insertarProducto` captura los valores mediante `request.POST.get('txtnom')`, etc., instancia la clase `Producto(nombre=nom, marca=mar, precio=pre)` y al invocar `pro.save()`, el ORM de Django traduce la instancia en un `INSERT INTO productos_producto (...) VALUES (...);`."

#### 7. ¿Por qué en `usuarios/forms.py` se utiliza `usuario = super().save(commit=False)`?
> **Respuesta:** "El parámetro `commit=False` le indica a Django que construya la instancia del modelo en la memoria RAM pero sin guardarla todavía en la base de datos. Esto es fundamental porque nos permite tomar la contraseña en texto plano, aplicarle `set_password()` para hashearla, y recién entonces ejecutar `usuario.save()` para persistirla de forma segura."

#### 8. ¿Dónde y cómo se controla el bloqueo de 3 intentos fallidos?
> **Respuesta:** "Se controla en el backend, en la vista `iniciar_sesion` de `usuarios/views.py`. Cuando `authenticate()` retorna `None` pero el usuario existe en la base de datos, incrementamos `usuario.intentos_fallidos += 1`. Si el contador es mayor o igual a 3, establecemos `usuario.bloqueado = True` y guardamos en SQLite con `update_fields=['intentos_fallidos', 'bloqueado']`. Si el login resulta exitoso, reiniciamos el contador a 0."

#### 9. ¿Por qué es una buena práctica de seguridad mostrar 'Usuario o contraseña incorrectos' cuando el usuario no existe?
> **Respuesta:** "Para evitar el ataque conocido como *User Enumeration* (enumeración de usuarios). Si el sistema respondiera 'El usuario no existe', un atacante sabría qué nombres de usuario son válidos en el sistema y podría concentrar ataques de fuerza bruta solo contra cuentas reales."

#### 10. ¿Por qué implementamos validaciones de contraseña tanto en JavaScript como en Python?
> **Respuesta:** "Es el principio de **Defensa en Profundidad**. La validación en JavaScript mejora la experiencia de usuario (UX) al darle feedback visual inmediato sin recargar la página. La validación en Python (`clean_contrasena` en `forms.py`) es la regla de seguridad definitiva del backend, ya que un atacante podría deshabilitar JavaScript en su navegador o enviar peticiones directas vía Postman/Curl."

---
*Proyecto desarrollado y documentado para la Evaluación Sumativa N° 2 de Programación Back End (INACAP).*
