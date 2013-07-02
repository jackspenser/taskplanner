import os

class Config(object):
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        os.path.split(os.path.abspath(__file__))[0].replace("\\", "/") + \
        '/db.sqlite'

