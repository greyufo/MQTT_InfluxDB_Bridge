# MQTT InfluxDB Python Bridge

## Сделайте виртуальное окружение для питона

\$ python3 -m venv env

## активируйте окружение

\$ source env/bin/activate

## Установите зависимости

\$ pip install -r requirements.txt

## Настроить

config.py

> INFLUXDB_ADDRESS = адрес, где развернут InfluxDB
> INFLUXDB_USER = пользователь
> INFLUXDB_PASSWORD = пароль
> INFLUXDB_DATABASE = база данных для метрик
>
> MQTT_ADDRESS = адрес MQTT сервиса
> MQTT_PORT = порт
> MQTT_USER = пользователь
> MQTT_PASSWORD = пароль
> MQTT_TOPIC = название топика
> MQTT_CLIENT_ID = какое-то название вашего клиента, придумайте

## запустить скрипт

\$ python main.py
