import os

class Config(object):
    DEBUG = False
    SECRET_KEY = '\n\xa6<\x12\x8d\xdc5\x15\x88\x95,\xcbz\xad\x9e\xda>\xaf\x1c\xe3\xff\x99\x9cG'
    UPLOAD_FOLDER = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'msg', 'zip'])


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        os.path.split(os.path.abspath(__file__))[0].replace("\\", "/") + \
        '/db.sqlite'

class PostgresConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://jeff:XXXXXXXX@localhost:5432/taskplanner'
