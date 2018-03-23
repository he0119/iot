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
    SECRET_KEY = os.environ.get('SECRET_KEY') or \
        'the quick brown fox jumps over the lazy dog'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASEDIR, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MQTT_CLIENT_ID = "server2"
    # use the free broker from HIVEMQ
    MQTT_BROKER_URL = get_config('mqtt', 'url')
    # default port for non-tls connection
    MQTT_BROKER_PORT = int(get_config('mqtt', 'port'))
    # set the username here if you need authentication for the broker
    MQTT_USERNAME = get_config('mqtt', 'username')
    # set the password here if the broker demands authentication
    MQTT_PASSWORD = get_config('mqtt', 'password')
    # set the time interval for sending a ping to the broker to 5 seconds
    MQTT_KEEPALIVE = 5
    # set TLS to disabled for testing purposes
    MQTT_TLS_ENABLED = True
    # get ca from server
    MQTT_TLS_CA_CERTS = None
