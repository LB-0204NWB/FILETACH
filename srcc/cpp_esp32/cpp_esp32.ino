#include <Adafruit_GFX.h>
#include <Adafruit_ST7735.h>
#include <SPI.h>
#include <WiFi.h>
#include <PubSubClient.h>

// Define the pins used for the display
#define TFT_CS    5
#define TFT_RST   17
#define TFT_DC    16
#define TFT_SDA   23
#define TFT_SCL   18

// Initialize the ST7735 display
Adafruit_ST7735 tft = Adafruit_ST7735(TFT_CS, TFT_DC, TFT_RST);

// WiFi and MQTT credentials
const char* ssid = "PASSS";
const char* password = "123456789";
const char* mqttServer = "192.168.137.21";   
const int mqttPort = 1883;

// Initialize WiFi and MQTT clients
WiFiClient espClient;
PubSubClient client(espClient);

// Define colors in hexadecimal format
#define BACKGROUND_COLOR ST7735_BLUE
#define TEXT_COLOR ST7735_WHITE
#define LED_COLOR ST7735_RED
#define LED_ON_COLOR ST7735_GREEN

// Updated pin configuration
const int buttonPins[5] = {14, 25, 26, 27, 33};
const int ledPins[5] = {4, 12, 13, 15, 32};
bool wifiConnected = false;
bool mqttConnected = false;
bool ledStates[5] = {false, false, false, false, false};

uint16_t convertColor(uint32_t hexColor) {
  uint8_t r = (hexColor >> 16) & 0xFF;
  uint8_t g = (hexColor >> 8) & 0xFF;
  uint8_t b = hexColor & 0xFF;
  return tft.color565(r, g, b);
}

void setup() {
  Serial.begin(9600);
  
  // Initialize the SPI bus for the display
  SPI.begin(TFT_SCL, -1, TFT_SDA, TFT_CS);
  
  // Initialize the ST7735 display
  tft.initR(INITR_BLACKTAB);
  tft.setRotation(3);

  for (int i = 0; i < 5; i++) {
    pinMode(buttonPins[i], INPUT_PULLUP);
    pinMode(ledPins[i], OUTPUT);
    digitalWrite(ledPins[i], LOW);
  }

  // Connect to WiFi
  connectToWiFi();

  // Setup MQTT
  client.setServer(mqttServer, mqttPort);
  client.setCallback(mqttCallback);

  drawInterface();
}

void loop() {
  checkButtons();
  
  if (!client.connected()) {
    reconnectMQTT();
  }
  client.loop();

  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    handleCommand(command);
  }
}

void connectToWiFi() {
  tft.setCursor(10, 30);
  tft.setTextColor(TEXT_COLOR);
  tft.setTextSize(1);
  tft.print("Connecting to WiFi...");
  
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    tft.print(".");
  }

  wifiConnected = true;
  tft.println("Connected!");
  drawInterface();  // Update the WiFi indicator on the screen
}

void reconnectMQTT() {
  tft.setCursor(10, 60);
  tft.print("Connecting to MQTT...");
  
  while (!client.connected()) {
    if (client.connect("ESP32Client")) {  // Removed username and password
      mqttConnected = true;
      tft.println("Connected!");
      
      // Subscribe to multiple topics for different LEDs
      client.subscribe("LED1");
      client.subscribe("LED2");
      client.subscribe("LED3");
      client.subscribe("LED4");
      client.subscribe("LED5");
      drawInterface();  // Update the MQTT indicator on the screen
    } else {
      delay(5000);
    }
  }
}

void mqttCallback(char* topic, byte* payload, unsigned int length) {
  String message;
  for (unsigned int i = 0; i < length; i++) {
    message += (char)payload[i];
  }

  // Handle messages for multiple LEDs
  if (String(topic) == "LED1") {
    setLEDState(0, message == "ON");
  } else if (String(topic) == "LED2") {
    setLEDState(1, message == "ON");
  } else if (String(topic) == "LED3") {
    setLEDState(2, message == "ON");
  } else if (String(topic) == "LED4") {
    setLEDState(3, message == "ON");
  } else if (String(topic) == "LED5") {
    setLEDState(4, message == "ON");
  }
}

void drawInterface() {
  tft.fillScreen(BACKGROUND_COLOR);
  tft.setTextColor(TEXT_COLOR);
  
  // Title
  tft.setTextSize(1);
  tft.setCursor(30, 10);
  tft.println("DO AN TOT NGHIEP");
  
  // WIFI and MQTT indicators
  tft.setTextSize(1);
  tft.setCursor(tft.width() - 60, 25);
  tft.print("WIFI");
  drawIndicator(tft.width() - 30, 20, wifiConnected);
  
  tft.setCursor(tft.width() - 60, 55);
  tft.print("MQTT");
  drawIndicator(tft.width() - 30, 50, mqttConnected);
  
  // LEDs
  int ledWidth = 20;
  int ledSpacing = 10;
  int startX = 10;
  int startY = tft.height() - 40;
  
  for (int i = 0; i < 5; i++) {
    drawLED(startX + i * (ledWidth + ledSpacing), startY, 
            String("LED") + String(i + 1), 
            ledStates[i] ? LED_ON_COLOR : LED_COLOR);
  }
}

void drawIndicator(int x, int y, bool state) {
  tft.fillRect(x, y, 20, 20, state ? LED_ON_COLOR : LED_COLOR);
}

void drawLED(int x, int y, String label, uint16_t color) {
  tft.fillRect(x, y, 20, 20, color);
  tft.setTextColor(TEXT_COLOR);
  tft.setTextSize(1);
  tft.setCursor(x, y + 25);
  tft.print(label);
}

void handleCommand(String command) {
  command.trim();
  for (int i = 0; i < 5; i++) {
    if (command == "LED" + String(i+1) + " ON") {
      setLEDState(i, true);
    } else if (command == "LED" + String(i+1) + " OFF") {
      setLEDState(i, false);
    }
  }
}
void updateLED(int ledIndex) {
  int ledWidth = 20;
  int ledSpacing = 10;
  int startX = 10;
  int startY = tft.height() - 40; // Updated Y position to match drawInterface
  drawLED(startX + ledIndex * (ledWidth + ledSpacing), startY, 
          String("LED") + String(ledIndex + 1), 
          ledStates[ledIndex] ? LED_ON_COLOR : LED_COLOR);
}
void checkButtons() {
  for (int i = 0; i < 5; i++) {
    if (digitalRead(buttonPins[i]) == LOW) {
      delay(50); // Debounce
      if (digitalRead(buttonPins[i]) == LOW) {
        // Đảo trạng thái LED
        bool newState = !ledStates[i];
        setLEDState(i, newState);

        // Gửi trạng thái mới qua MQTT
        String topic = "LED" + String(i + 1);
        String message = newState ? "ON" : "OFF";
        client.publish(topic.c_str(), message.c_str());

        // Chờ nút được nhả ra
        while (digitalRead(buttonPins[i]) == LOW);
      }
    }
  }
}

void setLEDState(int ledIndex, bool state) {
  ledStates[ledIndex] = state;
  digitalWrite(ledPins[ledIndex], state ? HIGH : LOW);
  updateLED(ledIndex);  // Cập nhật màn hình với trạng thái LED mới
}

