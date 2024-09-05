from PyQt5.QtCore import Qt, QTimer, QDateTime
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QStackedWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout
from handscustom import SecondPage

class CustomSwitch(QPushButton):
    def __init__(self, label_on, label_off, topic, mqtt_client, image_label, image_path_on, image_path_off, parent=None):
        super().__init__(parent)
        self.setCheckable(True)
        self.setMinimumSize(50, 30)
        self.setStyleSheet("""
            QPushButton {
                border: 2px solid #555;
                border-radius: 5px;
                background-color: #ff0000;
                color: white;   
                font-size: 12px;
                padding: 3px;
            }
            QPushButton:checked {
                background-color: #00ff00;
                color: white;
            }
        """)
        self.label_on = label_on
        self.label_off = label_off
        self.topic = topic
        self.mqtt_client = mqtt_client
        self.image_label = image_label
        self.image_path_on = image_path_on
        self.image_path_off = image_path_off
        self.update_label()
        self.update_image()
        self.toggled.connect(self.update_label)
        self.toggled.connect(self.update_image)
        self.toggled.connect(self.publish_state)

    def update_label(self):
        self.setText(self.label_on if self.isChecked() else self.label_off)

    def update_image(self):
        pixmap = QPixmap(self.image_path_on if self.isChecked() else self.image_path_off)
        self.image_label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.image_label.setAlignment(Qt.AlignCenter)
        self.apply_image_stylesheet()

    def apply_image_stylesheet(self):
        stylesheet = """
            QLabel {
                border: 1px solid #555;
                border-radius: 10px;
                padding: 5px;
                background-color: #f0f0f0;
            }
        """
        self.image_label.setStyleSheet(stylesheet)

    def publish_state(self):
        self.mqtt_client.client.publish(self.topic, "ON" if self.isChecked() else "OFF")

    def set_state(self, state):
        self.setChecked(state == "ON")
        self.update_label()
        self.update_image()

class FirstPage(QWidget):
    def __init__(self, stacked_widget, mqtt_client):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.mqtt_client = mqtt_client
        self.initUI()
        self.check_initial_state()

    def initUI(self):
        main_layout = QVBoxLayout()
        top_layout = QHBoxLayout()
        center_layout = QVBoxLayout()
        bottom_layout = QHBoxLayout()

        self.time_label = QLabel(self)
        self.date_label = QLabel(self)
        for label in (self.time_label, self.date_label):
            label.setStyleSheet("""
                font-size: 12px;
                border: 1px solid #007bff;
                border-radius: 5px;
                padding: 3px;
                background-color: #e6f2ff;
            """)
            label.setAlignment(Qt.AlignCenter)
        
        top_layout.addWidget(self.time_label)
        top_layout.addStretch(1)
        top_layout.addWidget(self.date_label)

        self.image_label = QLabel(self)
        main_image_path = "C:/Users/longb/Desktop/DOANTOINGHIEP/PJPY/FILE_tach/img/logo/LOGO.jpg"
        main_pixmap = QPixmap(main_image_path)
        self.image_label.setPixmap(main_pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.image_label.setAlignment(Qt.AlignCenter)
        center_layout.addWidget(self.image_label, alignment=Qt.AlignCenter)
        self.apply_main_image_stylesheet()

        uth_label = QLabel("UTH", self)
        uth_label.setStyleSheet("""
            font-size: 20px;
            color: white;
        """)
        uth_label.setAlignment(Qt.AlignCenter)
        center_layout.addWidget(uth_label, alignment=Qt.AlignCenter)
        
        center_layout.addStretch(1)

        image_path_on = "C:/Users/longb/Desktop/DOANTOINGHIEP/PJPY/FILE_tach/img/DEVICE_ON.jpg"
        image_path_off = "C:/Users/longb/Desktop/DOANTOINGHIEP/PJPY/FILE_tach/img/DEVICE_OFF.jpg"

        self.switches = []
        for i in range(1, 6):
            switch_layout = QVBoxLayout()
            switch_layout.setAlignment(Qt.AlignCenter)

            switch_image_label = QLabel(self)
            switch_image_label.setAlignment(Qt.AlignCenter)
            switch = CustomSwitch(f"Device {i} ON", f"Device {i} OFF", f"LED{i}", self.mqtt_client, switch_image_label, image_path_on, image_path_off)
            switch.setMinimumSize(60, 30)
            self.switches.append(switch)

            switch_layout.addWidget(switch_image_label)
            switch_layout.addWidget(switch, alignment=Qt.AlignCenter)
            bottom_layout.addLayout(switch_layout)

        center_layout.addLayout(bottom_layout)

        next_button = QPushButton('NEXT PAGE', self)
        next_button.setStyleSheet("""
            QPushButton {
                background-color: #008CBA;
                color: white;
                font-size: 14px;
                border-radius: 5px;            
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #0033bb;
            }
        """)
        next_button.clicked.connect(self.gotoNextPage)
        center_layout.addWidget(next_button, alignment=Qt.AlignRight)

        main_layout.addLayout(top_layout)
        main_layout.addLayout(center_layout)

        self.setLayout(main_layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        self.mqtt_client.messageSignal.connect(self.handle_status_message)

    def apply_main_image_stylesheet(self):
        stylesheet = """
            QLabel {
                border: 2px;
                border-radius: 10px;
                padding: 3px;
                background-color: #e6f2ff;
            }
        """
        self.image_label.setStyleSheet(stylesheet)

    def gotoNextPage(self):
        self.stacked_widget.setCurrentIndex(1)

    def update_time(self):
        current_time = QDateTime.currentDateTime()
        self.time_label.setText(current_time.toString("hh:mm:ss"))
        self.date_label.setText(current_time.toString("dd/MM/yyyy"))

    def update_switch_state(self, topic, message):
        switch_index = int(topic[3]) - 1
        if 0 <= switch_index < len(self.switches):
            self.switches[switch_index].set_state(message)

    def check_initial_state(self):
        for i in range(1, 6):
            self.mqtt_client.client.publish(f"LED{i}/get", "")
    
    def handle_status_message(self, topic, message):
        if topic.endswith("/status"):
            led_number = topic.split("/")[0]
            if led_number.startswith("LED"):
                self.update_switch_state(led_number, message)

class MainWindow(QWidget):
    def __init__(self, mqtt_client):
        super().__init__()
        self.mqtt_client = mqtt_client
        self.initUI()

    def initUI(self):
        self.stacked_widget = QStackedWidget()

        self.first_page = FirstPage(self.stacked_widget, self.mqtt_client)
        self.second_page = SecondPage(self.stacked_widget, self.mqtt_client)

        self.stacked_widget.addWidget(self.first_page)
        self.stacked_widget.addWidget(self.second_page)

        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)

        self.setWindowTitle('Two Page Navigation')
        self.setGeometry(0, 0, 800, 480)

        self.setStyleSheet("background-color: #635959;")

        self.show()

if __name__ == "__main__":
    import sys
    from mqtt_client import MQTTClient  # Assuming you have this module

    app = QApplication(sys.argv)
    mqtt_client = MQTTClient()  # Initialize your MQTT client
    window = MainWindow(mqtt_client)
    sys.exit(app.exec_())
