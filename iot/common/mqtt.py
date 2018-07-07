'''MQTT Client'''
import json

import requests
from iot import mqtt

from config import Config

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    '''The callback for when the client receives a CONNACK response from the server.'''
    # Subscribing in on_connect() means that if we lose the connection and
    client.publish('MQTT', 'hello world')
    # reconnect then subscriptions will be renewed.
    client.subscribe(Config.MQTT_TOPIC)

@mqtt.on_message()
def handle_mqtt_message(client, userdata, msg):
    '''The callback for when a PUBLISH message is received from the server.'''
    # print(msg.topic + ' ' + msg.payload.decode())
    device_data = msg.payload.decode().split('|')
    time, name = device_data[0].split(',')
    data = device_data[1]

    #post mqtt status data to server using json
    json_data = json.dumps({'time': time,
                            'name': name,
                            'data': data})

    try:
        headers = {'Content-Type': 'application/json'}
        res = requests.post(Config.API_URL,
                            headers=headers,
                            data=json_data,
                            auth=requests.auth.HTTPBasicAuth(Config.ADMIN_USERNAME,
                                                             Config.ADMIN_PASSWORD))
    except requests.exceptions.ConnectionError:
        print('iot server offline')
