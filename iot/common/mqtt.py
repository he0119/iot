'''MQTT Client'''
import json

import requests
from iot import mqtt

from config import Config

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    '''The callback for when the client receives a CONNACK response from the server.'''
    print('MQTT : Connected with result code ' + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    client.publish('MQTT', 'hello world')
    # reconnect then subscriptions will be renewed.
    client.subscribe(Config.MQTT_TOPIC)

@mqtt.on_message()
def handle_mqtt_message(client, userdata, msg):
    '''The callback for when a PUBLISH message is received from the server.'''
    # print(msg.topic + ' ' + msg.payload.decode())
    device_data = msg.payload.decode().split(',')

    if device_data[1] == 'Error' or device_data[2] == 'Error':
        device_data[1] = None
        device_data[2] = None

    #post mqtt status data to server using json
    json_data = json.dumps({'code' : int(device_data[0]),
                            'temperature' : float(device_data[1]) if device_data[1] else None,
                            'relative_humidity': float(device_data[2]) if device_data[2] else None,
                            'relay1_status': True if device_data[3] == '1' else False,
                            'relay2_status': True if device_data[4] == '1' else False,
                            'time' : device_data[5]})

    try:
        headers = {'Content-Type': 'application/json'}
        res = requests.post(Config.API_URL,
                            headers=headers,
                            data=json_data,
                            auth=requests.auth.HTTPBasicAuth(Config.ADMIN_USERNAME,
                                                             Config.ADMIN_PASSWORD))
        if res.status_code == 400:
            print(res.json())
    except requests.exceptions.ConnectionError:
        print('iot server offline')
