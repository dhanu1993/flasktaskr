import os

basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = 'flasktaskr.db'
USERNAME = 'admin'
PASSWORD = 'admin'
WTF_CSRF_ENABLED = True
SECRET_KEY = "WK\xd1DS\x0f,\xc1\x8dPZ\x0b%c\xaa\xf22z:R\xc2\x8a#\x95"

DATABASE_PATH = os.path.join(basedir, DATABASE)