from dotenv import load_dotenv
from .settings import *

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['job-site-u07r.onrender.com']

CSRF_TRUSTED_ORIGINS = ['https://job-site-u07r.onrender.com']
