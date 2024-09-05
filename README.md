# Hand Gesture Recognition - MQTT Device Control

## Structure

```css
FILE_tach
├───img
│   ├───hand
│   │   ├───OFF_1.jpg
│   │   ├───OFF_2.jpg
│   │   ├───OFF_3.jpg
│   │   ├───OFF_4.jpg
│   │   ├───OFF_5.jpg
│   │   ├───ON_1.jpg
│   │   ├───ON_2.jpg
│   │   ├───ON_3.jpg
│   │   ├───ON_4.jpg
│   │   ├───ON_5.jpg
│   ├───logo
│   │   └───LOGO.jpg
│   ├───DEVICE_OFF.jpg
│   ├───DEVICE_ON.jpg
│   └───icon.ico
├───src
│   ├───__pycache__
│   ├───display.py
│   ├───FILEUP2.pkl
│   ├───handscustom.py
│   ├───main.py
│   └───mqtt_client.py
└───srcc
```

Overview
---------
This project is a Python application using MQTT to control and monitor multiple devices. The application has a graphical user interface (GUI) built with PyQt5 and a hand gesture recognition system using MediaPipe and OpenCV.

Features
---------
- Control up to 5 devices via MQTT.
- Real-time device status updates.
- Hand gesture recognition for device control.
- Two-page navigation interface.

Requirements
------------
- Python 3.x
- PyQt5
- paho-mqtt
- opencv-python
- mediapipe
- numpy
- pickle

Installation
------------
1. Clone the repository:
```sh
    git clone https://github.com/yourusername/mqtt-device-control.git
    cd mqtt-device-control
```

2. Install the required packages:
```sh
    pip install PyQt5 paho-mqtt opencv-python mediapipe numpy
```

Configuration
-------------
1. Ensure your MQTT broker is running and accessible.
2. Update the MQTT broker's address and port in `main.py`:
   ```python
   mqtt_client = MQTTClient("your_broker_address", your_port)
   ```
3. Place the `FILEUP2.pkl` file in the `src` directory.

Usage
-----
1. Run the application:
```sh
    python main.py
```

2. The main window will display the control panel for the devices.
3. Use the buttons to turn devices on or off. The status will update in real-time.
4. Switch to the second page to use hand gestures to control the devices.

Code Structure
--------------
- `main.py`: The entry point of the application. Initializes the MQTT client and the main window.
- `mqtt_client.py`: Defines the `MQTTClient` class to handle MQTT connections and messages.
- `display.py`: Contains the GUI definitions, including the main window, device controls, and navigation.
- `handscustom.py`: Implements hand gesture recognition and camera handling.

Classes and Functions
---------------------
#### `main.py`
- Functions:
  - `resource_path(relative_path)`: Returns the absolute path to a resource.
- Main block:
  - Initializes `MQTTClient` and `MainWindow`.

#### `mqtt_client.py`
- `MQTTClient(QObject)` class:
  - Manages MQTT connections and message handling.

#### `display.py`
- `CustomSwitch(QPushButton)` class:
  - A custom switch button to control devices.
- `FirstPage(QWidget)` class:
  - The first page of the application with device controls.
- `MainWindow(QWidget)` class:
  - The main application window.

#### `handscustom.py`
- `SecondPage(QWidget)` class:
  - The second page with hand gesture recognition to control devices.


## PCB DESIGN
### SCHEMATIC
![image](https://github.com/user-attachments/assets/86b4b202-7805-43f8-a78a-57df520db9d9)
### PCB
![image](https://github.com/user-attachments/assets/18be5ee3-6517-491d-b6ad-29a7e933e1ec)
![image](https://github.com/user-attachments/assets/c4925566-0b25-4513-89e9-f811ef948151)


