import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'toplevel secret key')
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')

    XCLONE_MAIL_SUBJECT_PREFIX = '[Xcorps Clone]'
    XCLONE_MAIL_SENDER = 'Xcorps Admin <noreply@xcorp.com>'
    
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL', f"sqlite:///{os.path.join(basedir, 'site.db')}")

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL', 'sqlite://')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', f"sqlite:///{os.path.join(basedir, 'database.db')}")


config = {
    'development': DevelopmentConfig, 
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}