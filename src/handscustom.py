import cv2
import mediapipe as mp
import numpy as np
import pickle
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap, QTransform
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QMessageBox
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class SecondPage(QWidget):
    def __init__(self, stacked_widget, mqtt_client):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.mqtt_client = mqtt_client
        self.initUI()

        self.capture = None
        self.initializeCamera()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=False,
                                         max_num_hands=1, min_detection_confidence=0.7)
        
        with open(resource_path('src/FILEUP2.pkl'), 'rb') as f:
            self.svm = pickle.load(f)

        self.mqtt_client.messageSignal.connect(self.handle_mqtt_message)

    def initUI(self):
        self.setGeometry(100, 100, 1200, 800)

        # Device statuses
        self.device_status_labels = []
        for i in range(1, 6):
            label = QLabel(f"Device {i}: OFF", self)
            label.setGeometry(20, 50 + (i-1)*130, 150, 50)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("""
                QLabel {
                    background-color: #ff0000;
                    color: white;
                    font-size: 16px;
                    border-radius: 10px;
                    padding: 10px;
                }
            """)
            self.device_status_labels.append(label)
        # Image paths
        image_paths = [
            resource_path("img/hand/OFF_1.jpg"),
            resource_path("img/hand/ON_1.jpg"),
            resource_path("img/hand/OFF_2.jpg"),
            resource_path("img/hand/ON_2.jpg"),
            resource_path("img/hand/OFF_3.jpg"),
            resource_path("img/hand/ON_3.jpg"),
            resource_path("img/hand/OFF_4.jpg"),
            resource_path("img/hand/ON_4.jpg"),
            resource_path("img/hand/OFF_5.jpg"),
            resource_path("img/hand/ON_5.jpg"),
        ]

        # Angle to rotate the image (in degrees)
        angle = 0

        for i, path in enumerate(image_paths):
            label = QLabel(self)
            label.setGeometry(200 + (i % 2) * 200, 20 + (i // 2) * 130, 120, 120)
            
            pixmap = QPixmap(path)
            
            # Create a QTransform object and rotate it by the specified angle
            transform = QTransform().rotate(angle)
            
            # Apply the transformation to the QPixmap
            rotated_pixmap = pixmap.transformed(transform, Qt.SmoothTransformation)
            
            label.setPixmap(rotated_pixmap.scaled(label.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
            label.setStyleSheet("""
                QLabel {
                    background-color: #f0f0f0;
                    border-radius: 5px;
                    padding: 5px;
                }
            """)

        # Camera label
        self.camera_label = QLabel("CAMERA KHUNG", self)
        self.camera_label.setGeometry(600, 50, 640, 480)
        self.camera_label.setStyleSheet("background-color: #4682b4;border-radius: 20px; color: white; font-size: 24px;")
        self.camera_label.setAlignment(Qt.AlignCenter)

        # Buttons
        start_button = QPushButton('BẬT CAM', self)
        start_button.setGeometry(650, 640, 150, 50)
        start_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        start_button.clicked.connect(self.startCamera)

        stop_button = QPushButton('TẮT CAM', self)
        stop_button.setGeometry(850, 640, 150, 50)
        stop_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                font-size: 16px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #e53935;
            }
        """)
        stop_button.clicked.connect(self.stopCamera)

        back_button = QPushButton('BACK PAGE', self)
        back_button.setGeometry(1050, 640, 150, 50)
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #008CBA;
                color: white;
                font-size: 16px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #007bb5;
            }
        """)
        back_button.clicked.connect(self.gotoBackPage)

    def initializeCamera(self):
        if self.capture is not None:
            self.capture.release()

        self.capture = cv2.VideoCapture(0)
        if not self.capture.isOpened():
            QMessageBox.warning(self, "Camera Error", "Không thể mở camera")
            return False

        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        actual_width = self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        actual_height = self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        print(f"Độ phân giải camera: {actual_width}x{actual_height}")

        return True

    def gotoBackPage(self):
        self.stacked_widget.setCurrentIndex(0)
        self.stopCamera()

    def startCamera(self):
        if self.capture is None or not self.capture.isOpened():
            if not self.initializeCamera():
                return
        self.timer.start(30)

    def stopCamera(self):
        self.timer.stop()
        if self.capture is not None:
            self.capture.release()
        self.camera_label.clear()

    def image_processed(self, hand_img):
        img_rgb = cv2.cvtColor(hand_img, cv2.COLOR_BGR2RGB)
        img_flip = cv2.flip(img_rgb, 1)
        
        results = self.hands.process(img_flip)

        if results.multi_hand_landmarks:
            landmarks = results.multi_hand_landmarks[0]
            data = []
            for landmark in landmarks.landmark:
                data.extend([landmark.x, landmark.y, landmark.z])
            return data
        else:
            return None

    def update_frame(self):
        if self.capture is None or not self.capture.isOpened():
            return

        ret, frame = self.capture.read()
        if ret:
            data = self.image_processed(frame)
            if data is not None:
                data = np.array(data)
                y_pred = self.svm.predict(data.reshape(-1, 63))
                text = str(y_pred[0])
                original_list = text.split("_")
                new_list = [item for item in original_list if item != 'device']
                print(new_list)
                self.mqtt_client.client.publish(f"LED{new_list[1]}/set", new_list[0])
            else:
                text = "UNKNOWN"

            font = cv2.FONT_HERSHEY_SIMPLEX
            org = (50, 100)
            fontScale = 3
            color = (255, 0, 0)
            thickness = 5
            frame = cv2.putText(frame, text, org, font, fontScale, color, thickness, cv2.LINE_AA)

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = QImage(frame_rgb.data, frame_rgb.shape[1], frame_rgb.shape[0], frame_rgb.strides[0], QImage.Format_RGB888)
            self.camera_label.setPixmap(QPixmap.fromImage(image).scaled(self.camera_label.size(), Qt.KeepAspectRatio))
        else:
            print("Không thể chụp khung hình")

    def handle_mqtt_message(self, topic, message):
        # if topic.startswith("LED") and topic.endswith("/status"):
        if message == "ON" or message == "OFF":
            device_number = int(topic[3])
            if 1 <= device_number <= 5:
                label = self.device_status_labels[device_number - 1]
                if message == "ON":
                    label.setText(f"Device {device_number}: ON")
                    label.setStyleSheet("""
                        QLabel {
                            background-color: #00ff00;
                            color: white;
                            font-size: 16px;
                            border-radius: 10px;
                            padding: 10px;
                        }
                    """)
                else:
                    label.setText(f"Device {device_number}: OFF")
                    label.setStyleSheet("""
                        QLabel {
                            background-color: #ff0000;
                            color: white;
                            font-size: 16px;
                            border-radius: 10px;
                            padding: 10px;
                        }
                    """)
