import json
import random
from paho.mqtt import client as mqtt_client


def write_json(store_path, data):
    with open(store_path, 'w') as jsonFile:
        json.dump(data, jsonFile, indent=4)


def read_json(store_path):
    with open(store_path, 'r') as jsonFile:
        data = json.loads(jsonFile.read())
    return data


class MqttPublish:
    def __init__(self):
        self.settings = read_json('./settings.json')
        self.broker = self.settings['mqtt']['broker']
        self.port = int(self.settings['mqtt']['port'])
        self.username = self.settings['mqtt']['user']
        self.password = self.settings['mqtt']['pass']
        self.client_id = f'python-mqtt-{random.randint(0, 1000)}'

    def connect_mqtt(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

        client = mqtt_client.Client(self.client_id)
        # client.username_pw_set(self.username, self.password)
        client.on_connect = on_connect
        client.connect(self.broker, self.port)
        return client

    def publish(self, topic='/python/mqtt', msg='no message'):
        client = self.connect_mqtt()
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
