git clone git@github.com:cesardramirez/python-rest-google-drive.git
cd /python-rest-google-drive

# Crear entorno virtual básico.
virtualenv -p /usr/bin/python3.4 venv
source venv/bin/activate
pip install --upgrade pip
pip install --upgrade setuptools

# Instalar Google Client Library
pip install --upgrade google-api-python-client oauth2client

# Correr Principal
python main.py

# Web Server - Flask
pip install --upgrade google-auth google-auth-oauthlib google-auth-httplib2
pip install --upgrade flask
pip install --upgrade requests