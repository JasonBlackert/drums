"""
    Author: Jason E. Blackert
    Project: D.RU.M.S.
    Purpose: Serve as an application for monitoring the dog run at the
             Poneck residence.
"""

import sys

import cv2
import numpy as np
from broker import MqttBroker
from config import parse_args
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget

"""
Face Detection:
haarcascade_frontalface_default.xml: Detects frontal faces in images.
haarcascade_frontalface_alt.xml: An alternative frontal face detector.
haarcascade_profileface.xml: Detects profile faces in images.
haarcascade_eye.xml: Detects eyes within the detected face regions.
haarcascade_smile.xml: Detects smiles within the detected face regions.
Eye Detection:

haarcascade_eye.xml: Detects eyes in images.
haarcascade_eye_tree_eyeglasses.xml: Detects eyes with eyeglasses in images.
Upper Body Detection:

haarcascade_upperbody.xml: Detects upper bodies (torso) in images.
Lower Body Detection:

haarcascade_lowerbody.xml: Detects lower bodies (waist and legs) in images.
Full Body Detection:

haarcascade_fullbody.xml: Detects full human bodies in images.
Cat Face Detection:

haarcascade_frontalcatface.xml: Detects frontal faces of cats in images.
License Plate Detection:

haarcascade_russian_plate_number.xml: Detects license plates with Russian numbers.
"""

args = parse_args()
config = args.config

MQTT_HOST = config["mqtt"]["host"]
MQTT_PORT = config["mqtt"]["port"]
MQTT_TOPIC = config["mqtt"]["topic"]

GEOMETRY = (1640, 1480)

COLOR_HUMAN = (0, 255, 0)
COLOR_CAT = (0, 0, 255)

HUMAN = "haarcascade_frontalface_default.xml"
HUMAN_BODY = "haarcascade_fullbody.xml"
CAT = "haarcascade_frontalcatface.xml"
CAT_EXT = "haarcascade_frontalcatface_extended.xml"


def object_detection(frame, cascade, color: tuple):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    entity = cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
    )

    for x, y, w, h in entity:
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)


class CameraWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Load the pre-trained face cascade classifier
        self.face_cascade = cv2.CascadeClassifier(HUMAN)
        self.cat_cascade = cv2.CascadeClassifier(CAT)

        # self.camera = cv2.VideoCapture(-1)
        # self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, GEOMETRY[0])
        # self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, GEOMETRY[1])

        self.broker = MqttBroker()
        self.broker.start()
        self.broker.client.subscribe(MQTT_TOPIC)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)  # "Looping Mechanism"
        self.timer.start(1000 // 30)  # Update every 30 milliseconds

    def update_frame(self):
        if self.broker.queue:
            frame = np.asarray(self.broker.queue.popleft())
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Resize frame to match window size
            # frame = cv2.resize(frame, (self.width(), self.height()))

            # object_detection(frame, self.face_cascade, COLOR_HUMAN)
            # object_detection(frame, self.cat_cascade, COLOR_CAT)

            image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(image)
            self.image_label.setPixmap(pixmap)

    def closeEvent(self, event):
        self.camera.release()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("D.RU.M.S.")
        self.setWindowIcon(QIcon("share/drums.png"))
        self.setGeometry(100, 100, GEOMETRY[0], GEOMETRY[1])

        self.camera = CameraWidget()
        self.setCentralWidget(self.camera)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
