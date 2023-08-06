#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from paho.mqtt import client as mqtt_client
import random
from pdb import set_trace as stop
import json

class Alarmer():
    def __init__(self, broker: str = 'broker.emqx.io', port: int = 1883) -> None:
        self.broker = broker
        self.port = port
        self.client = None

    def connect(self, topic, srv_id, dev_id, label, srv_type):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("[Alarmer] Connected to MQTT Broker: %s:%s!" % (self.broker, self.port))
            else:
                print("[Alarmer] Failed to connect, return code %d\n" % rc)

        self.client = mqtt_client.Client(f'python-alarmer-{random.randint(0, 1000)}')
        self.client.on_connect = on_connect
        self.client.connect(self.broker, self.port)
        self.client.loop_start()
        self.topic = topic
        self.alarm_msg = {
            "srv_id" = srv_id,
            "dev_id" = dev_id,
            "label" = label,
            "srv_type" = srv_type,
            "code_err" = -1,
            "code_severity" = -1,
            "time" = 0,
            "content" = ""
        }

    def alarm(self, code_err: int, code_severity: int, content: str):
        self.alarm_msg['code_err'] = code_err
        self.alarm_msg['code_severity'] = code_severity
        self.alarm_msg['content'] = content
        self.alarm_msg['time'] = time.time_ns()
        self.client.publish(self.topic, json.loads(self.alarm_msg), 1, False)