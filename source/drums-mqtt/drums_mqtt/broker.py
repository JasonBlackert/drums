import itertools
import logging
from collections import deque

import paho.mqtt.client as mqtt
from config import parse_args
from helpers import conver2pilimage

args = parse_args()
config = args.config
log = logging.getLogger(__name__)

MQTT_TOPIC = config["mqtt"]["topic"]


class MqttBroker:
    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.queue = deque()

    def on_connect(self, client, userdata, flags, rc):
        log.info("client connected with result code " + str(rc))

    def on_message(self, client, userdata, msg):
        if msg.topic != MQTT_TOPIC:
            return
        print(f"{msg.topic}")
        image = conver2pilimage(msg.payload)
        image = image.convert("RGB")
        self.queue.append(image)

    def start(self):
        self.client.connect(config["mqtt"]["host"], config["mqtt"]["port"])
        self.client.loop_start()

    def publish(self, *args, **kwargs):
        return getattr(self.client, "publish")(*args, **kwargs)

    def multicast(self, cmds: list[str], msg="Multicasting") -> None:
        log.info(f"{msg}: {cmds}")
        for cmd in cmds:
            self.client.publish("Pulse/cmd", cmd)

    def unicast(self, cmds: list[str], macs: list[str], msg="Unicasting") -> None:
        log.info(f"{msg}: {cmds} to {macs}")
        for cmd, mac in itertools.product(cmds, macs):
            self.client.publish(f"Pulse/{mac}/cmd", cmd)
