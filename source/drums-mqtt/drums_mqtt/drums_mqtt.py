import os
import time

import cv2
from broker import MqttBroker
from helpers import convert2bytearray
from PIL import Image

OPERATION = "PUBLISH"  # "SUBSCRIBE"
GEOMETRY = (1640, 1480)
FPS = 0.5


def main():
    while True:
        "Hello Worlds!"
        time.sleep(10)


def test():
    print("Hello Test!")


class Insight:
    def __init__(
        self,
        host: str = "10.0.0.18",
        port: int = 1883,
        topic: int = "Camera/capture",
    ):
        self.broker = MqttBroker()
        self.broker.start()

        self.host = host
        self.port = port
        self.topic = topic

    def main(self):
        print(f"Running from USER: {os.getenv('USER')}")

        if OPERATION == "PUBLISH":
            self.publish()
        elif OPERATION == "SUBSCRIBE":
            self.subscribe()
        else:
            pass

    def publish(self):
        self.camera = cv2.VideoCapture(-1)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, GEOMETRY[0])
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, GEOMETRY[1])

        while True:
            ret, frame = self.camera.read()

            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(frame)
                byte_array = convert2bytearray(image)
                self.broker.publish(self.topic, byte_array)

            time.sleep(1 / FPS)

    def check_camera_port(self):
        for i in range(0, 5):
            cap = cv2.VideoCapture(i)
            is_camera = cap.isOpened()
            if is_camera:
                print(f"Input {i} is a valid camera value for VIDEO_SOURCE")
                cap.release()
                time.sleep(3)


if __name__ == "__main__":
    insight = Insight()
    insight.main()
