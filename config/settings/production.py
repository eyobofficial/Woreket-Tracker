from .base import *
from decouple import Csv


DEBUG = False
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())
