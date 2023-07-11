"""Production configuration."""
from os import environ, path
from datetime import timedelta

# defaults
SECRET_KEY = environ.get('SECRET_KEY')
JWT_SECRET_KEY = environ.get('JWT_SECRET_KEY')
JWT_ACCESS_TOKEN_EXPIRES = timedelta(
    hours=int(environ.get('JWT_ACCESS_TOKEN_EXPIRES')))
JWT_REFRESH_TOKEN_EXPIRES = timedelta(
    days=int(environ.get('JWT_REFRESH_TOKEN_EXPIRES')))


# Others
FLASK_ENV = 'production'
DEBUG = False
TESTING = False
SESSION_COOKIE_SECURE = True
JWT_COOKIE_SECURE = True

# Database
SQL_HOST = environ.get('SQL_HOST')
SQL_USERNAME = environ.get('SQL_USERNAME')
SQL_PASSWORD = environ.get('SQL_PASSWORD')
SQL_DATABASE = environ.get('SQL_DATABASE')
DATABASE_URI = environ.get('DATABASE_URI')
