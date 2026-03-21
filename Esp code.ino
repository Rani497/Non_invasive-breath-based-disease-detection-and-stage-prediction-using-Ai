#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>
#include <Adafruit_SGP40.h>
#include <ArduinoJson.h>

#define MQ3_PIN 34    // GPIO 34 for MQ3
#define MQ135_PIN 35  // GPIO 35 for MQ135
#define DHT_PIN 4     // GPIO 4 for DHT22
#define DHT_TYPE DHT22

const char* ssid = "Nokia7.2";          // Your Wi-Fi SSID
const char* password = "asdfghjkl123";  // Your Wi-Fi password
const char* flaskIP = " 10.210.59.159";   // Flask server's IP address (same for both)
const int flaskPort = 5000;              // Flask port

DHT dht(DHT_PIN, DHT_TYPE);
Adafruit_SGP40 sgp;

void setup() {
  Serial.begin(9600);
  dht.begin();
  
  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to Wi-Fi...");
  }
  Serial.println("Connected to Wi-Fi");
  Serial.print("ESP32 IP: ");
  Serial.println(WiFi.localIP());
  
  if (!sgp.begin()) {
    Serial.println("SGP40 not found! Check I2C wiring.");
  } else {
    Serial.println("SGP40 OK");
  }
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    float humidity = dht.readHumidity();
    float temperature = dht.readTemperature();
    
    // MQ3 calculation (acetone)
    float rawMQ3 = analogRead(MQ3_PIN);
    float voltageMQ3 = rawMQ3 * (3.3 / 4095.0);
    float rsMQ3 = ((3.3 - voltageMQ3) / voltageMQ3) * 10;
    float ratioMQ3 = rsMQ3 / 60;
    float acetone = 0.4 * pow(ratioMQ3, -1.43);
    
    // MQ135 calculation (ammonia)
    float rawMQ135 = analogRead(MQ135_PIN);
    float voltageMQ135 = rawMQ135 * (3.3 / 4095.0);
    float rsMQ135 = ((3.3 - voltageMQ135) / voltageMQ135) * 10;
    float ratioMQ135 = rsMQ135 / 3.6;
    float ammonia = 0.1 * pow(ratioMQ135, -1.5);
    
    uint16_t vocIndex = sgp.measureVocIndex(temperature, humidity);
    
    // Create JSON
    StaticJsonDocument<200> doc;
    doc["temperature"] = temperature;
    doc["humidity"] = humidity;
    doc["acetone"] = acetone;
    doc["ammonia"] = ammonia;
    doc["vocIndex"] = vocIndex;
    
    // Send to Flask via HTTP POST
    HTTPClient http;
    String url = "http://" + String(flaskIP) + ":" + String(flaskPort) + "/data";
    http.begin(url);
    http.addHeader("Content-Type", "application/json");
    String jsonString;
    serializeJson(doc, jsonString);
    int httpResponseCode = http.POST(jsonString);
    
    if (httpResponseCode > 0) {
      Serial.println("Data sent to Flask: " + jsonString);
    } else {
      Serial.println("Error sending data: " + String(httpResponseCode));
    }
    http.end();
  } else {
    Serial.println("Wi-Fi disconnected");
  }
  
  delay(5000);
}