#include <WiFiS3.h>
#include <WebSocketClient.h>
#include "arduino_secrets.h" 
using namespace net;

WebSocketClient client;
char ssid[] = SECRET_SSID;    
char password[] = SECRET_PASS;    

void setup() {
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  delay(5000);
  Serial.println("Connecting to Wi-Fi");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println(".");
  }
  Serial.println("\nConnected to Wi-Fi!");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  client.onOpen([](WebSocket &ws) {
    Serial.println("OPENED!");
    const char message[]{ "Hello from Arduino client!" };
    ws.send(WebSocket::DataType::TEXT, message, strlen(message));
  });
  client.onClose([](WebSocket &ws, const WebSocket::CloseCode code,
                   const char *reason, uint16_t length) {
    // ...
  });
  client.onMessage([](WebSocket &ws, const WebSocket::DataType dataType,
                     const char *message, uint16_t length) {
    // ...
  });

  client.open("http://100.27.128.63:3333", 80);
  Serial.println("Opened?");
}

void loop() {
  client.listen();
  //  Serial.println("Looping...");
  //  delay(1000);  // Print every second
  // Nothing needed here for now
}