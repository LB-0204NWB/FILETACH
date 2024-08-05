# MQTT-Based Device Control Application
### Overview
This project is a Python-based application that utilizes MQTT to control and monitor multiple devices. It features a graphical user interface (GUI) built using PyQt5 and a hand gesture recognition system using MediaPipe and OpenCV.

### Features
Control up to 5 devices via MQTT.
Real-time status updates of devices.
Hand gesture recognition for device control.
Two-page navigation interface.
### Requirements
Python 3.x
PyQt5
paho-mqtt
opencv-python
mediapipe
numpy
pickle
### Installation
Clone the repository:
```sh
git clone https://github.com/yourusername/mqtt-device-control.git
cd mqtt-device-control
Install the required packages:
```

```sh
pip install PyQt5 paho-mqtt opencv-python mediapipe numpy
```
### Setup
1. Ensure that your MQTT broker is running and accessible.
2. Update the MQTT broker address and port in main.py:
```python
mqtt_client = MQTTClient("your_broker_address", your_port)
```
3. Place the FILEUP2.pkl file in the src directory.
### Usage
1. Run the application:

```sh
python main.py
```
2. The main window will appear with the control panel for the devices.

3. Use the buttons to switch devices on and off. The status will be updated in real-time.

4. Navigate to the second page to use hand gestures for controlling the devices.

### Code Structure
* main.py: The entry point of the application. It initializes the MQTT client and the main window.
* mqtt_client.py: Defines the MQTTClient class for handling MQTT connections and messages.
* display.py: Contains the GUI definitions including the main window, device controls, and navigation.
* handscustom.py: Implements the hand gesture recognition and camera handling.
## Classes and Functions
### main.py
 * Functions:
  *resource_path(relative_path): Returns the absolute path to the resource.
### Main Block:
* Initializes the MQTTClient and MainWindow.
### mqtt_client.py
* Class MQTTClient(QObject)
* Manages MQTT connections and message handling.
### display.py
* Class CustomSwitch(QPushButton)
* Custom switch button for device control.
* Class FirstPage(QWidget)
* The first page of the application with device controls.
* Class MainWindow(QWidget)
* The main application window.
### handscustom.py
Class SecondPage(QWidget)
The second page with hand gesture recognition for device control.
# License
This project is licensed under the MIT License. See the LICENSE file for more details.

# Contact
For any questions or suggestions, please contact Longbach0204@gmail.com
