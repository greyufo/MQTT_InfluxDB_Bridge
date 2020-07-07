#!/usr/bin/env python3

"""A MQTT to InfluxDB Bridge

This script receives MQTT data from Tasmota firware Sonoff device and saves those to InfluxDB for Grafana.
Save Temperatue and Humidity values
Sonoff YH18 with Sensor Si7021

"""
import json

import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
from os import environ, path

from config import INFLUXDB_ADDRESS, INFLUXDB_USER, INFLUXDB_PASSWORD, INFLUXDB_DATABASE, MQTT_ADDRESS, MQTT_PORT, MQTT_USER, MQTT_PASSWORD, MQTT_TOPIC, MQTT_CLIENT_ID

MSG = ""
influxdb_client = InfluxDBClient(
    INFLUXDB_ADDRESS, 8086, INFLUXDB_USER, INFLUXDB_PASSWORD, None)


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("MQTT client connected OK")
    else:
        print("MQTT client didnt' connect, returned code=", rc)
    client.subscribe(MQTT_TOPIC)


def on_message(client, userdata, msg):

    MSG = json.loads(msg.payload.decode('utf-8'))

    if MSG is not None:
        _send_sensor_data_to_influxdb(MSG)


def _send_sensor_data_to_influxdb(msg):
    json_body = [
        {

            'time': msg["Time"].replace(' ', ''),
            "measurement": "Temperature",
            "fields": {
                "value": msg["SI7021"]["Temperature"]
            }
        }
    ]
    print(json_body)
    influxdb_client.write_points(json_body)

    json_body = [
        {
            'time': msg["Time"].replace(' ', ''),
            "measurement": "Humidity",
            "fields": {
                "value": msg["SI7021"]["Humidity"]
            }
        }
    ]
    print(json_body)
    influxdb_client.write_points(json_body)


def _init_influxdb_database():

    databases = influxdb_client.get_list_database()
    if len(list(filter(lambda x: x['name'] == INFLUXDB_DATABASE, databases))) == 0:
        influxdb_client.create_database(INFLUXDB_DATABASE)
    influxdb_client.switch_database(INFLUXDB_DATABASE)
    print('Selected DB')


def main():
    _init_influxdb_database()

    mqtt_client = mqtt.Client(MQTT_CLIENT_ID)
    mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect(MQTT_ADDRESS, MQTT_PORT)
    mqtt_client.loop_forever()


if __name__ == '__main__':
    print('MQTT to InfluxDB bridge')
    main()
