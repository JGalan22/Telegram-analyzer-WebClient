# Telegram Analyzer

_Herramienta para visualización de la información recolectada de grupos y canales de Telegram_


### Pre-requisitos 📋

_Que cosas necesitas para instalar el software_

```
Python +3.6 

```
 Enlace para descargar [Python](https://www.python.org/downloads/)

### Instalación 🔧

_Pasos necesarios para instalar la herramienta._

_1 - Comprobar la versión de Python que tenemos instalada, ejecutamos UNO de las siguientes instrucciones._

```
python -V
python --version
```


_2 - Crear un directorio donde crearemos un entorno virtual_
_Crearemos el directorio en el path que queramos, por ejemplo:_

```
mkdir C:\tools\telegram-analyzer #Ejecutar en la terminal de Windows en este caso
```
_Crear el entorno virtual en el directorio creado_
```
virutalenv telegram-analyzer
```
Nota: En nuestro caso usamos virutalenv, para instalarlo:
```
pip install virtualenv
```
_3 - Descargar el proyecto en el directorio creado_

_4 - Activar el entorno virtual y posicionarnos en la carpeta de proyecto descargado._

_5 - Descargar todas las depenencias que están definidas en el archivo **requirements.txt** ejecutando:
```
pip install -r requirements.txt
```
Nota: Si nos aparece algún error revisar que estamos en el path correcto al mismo nivel que el archivo **requirements.txt**

_Si se ha seguido todo el proceso de instalación ya se puede usar la herramienta, pero antes configurar las credenciales.😁_

## Archivo de configuración ⚙️

_1 - Para poder usar la herramienta correctamente solo hay que meter los datos de la instancia de la base de datos donde se están guardando los datos obtenidos de telegram con [Telegram Analyzer CLI](https://gitlab.com/JesusGalan/telegram-analyzer-cli)_

_2 - Para introducir las claves de la base de datos es necesario hacerlo en el archivo settings.py que se encunetra en el siguente path._
```
python-telegram-analyzer/server/settings.py
```
_3 - Y se deberá editar la sección correspondiente con la base de datos, DATABASE_
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'yourBBDDName',
        'USER': 'yourBBDDUserName',
        'PASSWORD': 'yourBBDDpassword',
        'HOST': 'yourBBDDhostName',
        'PORT':  #yourBBDDport
    }
}
```
_ Ahora sí, todo listo para usar la herramienta._😉

### Ejemplos de uso 🔩

_Levantar en local la aplicación para poder visualizar los datos._
```
python manage.py runserver
```


## Construido con 🛠️

_Este proyecto se ha creado con:_

* [Django](https://www.djangoproject.com/) - Framework para desarrollar aplicaciones web
