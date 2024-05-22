#include <WiFi.h>
#include <HTTPClient.h>
#include <Servo.h>

const char* ssid = "SatyaM31";
const char* password = "Satya123";
const char* serverUrl = "http://192.168.182.184:5000/capture_and_predict";

Servo servoMotor;
const int servoPin = 2;
const int ultrasonicTriggerPin = 5; 
const int ultrasonicEchoPin = 18; 

void setup() {
  Serial.begin(115200);
  servoMotor.attach(servoPin);
  pinMode(ultrasonicTriggerPin, OUTPUT); 
  pinMode(ultrasonicEchoPin, INPUT); 
  connectToWiFi();
  servoMotor.write(0);
  delay(5000);
}

void loop() {
  if (detectObject()) {
    sendSignalToServer();
    delay(6000);
  }
}

void connectToWiFi() {
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
  Serial.println(WiFi.localIP());
}

bool detectObject() {
  digitalWrite(ultrasonicTriggerPin, LOW);
  delayMicroseconds(2);
  digitalWrite(ultrasonicTriggerPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(ultrasonicTriggerPin, LOW);

  unsigned long duration = pulseIn(ultrasonicEchoPin, HIGH);
  unsigned long distance = duration * 0.034 / 2;
  Serial.print("Distance: ");
  Serial.println(distance);
  return distance < 13.5;
}

void sendSignalToServer() {
  HTTPClient http;
  http.begin(serverUrl);
  int httpResponseCode = http.GET();
  delay(2000);
  if (httpResponseCode > 0) {
    Serial.println("Signal sent to server");
    delay(1000); 
    String response = http.getString(); 
    controlServo(response); 
  }
  else {
    Serial.println("Error sending signal to server");
  }
  http.end();
}

void controlServo(String response) {
  if (response == "1") {
    // Rotate servo clockwise
    Serial.println("Organic garbage detected");
    servoMotor.write(0);
    delay(1000); 
    servoMotor.write(90); 
    delay(5000); 
  } else if (response == "0") {
    // Rotate servo anticlockwise
    Serial.println("Inorganic garbage detected");
    servoMotor.write(180); 
    delay(1000); 
    servoMotor.write(90);
    delay(5000);
  } else {
    Serial.println("Invalid response from server");
  }
}
