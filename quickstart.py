# coding=utf-8
from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# Configurar el API Drive v3.
SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'
CREDENTIALS_FILE = 'credentials.json'  # Al ejecutar el programa, modifica el archivo credentials.json.
CLIENT_SECRET_FILE = 'client_secret.json'


def get_credentials():
    """ Obtiene las credenciales de usuario válidas del storage.

    Si no ha almacenado nada, o si las credenciales almacenadas son inválidas,
    el flujo OAuth2 se completa para obtener las nuevas credenciales.

    Retorna:
        credentials, las credenciales obtenidas
    """
    store = file.Storage(CREDENTIALS_FILE)
    credentials = store.get()

    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        credentials = tools.run_flow(flow, store)
        print('Almacenamiento de credenciales para ' + CREDENTIALS_FILE)

    return credentials


def main():
    """
    Muestra el uso básico de la API Drive v3.

    Crea un servicio de la API Drive v3 API e imprime los nombres y los ids de los últimos 10 archivos
    que el usuario ha tenido acceso.
    """
    credentials = get_credentials()  # Obtiene las creenciales del método definido previamente.
    service = build('drive', 'v3', http=credentials.authorize(Http()))

    # Llamar el API Drive v3.
    results = service.files().list(pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No se encontraron los archivos.')
    else:
        print('Archivos:')
        for item in items:
            print('{0} ({1})'.format(item['name'], item['id']))