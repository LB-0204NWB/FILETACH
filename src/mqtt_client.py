from PyQt5.QtCore import QObject, pyqtSignal
import paho.mqtt.client as mqtt

class MQTTClient(QObject):
    messageSignal = pyqtSignal(str, str)

    def __init__(self, broker, port):
        super().__init__()
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_publish = self.on_publish

        self.client.connect(broker, port, 60)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {rc}")
        client.subscribe("#")
        for i in range(1, 6):
            client.subscribe(f"LED{i}")
            client.subscribe(f"LED{i}/status")
    
    def on_message(self, client, userdata, msg):
        message = msg.payload.decode()
        topic = msg.topic
        print(f"Received message: {message} on topic: {topic}")
        self.messageSignal.emit(topic, message)

    def on_publish(self, client, userdata, mid):
    
        print(f"Message ID {mid} published.")