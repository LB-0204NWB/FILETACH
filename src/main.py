import sys
import os
from PyQt5.QtWidgets import QApplication
from display import MainWindow
from mqtt_client import MQTTClient

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# Thêm thư mục src vào sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mqtt_client = MQTTClient("192.168.1.179", 1883)
    main_window = MainWindow(mqtt_client)
    sys.exit(app.exec_())
