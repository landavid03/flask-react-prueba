import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Acceder a las variables de entorno
FLASK_APP = os.getenv("FLASK_APP")
FLASK_ENV = os.getenv("FLASK_ENV")
DATABASE_URL = os.getenv("DATABASE_URL")
LOG_LEVEL = os.getenv("LOG_LEVEL", "info")  # Valor predeterminado: info
API_KEY = os.getenv("API_KEY")
SWAGGER_URL_ENV = os.getenv("SWAGGER_URL")
SWAGGER_URL_YAML = os.getenv("SWAGGER_URL_YAML")
