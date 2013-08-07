import os

class Config(object):
    DEBUG = False
    SECRET_KEY = '\n\xa6<\x12\x8d\xdc5\x15\x88\x95,\xcbz\xad\x9e\xda>\xaf\x1c\xe3\xff\x99\x9cG'

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        os.path.split(os.path.abspath(__file__))[0].replace("\\", "/") + \
        '/db.sqlite'

class PostgresConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = '' # fill in for using Postgres at home