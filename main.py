from operations import Operations

#Operations().list_files(5)
#Operations().upload_file('unnamed.jpg', 'files/unnamed.jpg', 'image/jpeg')
#Operations().download_file('1QlESUIuL89vOcLb05a6Eyaxk3rZr71DF', 'files/Document.pdf')
#Operations().create_folder('Google')
#Operations().insert_file_to_folder('10pc3yVHcVQrIaaGHdtwRFAkqhwNkjYPk', 'Example.png', 'files/Example.png', 'image/png')
#Operations().search_file("mimeType='image/jpeg'")  # Buscar imagenes jpg
Operations().search_file("name contains 'unnamed'")  # Buscar imagenes jpg