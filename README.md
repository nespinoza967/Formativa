# Herramientas en Común

Aplicación web en Django para que la **Junta de Vecinos Villa Los Aromos** administre el inventario de herramientas y los préstamos a sus socios.

## Requisitos

- Python 3.12 o superior
- MySQL o MariaDB
- Git

## Cómo ejecutar el proyecto

1. **Clonar el repositorio**
   ```bash
   git clone <url-del-repositorio>
   cd Formativa
   ```

2. **Crear y activar el entorno virtual**
   ```bash
   python3 -m venv venv
   source venv/bin/activate        # Linux / macOS
   # venv\Scripts\activate         # Windows
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Crear la base de datos** (en la consola de MySQL/MariaDB)
   ```sql
   CREATE DATABASE herramientas_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

5. **Configurar las variables de entorno**: copiar `.env.example` a `.env` y completar los datos.
   ```bash
   cp .env.example .env
   ```
   | Variable | Descripción |
   |---|---|
   | `SECRET_KEY` | Clave secreta de Django |
   | `DEBUG` | `True` en desarrollo |
   | `DB_NAME` | `herramientas_db` |
   | `DB_USER` / `DB_PASSWORD` | Usuario y contraseña de MySQL |
   | `DB_HOST` / `DB_PORT` | Normalmente `localhost` y `3306` |

6. **Crear las tablas y cargar los datos de prueba** (3 categorías y 15 herramientas)
   ```bash
   python manage.py migrate
   python manage.py loaddata datos_iniciales
   ```

7. **Crear los usuarios de prueba**
   ```bash
   python manage.py shell -c "
   from django.contrib.auth.models import User
   User.objects.create_superuser('admin', '', 'admin1234')
   User.objects.create_user('encargado', '', 'encargado1234', is_staff=True)
   User.objects.create_user('socio', '', 'socio1234')
   "
   ```

8. **Levantar el servidor**
   ```bash
   python manage.py runserver
   ```
   Abrir http://127.0.0.1:8000/

## Usuarios de prueba

| Usuario | Contraseña | Rol | Qué puede hacer |
|---|---|---|---|
| `admin` | `admin1234` | Superusuario | Todo, incluido el Django Admin (`/admin/`) |
| `encargado` | `encargado1234` | Encargado (`is_staff`) | CRUD de herramientas y categorías, ver todos los préstamos, activarlos y registrar devoluciones |
| `socio` | `socio1234` | Socio | Ver el catálogo, armar una solicitud (máx. 3 herramientas), confirmarla y cancelar sus préstamos pendientes |

## Funcionalidades

- **Autenticación**: login/logout con `django.contrib.auth`; la sesión expira a los 30 minutos.
- **Control de acceso**: todas las vistas requieren sesión; las de gestión son solo para el encargado (`prestamos/permisos.py`).
- **CRUD** de herramientas (con buscador y filtro por categoría) y de categorías, con validación del código `HER-000`.
- **Solicitud de préstamo** guardada en `request.session` como un carrito, con contador en el menú.
- **Préstamos**: ciclo Pendiente → Activo → Devuelto, o Pendiente → Cancelado. La herramienta se libera al cancelar o devolver.

## Estructura

```
herramientas_comun/   configuración del proyecto (settings, urls)
prestamos/
├── models.py         Categoria, Herramienta, Prestamo
├── forms.py          CategoriaForm, HerramientaForm
├── views.py          vistas de CRUD, solicitud y préstamos
├── permisos.py       decorador y mixin para el encargado
├── context_processors.py  contador de la solicitud
├── fixtures/         datos de prueba
└── templates/prestamos/
```
