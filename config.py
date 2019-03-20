import os


class Config(object):
    CSRF_ENABLED = True
    SECRET_KEY = os.urandom(16)