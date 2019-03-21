import os


class Config(object):
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    CSRF_ENABLED = True
    SECRET_KEY = os.urandom(16)
    ICS_STORAGE_FOLDER = os.path.join(BASE_DIR, 'ics')