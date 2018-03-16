import logging

import paho.mqtt.client as mqtt
import requests
from requests.auth import HTTPBasicAuth
import config

SERVER_USERNAME = config.get_config("server", "username")
SERVER_PASSWORD = config.get_config("server", "password")
MQTT_USERNAME = config.get_config("mqtt", "username")
MQTT_PASSWORD = config.get_config("mqtt", "password")


def on_connect(client, userdata, flags, rc):
    '''The callback for when the client receives a CONNACK response from the server.'''
    # print("Connected with result code " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    client.publish("MQTT", "hello world")
    # reconnect then subscriptions will be renewed.
    client.subscribe("status")


def on_message(client, userdata, msg):
    '''The callback for when a PUBLISH message is received from the server.'''
    # print(msg.topic + " " + msg.payload.decode())
    try:
        res = requests.post('http://127.0.0.1:5000/api/status', data=msg.payload.decode(), auth=HTTPBasicAuth(SERVER_USERNAME, SERVER_PASSWORD))
        if res.json()["status"] == "failed":
            print("failed")
    except requests.exceptions.ConnectionError:
        print("failed")
    except Exception as e:
        logging.exception(e)

def main():
    '''main function'''
    client = mqtt.Client("server")
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.connect("broker.shiftr.io")
    client.loop_forever()

if __name__ == '__main__':
    main()
