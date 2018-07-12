# coding=utf-8
import io

from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from auth import Auth


class Operations:
    def list_files(self, size):
        """
        Muestra el uso básico de la API Drive v3.

        Imprime los nombres y los ids de los últimos 10 archivos que el usuario ha tenido acceso.
        """
        drive_service = Auth().get_service()

        # Llamar el API Drive v3.
        results = drive_service.files().list(pageSize=size, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            print('No se encontraron los archivos.')
        else:
            print('Archivos:')
            for item in items:
                print('{0} ({1})'.format(item['name'], item['id']))

    def upload_file(self, filename, filepath, mimetype):
        drive_service = Auth().get_service()

        file_metadata = {'name': filename}
        media = MediaFileUpload(filepath, mimetype=mimetype)
        file = drive_service.files().create(body=file_metadata,
                                                           media_body=media,
                                                           fields='id').execute()
        print('Archivo cargado! ')
        print('ID Archivo: %s' % file.get('id'))

    def download_file(self, file_id, filepath):
        drive_service = Auth().get_service()

        request = drive_service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))
        with io.open(filepath, 'wb') as f:
            fh.seek(0)
            f.write(fh.read())
            print('Archivo %s descargado!' % file_id)

    def create_folder(self, foldername):
        drive_service = Auth().get_service()

        file_metadata = {
            'name': foldername,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        file = drive_service.files().create(body=file_metadata,
                                            fields='id').execute()
        print('Carpeta Creada!')
        print('ID Carpeta: %s' % file.get('id'))


