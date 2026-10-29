import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'tu_clave_secreta_aqui_cambia_esto'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '../bd_anuncios.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_HTTPONLY = True
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)

