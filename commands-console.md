git clone git@github.com:cesardramirez/python-rest-google-drive.git
cd /python-rest-google-drive

# Crear entorno virtual básico.
virtualenv -p /usr/bin/python3.4 venv
source venv/bin/activate
pip install --upgrade pip
pip install --upgrade setuptools