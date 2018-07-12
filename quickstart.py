# coding=utf-8
"""
Muestra el uso básico de la API Drive v3.

Crea un servicio de la API Drive v3 API e imprime los nombres y los ids de los últimos 10 archivos
que el usuario ha tenido acceso.
"""
from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# Configurar el API Drive v3.
SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'
store = file.Storage('credentials.json')  # Al ejecutar el programa, modifica el archivo credentials.json.
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('drive', 'v3', http=creds.authorize(Http()))

# Llamar el API Drive v3.
results = service.files().list(
    pageSize=10, fields="nextPageToken, files(id, name)").execute()
items = results.get('files', [])
if not items:
    print('No files found.')
else:
    print('Files:')
    for item in items:
        print('{0} ({1})'.format(item['name'], item['id']))