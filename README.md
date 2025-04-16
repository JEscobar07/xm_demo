
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

cd ./core

python manage.py migrate

python manage.py runserver

    Asegúrate de que el backend esté corriendo en http://127.0.0.1:8000/ (o  en la ip correspondiente)
    
### 🐳 2. Ejecutar el script de automatización con Docker

Abrir otra terminal, dejan corriendo el servidor de django.

Este proyecto incluye un Dockerfile para encapsular únicamente el script de automatización (./automation/script.py).

### 2.1 Construir la imagen Docker:

docker build -t odoo-playwright-bot .

### 2.2 Ejecutar el script:

docker run --env-file .env odoo-playwright-bot

     Este comando ejecuta el script dentro de un contenedor Docker que usa Playwright para automatizar tareas. El script se conecta y envia las variables de entorno al backend Django local, por lo tanto, asegúrate de que esté activo antes de correrlo .

⚙️ Variables de entorno

Este proyecto utiliza un archivo .env para las credenciales del login y de Odoo. Asegúrate de tener un archivo .env en la raíz.

Nota:

Para visualizar las acciones que realiza el script seguir las siguientes instrucciones:

0) Estar ejecuntando en una terminal el servidor MVC de django previamente con el comando "python manage.py runserver" debe mantener  ejecutandose en todo momento hasta final mientras continua con el siguientes pasos.
1) Ir a la linea de codigo 119 del script que esta ubicado en la ruta: ./automation/script.py
2) Cambiar la propiedad de headless a False ->  browser = await p.chromium.launch(headless=False, slow_mo=1000)
3) Despues ingresar a la linea de codigo 4 del archivo de variables de entorno ubicada en la ruta : ./.env
4) Cambiar la url http://host.docker.internal:8000 por la url donde se haya desplegado nuestro MVC de django , ejemplo -> PLAYWRIGHT_BASE_URL=http://127.0.0.1:8000
5) Abrir una nueva terminal (sin eliminar la que se ha estado ejecutando el mvc de django)
6) Activar nuevamente un entorno virtual con el comando .venv\Scripts\activate
7) Ejecutar nuevamente el script con el siguiente comando: python ./automation/script.py

