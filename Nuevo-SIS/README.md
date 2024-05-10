# Sistema Integral de Sedes
Aplicación para la administración de algunos procesos de las Sedes Comunales del Gobierno de Ciudad de Buenos Aires

## Pre requisitos
- Python 3.11
- Django 4.2
- Virtualenv
  

### Instalación
1. Crear entono virtual: 
``` python3 -m venv venv ```

2. Activar el entorno virtual:
```venv\Scripts\activate ```

3. Instalar dependencias:
``` pip install -r requirements.txt ``` 

4. Generar los scripts para crear las migraciones (BD):
``` python3 manage.py makemigrations ``` 

5. Aplicar las migraciones en la BD:
```  python3 manage.py migrate ``` 

6. Crear super usuario para acceder al /admin/
``` python3 manage.py createsuperuser```

7. Levantar un servidor local para servir la aplicación en el localhost:8000
``` python3 manage.py runserver``` 

