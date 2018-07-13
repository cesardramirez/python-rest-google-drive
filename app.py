# -*- coding: utf-8 -*-

import os
import flask
import requests

import google.oauth2.credentials as creden
import google_auth_oauthlib.flow as fw
from googleapiclient.discovery import build

# Esta variable especifica el nombre de un archivo que contiene la información de OAuth 2.0
# para esta apliación, incluyendo sus client_id y client_secret.
CLIENT_SECRETS_FILE = "client_secret.json"

# El scope de acceso de OAuth 2.0 permite un total acceso lectura/escritura de la cuenta del usuario
# autenticado y requiere solicitudes para usar una conexión SSL.
SCOPES = ['https://www.googleapis.com/auth/drive']
API_SERVICE_NAME = 'drive'
API_VERSION = 'v3'

app = flask.Flask(__name__)
# Nota: Se incluye una clave secreta en el ejemplo para que funcione.
# Si usa este código en su aplicación, reemplace esto con una clave secreta verdadera.
#app.secret_key = os.urandom(24)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


@app.route('/')
def index():
    return print_index_table()


@app.route('/test')
def test_api_request():
    if 'credentials' not in flask.session:
        return flask.redirect('authorize')

    # Carga credenciales de la sesión
    credentials = creden.Credentials(**flask.session['credentials'])
    drive = build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

    # Es como si realizara una peticion get con la url 'https://www.googleapis.com/drive/v3/files'
    # Crea una lista de los archivos de Google Drive del usuario autenticado.
    files = drive.files().list().execute()

    # Guarda las credenciales nuevamente en sesión en caso de que el token de acceso se haya actualizado.
    # Nota: En una app de producción, es probable que desee guardar estas credenciales en una base de datos persistente.
    flask.session['credentials'] = credentials_to_dict(credentials)

    return flask.jsonify(**files)  # Revisar con debug... pasa una lista a formato json.


@app.route('/authorize')
def authorize():
    # Crea una instancia de flujo (flow) para administrar los pasos de la autorización de OAuth 2.0
    flow = fw.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES)
    flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

    authorization_url, state = flow.authorization_url(
        # Habilita el acceso offline para que pueda actualizar un token de acceso sin pedir permiso al usuario.
        # Recomendado para web server apps.
        access_type='offline',
        # Habilita la autorización incremental. Recomenddado como una buena práctica.
        include_granted_scopes='true'
    )

    # Almanacena el estado para que la devolución pueda verificar la respuesta el servidor de autenticación.
    flask.session['state'] = state

    return flask.redirect(authorization_url)


@app.route('/oauth2callback')
def oauth2callback():
    # Especifica el estado cuando se está creando el flujo en el callback
    # para que pueda verificarse en la respuesta del servidor de autorización.
    state = flask.session['state']

    flow = fw.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

    # Utiliza la respuesta del servidor de autenticación para recuperar los tokens de OAuth 2.0.
    authorization_response = flask.request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Almacena las credenciales en la sesión.
    # Nota: En una app de producción, es probable que desee guardar estas credenciales en una base de datos persistente.
    credentials = flow.credentials
    flask.session['credentials'] = credentials_to_dict(credentials)

    return flask.redirect(flask.url_for('test_api_request'))


@app.route('/revoke')
def revoke():
    if 'credentials' not in flask.session:
        return 'Usted necesita <a href="/authorize">autorizar</a> ' \
               'antes de probar el código para revocar las credenciales.'

    credentials = creden.Credentials(**flask.session['credentials'])

    revoke = requests.post('https://accounts.google.com/o/oauth2/revoke',
                           params={'token': credentials.token},
                           headers = {'content-type': 'application/x-www-form-urlencoded'})

    status_code = getattr(revoke, 'status_code')
    if status_code == 200:
        return 'Las credenciales se revocaron con éxito.' + print_index_table()
    else:
        return 'Ocurrió un error. ' + print_index_table()


@app.route('/clear')
def clear_creentials():
    if 'credentials' in flask.session:
        del flask.session['credentials']

    return 'Las credenciales se han eliminado.<br><br>' + print_index_table()


def credentials_to_dict(credentials):
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }


def print_index_table():
    return '<table>' \
           '<tr><td><a href="/test">Prueba de una API request</a></td>' \
           '<td>Envíe una solicitud al API y vea una respuesta JSON formateada. ' \
           'Revise el flujo de la autorización si no hay credenciales almacenadas para el usuario.' \
           '</td></tr>' \
           '<tr><td><a href="/authorize">Pruebe el flujo de autenticación directamente</a></td>' \
           '<td>Vaya directamente al flujo de autorización. ' \
           'Si hay credenciales almacenadas, es posible que todavía no se le solicite ' \
           'volver a autorizar la aplicación.</td></tr>' \
           '<tr><td><a href="/revoke">Revocar credenciales actuales</a></td>' \
           '<td>Revoque el token de acceso asociado con la sesión del usuario actual. ' \
           'Después de revocar las credenciales, si va a la página de prueba, debería ' \
           'ver un error de <code>invalid_grant</code>.</td></tr>' \
           '<tr><td><a href="/clear">Borrar credenciales de la sesión de Flask</a></td>' \
           '<td>Borra el token de acceso almacenado actualmente de la sesión del usuario. ' \
           'Después de borrar el token, si vuelve a <a href="/test">probar la API Request</a>, ' \
           'debe volver al flujo e autenticación.</td></tr></table>'


if __name__ == '__main__':
    # Cuando se ejecuta localmente, desactive la verificación HTTPs de OAuthlib.
    # Nota: Cuando se ejecute en producción NO deje esta opción habilitada.
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    # Especifica un nombre de host y un puerto que están configurados como un URI de redireccccionamiento
    # válido para su proyecto API en la consola de Google API.
    app.run('localhost', 8080, debug=True)