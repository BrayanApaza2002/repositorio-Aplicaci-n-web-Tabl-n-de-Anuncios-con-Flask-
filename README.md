# 📋 Tablón de Anuncios — Tecnologías Emergentes II

Aplicación web desarrollada con **Python / Flask** y **SQLite** que permite gestionar un tablón de anuncios con sistema de usuarios, categorías y publicaciones.

---

##  Características
-  Registro e inicio de sesión de usuarios
-  Gestión de roles: **Administrador** y Usuario normal
-  Gestión completa de categorías (crear, listar, editar, eliminar)
-  Publicación de anuncios con título, contenido y categoría
-  Edición y eliminación de anuncios
-  Panel de administración de usuarios (solo para administradores)
-  Arquitectura con **Application Factory** y **Blueprints**

---

##  Estructura de la Base de Datos

| Tabla | Campos |
|---|---|
| **usuarios** | id, nombre, correo, contrasena_hash, es_admin |
| **categorias** | id, nombre, descripcion |
| **anuncios** | id, titulo, contenido, fecha_creacion, usuario_id, categoria_id |

**Relaciones:**
- Un usuario puede tener muchos anuncios (1 → N)
- Una categoría puede tener muchos anuncios (1 → N)

---

##  Estructura del Proyecto
tablon_anuncios/
├── app/
│ ├── init.py # Application Factory
│ ├── models.py # Modelos y conexión a la BD
│ ├── auth/ # Autenticación
│ │ ├── init.py
│ │ └── routes.py
│ ├── anuncios/ # Gestión de anuncios
│ │ ├── init.py
│ │ └── routes.py
│ ├── categorias/ # Gestión de categorías
│ │ ├── init.py
│ │ └── routes.py
│ ├── usuarios/ # Gestión de usuarios
│ │ ├── init.py
│ │ └── routes.py
│ └── templates/ # Vistas HTML
│ ├── base.html
│ ├── auth/
│ ├── anuncios/
│ ├── categorias/
│ └── usuarios/
├── run.py # Archivo para ejecutar la app
├── requirements.txt # Dependencias
├── bd_anuncios.db # Base de datos SQLite
└── README.md # Este archivo

---

## ⚙️ Instalación y Ejecución

### 1. Requisitos previos
- Python 3.10 o superior instalado

### 2. Instalar dependencias
```bash
pip install flask flask-sqlalchemy
python run.py
http://127.0.0.1:5000
