'''config'''
import configparser
import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))

def get_config(section, key):
    '''获取config配置文件'''
    config = configparser.ConfigParser()
    path = os.path.split(os.path.realpath(__file__))[0] + '/configuration/py.conf'
    config.read(path)
    return config.get(section, key)

class Config(object):
    SECRET_KEY = os.environ.get(
        'SECRET_KEY') or 'the quick brown fox jumps over the lazy dog'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASEDIR, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
