'''config'''
import configparser
import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))

def get_config(section, key):
    '''read config in py.conf'''
    config = configparser.ConfigParser()
    path = os.path.split(os.path.realpath(__file__))[0] + '/configuration/py.conf'
    config.read(path)
    return config.get(section, key)

class Config(object):
    '''config'''
    SECRET_KEY = get_config('database', 'secret_key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASEDIR, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MQTT_CLIENT_ID = get_config('mqtt', 'id')
    # use the free broker
    MQTT_BROKER_URL = get_config('mqtt', 'url')
    # default port for non-tls connection
    MQTT_BROKER_PORT = int(get_config('mqtt', 'port'))
    # set the username here if you need authentication for the broker
    MQTT_USERNAME = get_config('mqtt', 'username')
    # set the password here if the broker demands authentication
    MQTT_PASSWORD = get_config('mqtt', 'password')
    # set TLS to disabled for testing purposes
    MQTT_TLS_ENABLED = True
    # get CA from server
    MQTT_TLS_CA_CERTS = None

    ADMIN_USERNAME = get_config('admin', 'username')
    ADMIN_PASSWORD = get_config('admin', 'password')
    ADMIN_EMAIL = get_config('admin', 'email')

    API_URL = 'http://127.0.0.1:5000/api/status'

    SWAGGER_URL = get_config('swagger', 'url')
    SWAGGER_API_URL = get_config('swagger', 'json')
