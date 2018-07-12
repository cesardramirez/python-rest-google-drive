# coding=utf-8
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools


class Auth:
    # Configurar el API Drive v3.
    SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'
    CREDENTIALS_FILE = 'credentials.json'  # Al ejecutar el programa, modifica el archivo credentials.json.
    CLIENT_SECRET_FILE = 'client_secret.json'
    APPLICATION_NAME = 'API Drive Python Files'

    def get_credentials(self):
        """ Obtiene las credenciales de usuario válidas del storage.

        Si no ha almacenado nada, o si las credenciales almacenadas son inválidas,
        el flujo OAuth2 se completa para obtener las nuevas credenciales.

        Retorna:
            credentials, las credenciales obtenidas
        """
        store = file.Storage(self.CREDENTIALS_FILE)
        credentials = store.get()

        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(self.CLIENT_SECRET_FILE, self.SCOPES)
            flow.user_agent = self.APPLICATION_NAME
            credentials = tools.run_flow(flow, store)

        return credentials

    def get_service(self):
        """ Crea un servicio de la API Drive v3 API.

        Retorna:
            service
        """
        credentials = self.get_credentials()
        service = build('drive', 'v3', http=credentials.authorize(Http()))

        return service
