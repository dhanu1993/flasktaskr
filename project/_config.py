import os

basedir = os.path.abspath(os.path.dirname(__file__))
DATABASE = 'flasktaskr.db'
CSRF_ENABLED = True
SECRET_KEY = 'b\xfa\xe4\x94<\xd4wm\x84\x0f7\xe6)H\x0c\xe48\xedE\xcc^\xcaN?'

DATABASE_PATH = os.path.join(basedir, DATABASE)

SQLALCHEMY_DATABASE_URI = 'sqlite:///'+DATABASE_PATH
