# python-rest-google-drive
Servicio REST hecho en Python que comunica con Google Drive

## Proceso de Instalación
* Descargar proyecto
<br><code>git clone git@github.com:cesardramirez/python-rest-google-drive.git</code>
<br><code>cd /python-rest-google-drive</code>
* Crear un entorno virtual básico
<br><code>virtualenv -p /usr/bin/python3.4 venv</code>
<br><code>source venv/bin/activate</code>
<br><code>pip install --upgrade pip</code>
<br><code>pip install --upgrade setuptools</code>
* Instalar Google Client Library
<br><code>pip install --upgrade google-api-python-client oauth2client</code>
* Librerías para ejecutar Flask (Web Server)
<br><code>pip install --upgrade google-auth google-auth-oauthlib google-auth-httplib2</code>
<br><code>pip install --upgrade flask</code>
<br><code>pip install --upgrade requests</code>
* Ejecutar proyecto
<br><code>python app.py</code>

## Generar permisos en API Drive v3
1. Ingresar a [Google APIs](https://console.developers.google.com/).
2. Credenciales > Crear credenciales > ID de cliente de OAuth > Aplicación web > Crear.
3. Descargar archivo y renombrarlo como **client_secret.json**. Colocarlo en la raíz del proyecto.
<br>![](https://i.snag.gy/ElLeSI.jpg)
4. Al ejecutar la app por primera vez, aceptar los permisos.
<br>![](https://i.snag.gy/luMFDr.jpg)
5. Revisar los enlaces actuales de la api para visualizarlas.
<br>![](https://i.snag.gy/XPwg89.jpg)