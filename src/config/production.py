"""Production configuration."""
from os import environ, path
from datetime import timedelta

# from dotenv import load_dotenv
# basedir = path.abspath(path.dirname(__file__))
# load_dotenv(path.join(basedir, '.env'))
# load_dotenv()

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

# '{dialect}+{driver}://{username}:{password}@{host}:{port}/{database}'.format(
#     dialect=environ.get('SQL_DIALECT'),
#     driver=environ.get('SQL_DRIVER'),
#     username=environ.get('SQL_USER'),
#     password=environ.get('SQL_PASSWORD'),
#     host=environ.get('HOST'),
#     port=environ.get('PORT'),
#     database=environ.get('DATABASE')
# )
