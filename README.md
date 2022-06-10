## Proyecto Final Encuestas Online

## Tabla de Contenidos

## Información General 
Aplicación para ofrecer servicios de gestión encuestas. Con perfil de administración, encuestador y usuario.

## Tecnologías
Este proyecto fue creado usando:
* HTML
* CSS
* Boostrap
* JavaScript
* JQuery
* Crispy Forms

## Instalación
Puede descargar este proyecto desde https://github.com/Patricia0livares

## Instrucciones para instalación

## Instalación

-Clonar el repositorio usando ``` git clone ```
-Se abre la carpeta en un editor Visual Studio Code.

-Se abre un nuevo terminal en Visual Studio Code y se crea el entorno virtual con el comando:
```pip install venv venv ```
-Se activa el entorno virtual:
```cd venv/Scripts/activate ```
-Despues de volver a la carpeta principal con cd .. Se instala los requerimientos
-Con el siguiente comando:
```pip install -r requirements.txt```
-Se hacen las migraciones con el comando:
``` python manage.py migrate```
-Se crea el superusuario para acceder al admin:
```python manage.py createsuperuser```
-Se levanta el servidor con:
``` python manage.py runserver```
