#coding=utf-8

import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ACXNLDDSA78979DSA7D'
    WTF_CSRF_ENABLED = False
    AUTH_STATE = 'YouCannotSeeMe!'
    BABEL_DEFAULT_LOCALE = 'zh_CN'
    WAIT_LIST = []
    NOW_TIMES = '1'

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DATABASE = {
        'name': os.path.join(BASE_DIR, 'sqlite.db'),
        'engine': 'peewee.SqliteDatabase',
    }
    DEBUG = True


config = {
    'development':DevelopmentConfig,
    'default':DevelopmentConfig
}