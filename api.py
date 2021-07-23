import json
from main_lib import read_json, MqttPublish
from flask import Flask
from fritzbox.fritzbox import endpoint_manager as fritzbox_endpoint_manager

# READ: settings.json
settings = read_json('settings.json')

# API: configuration
app = Flask(__name__)
api_host = settings["api"]["host"]
api_port = settings["api"]["port"]
api_debug = settings["api"]["debug"]
api_threaded = settings["api"]["threaded"]

# MQTT: configuration
mqtt = MqttPublish()
mqtt_topic = settings['api']['mqtt_topic']


# MQTT: functions
def mqtt_pub(mqtt_msg):
    mqtt.publish(mqtt_topic, mqtt_msg)


# API: functions
def run_api():
    mqtt_msg = "{'api':{'status': 'start'}}"
    mqtt_pub(mqtt_msg)
    app.run(api_host, api_port, debug=api_debug, threaded=api_threaded)


# API: endpoints
@app.route("/")
@app.route("/fb/")
@app.route("/fritzbox/")
@app.route("/fb/<path:path>")
@app.route("/fritzbox/<path:path>")
def fritzbox(path=None):
    mqtt_msg = "{'send':'fritzbox/data'}"
    data = fritzbox_endpoint_manager(path)
    mqtt_pub(mqtt_msg)
    return data
