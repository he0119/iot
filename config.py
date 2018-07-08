'''config'''
import os


class Config(object):
    '''config'''
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(
        os.path.abspath(os.path.dirname(__file__)), 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MQTT_CLIENT_ID = os.environ.get('MQTT_CLIENT_ID')
    # Use the free broker
    MQTT_BROKER_URL = os.environ.get('MQTT_BROKER_URL')
    # Default port for non-tls connection
    MQTT_BROKER_PORT = int(os.environ.get('MQTT_BROKER_PORT'))
    # Set the username here if you need authentication for the broker
    MQTT_USERNAME = os.environ.get('MQTT_USERNAME')
    # Set the password here if the broker demands authentication
    MQTT_PASSWORD = os.environ.get('MQTT_PASSWORD')
    # Set TLS to disabled for testing purposes
    MQTT_TLS_ENABLED = True
    # Get CA from server
    MQTT_TLS_CA_CERTS = None
    # Get topic name for receving data
    MQTT_TOPIC = os.environ.get('MQTT_TOPIC')
    # Get topic name for controling device
    MQTT_CONTROL_TOPIC = os.environ.get('MQTT_CONTROL_TOPIC')

    MQTT_POST_URL = os.environ.get('MQTT_POST_URL')

    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL')

    SWAGGER_URL = os.environ.get('SWAGGER_URL')
    SWAGGER_API_URL = os.environ.get('SWAGGER_API_URL')
