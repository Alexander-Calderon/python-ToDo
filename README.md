 
# TODO App

Aplicación que permite la gestión de tareas, desarrollado para el curso de IA Generativa.
**Ir al sitio:** 

[![TodoApp](https://img.shields.io/badge/Website-TodoApp-4c8bf5?logo=appveyor&logoColor=white&style=for-the-badge)](https://todoapp.alexandercalderon.dev)



## Características
- Agregar nuevas tareas
- Listar tareas (todas, pendientes, completadas)
- Marcar tareas como completadas
- Eliminar tareas completadas
- Exportar/Importar tareas en formato JSON
- Interfaz gráfica con Streamlit


## Tecnologías utilizadas
- Python: Lenguaje de programación utilizado.
- Streamlit: Librería de Python para crear interfaces gráficas de manera rápida y sencilla.
- SQLAlchemy: Toolkit SQL para Python, usado como ORM para la gestión de la bd (sqlite en este caso).



## Instalación

### Instalación directa en la máquina Host

**(Requisitos Previos)**
Python 3 y pip3 instalado en el sistema.

##### Crear entorno virtual
```
python -m venv venv-todo
```
ó
```
python3 -m venv venv-todo
```

Donde `venv-todo` es el nombre del entorno virtual.

##### Activar entorno virtual
**Linux/Mac**: 
```
source venv-todo/bin/activate
```

**Windows**:
```
venv-todo\Scripts\activate
```
##### Instalar dependencias
```
pip install -r requirements.txt
```
##### Lanzar aplicación
```
streamlit run app.py
```

Una vez lanzada, se mostrará en pantalla la información para acceder a la aplicación desde el navegador.


### Docker
**Requisitos Previos**
- Tener docker instalado:
	**Linux/Windows(WSL2)**
	https://docs.docker.com/engine/install/ubuntu/
	(Seleccionar la distro que utilices)
	
	**Mac**
	https://docs.docker.com/desktop/setup/install/mac-install/
	
	**Windows**
	https://docs.docker.com/desktop/setup/install/windows-install/


##### Compilar la imagen
Desde el directorio raiz que contiene el Dockerfile, ejecutar
```
docker build --no-cache -t todo-app .
```

##### Correr contenedor
```
docker run --rm -p 8500:8501 todo-app
```
El proyecto quedará accesible desde el puerto 8500 desde la máquina Host.


## Estructura del Proyecto

- `app.py`: EntryPoint de la aplicación.
- `app`: Vista de la aplicación.
- `models`: Carpeta del modelo implementado utilizando SQLAlchemy.
- `db`: Base de datos.
- `requirements.txt`: Dependencias del proyecto.


#### Extras

**Posibles mejoras a implementar (incluyendo en caso de que la aplicación necesite escalar):**
- Carpeta Assets
- Separar la lógica en Servicios y Repositorios.
- Generalizar componentes web para su reutilización en las vistas (`components`).
- Extraer funcionalidades de manera mas estructurada, como la manipulación de archivos Json, su lectura y escritura.


## Badges  

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)
[![AGPL License](https://img.shields.io/badge/license-AGPL-blue.svg)](http://www.gnu.org/licenses/agpl-3.0)

