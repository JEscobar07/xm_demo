
Este proyecto automatiza la recolección de empleados desde Odoo CRM y los registra en un sistema local desarrollado con Django, utilizando Playwright.

---

## 🧰 Requisitos

- Tener **Docker** instalado → [Descargar Docker](https://www.docker.com/)
- Tener **Python 3.11 o superior** instalado
- Tener **pip** y **virtualenv** disponibles en tu sistema

---

## 🧪 1. Levantar el backend de Django localmente

### 1.1 Clona este repositorio:

git clone https://github.com/JEscobar07/xm_demo.git
cd xm_demo

### 1.2 Crear y activar un entorno virtual de Python
En Windows:

python -m venv .venv
.venv\Scripts\activate

En Linux / macOS:

python3 -m venv .venv
source .venv/bin/activate

### 1.3 Instala las dependencias:

pip install -r requirements.txt

### 1.4 Corre las migraciones y el servidor:

python manage.py migrate
python manage.py runserver

    Asegúrate de que el backend esté corriendo en http://127.0.0.1:8000/ (o  en la ip correspondiente)
    
### 🐳 2. Ejecutar el script de automatización con Docker

Este proyecto incluye un Dockerfile para encapsular únicamente el script de automatización (./automation/script.py).

### 2.1 Construir la imagen Docker:

docker build -t odoo-playwright-bot .

### 2.2 Ejecutar el script:

docker run --rm odoo-playwright-bot

     Este comando ejecuta el script dentro de un contenedor Docker que usa Playwright para automatizar tareas. El script se conecta al backend Django local, por lo tanto, asegúrate de que esté activo antes de correrlo.

⚙️ Variables de entorno

Este proyecto utiliza un archivo .env para las credenciales del login y de Odoo. Asegúrate de tener un archivo .env en la raíz con el siguiente contenido:

📁 Estructura del proyecto

xm_demo/
│
├── automation/
│   └── script.py         ← Script que se ejecuta con Docker
│
├── core/
│   └── manage.py         ← Proyecto Django (correr localmente)
│
├── requirements.txt      ← Dependencias del proyecto
├── Dockerfile            ← Dockeriza solo el script
├── .env                  ← Credenciales 
 ── README.md             ← Guía completa
