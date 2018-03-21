import logging
from datetime import datetime
import json

import paho.mqtt.client as mqtt
import requests
from requests.auth import HTTPBasicAuth
import config

SERVER_USERNAME = config.get_config("server", "username")
SERVER_PASSWORD = config.get_config("server", "password")
MQTT_USERNAME = config.get_config("mqtt", "username")
MQTT_PASSWORD = config.get_config("mqtt", "password")
API_URL = "http://127.0.0.1:5000/api/status"
BROKER_SERVER = "broker.shiftr.io"

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
    device_data = msg.payload.decode().split(",")
    json_data = json.dumps({"code" : int(device_data[0]),
                            "temperature" : float(device_data[1]),
                            "relative_humidity" : float(device_data[2]),
                            "relay1" : True if device_data[3] == "ON" else False,
                            "relay2" : True if device_data[4] == "ON" else False,
                            "time" : device_data[5]})
    print(json_data)
    try:
        res = requests.post(API_URL,
                            data=json_data,
                            auth=HTTPBasicAuth(SERVER_USERNAME, SERVER_PASSWORD))
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
    client.connect(BROKER_SERVER)
    client.loop_forever()

if __name__ == '__main__':
    main()
