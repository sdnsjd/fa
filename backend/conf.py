from dotenv import load_dotenv
import os
from fastapi.templating import Jinja2Templates

dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../.env'))
load_dotenv(dotenv_path)
secret_key = os.getenv('secret_key')

templates = Jinja2Templates(directory="frontend/templates")
UPLOAD_DIRECTORY = "frontend/static/images/"

