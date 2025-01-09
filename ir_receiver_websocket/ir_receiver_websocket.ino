#include "WiFiS3.h"
#include "arduino_secrets.h" 
#include "Arduino_LED_Matrix.h"
#include <IRremote.hpp>
#define DECODE_NEC          // Includes Apple and Onkyo. To enable all protocols , just comment/disable this line.


ArduinoLEDMatrix matrix;

char ssid[] = SECRET_SSID;    
char pass[] = SECRET_PASS;
char serverAddress[] = "100.27.128.63:3333";  // server address

int keyIndex = 0;            // your network key index number (needed only for WEP)
int IR_RECEIVE_PIN = 7;
int status = WL_IDLE_STATUS;
// if you don't want to use DNS (and reduce your sketch size)
// use the numeric IP instead of the name for the server:
IPAddress server(100,27,128,63);  // numeric IP for Google (no DNS)
// char server[] = "www.google.com";    // name address for Google (using DNS)

// Initialize the Ethernet client library
// with the IP address and port of the server
// that you want to connect to (port 80 is default for HTTP):
WiFiClient client;

/* -------------------------------------------------------------------------- */
void setup() {
/* -------------------------------------------------------------------------- */  
  //Initialize serial and wait for port to open:
  Serial.begin(9600);
  matrix.begin();
  const uint32_t happy[] = {
    0x19819,
    0x80000001,
    0x81f8000
  };
  matrix.loadFrame(happy);
  delay(500);
  IrReceiver.begin(7, true);
  Serial.print(F("Ready to receive IR signals of protocols: "));
  printActiveIRProtocols(&Serial);
  Serial.println("at pin " + String(IR_RECEIVE_PIN));
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  
  // check for the WiFi module:
  if (WiFi.status() == WL_NO_MODULE) {
    Serial.println("Communication with WiFi module failed!");
    // don't continue
    while (true);
  }
  
  String fv = WiFi.firmwareVersion();
  if (fv < WIFI_FIRMWARE_LATEST_VERSION) {
    Serial.println("Please upgrade the firmware");
  }
  
  // attempt to connect to WiFi network:
  while (status != WL_CONNECTED) {
    Serial.print("Attempting to connect to SSID: ");
    Serial.println(ssid);
    // Connect to WPA/WPA2 network. Change this line if using open or WEP network:
    status = WiFi.begin(ssid);
     
    // wait 10 seconds for connection:
    delay(10000);
  }
  
  printWifiStatus();
  const uint32_t heart[] = {
      0x3184a444,
      0x44042081,
      0x100a0040
  };

  matrix.loadFrame(heart);

 
  Serial.println("\nStarting connection to server...");
  // if you get a connection, report back via serial:
  if (client.connect(server, 3333)) {
    Serial.println("connected to server");
  }
}

/* just wrap the received data up to 80 columns in the serial print*/
/* -------------------------------------------------------------------------- */
void read_response() {
/* -------------------------------------------------------------------------- */  
  uint32_t received_data_num = 0;
  while (client.available()) {
    /* actual data reception */
    char c = client.read();
    /* print data to serial port */
    Serial.print(c);
    /* wrap data to 80 columns*/
    received_data_num++;
    if(received_data_num % 80 == 0) { 
      Serial.println();
    }
  }  
}

/* -------------------------------------------------------------------------- */
void loop() {
/* -------------------------------------------------------------------------- */  
  read_response();

  // if the server's disconnected, stop the client:
  if (!client.connected()) {
    Serial.println();
    Serial.println("disconnecting from server.");
    client.stop();

    // do nothing forevermore:
    while (true);
  }
  if (IrReceiver.decode()) {

        /*
         * Print a summary of received data
         */
        if (IrReceiver.decodedIRData.protocol == UNKNOWN) {
            Serial.println(F("Received noise or an unknown (or not yet enabled) protocol"));
            // We have an unknown protocol here, print extended info
            IrReceiver.printIRResultRawFormatted(&Serial, true);
            IrReceiver.resume(); // Do it here, to preserve raw data for printing with printIRResultRawFormatted()
        } else {
            IrReceiver.resume(); // Early enable receiving of the next IR frame
            IrReceiver.printIRResultShort(&Serial);
            IrReceiver.printIRSendUsage(&Serial);
        }
        Serial.println();

        /*
         * Finally, check the received data and perform actions according to the received command
         */
        if (IrReceiver.decodedIRData.command == 0x58) {
          Serial.println("Red - primary");
           String payload = "{\"action\":\"play_music\",\"command\":\"0x58\"}";
          
        } else if (IrReceiver.decodedIRData.command == 0x59) {
          Serial.println("Red - primary");
          String payload = "{\"action\":\"play_music\",\"command\":\"0x59\"}";
            // do something else
        } else if (IrReceiver.decodedIRData.command == 0x45) {
          Serial.println("Red - primary");
           String payload = "{\"action\":\"play_music\",\"command\":\"0x45\"}";
            // do something else
        }
        // // Make a HTTP request:
        // // Construct the full HTTP POST request in one go
        String httpRequest = String("POST /api/play_music HTTP/1.1\r\n") +
                            "Host: http://100.27.128.63:3333\r\n" +
                            "Content-Type: application/json\r\n" +
                            "Content-Length: " + String(payload.length()) + "\r\n" +
                            "Connection: close\r\n\r\n" +  // End of headers
                            payload;                      // JSON payload

        // Send the HTTP POST request
        client.print(httpRequest);
        client.println("Connection: close");
        client.println();
        // do something
    }
}

/* -------------------------------------------------------------------------- */
void printWifiStatus() {
/* -------------------------------------------------------------------------- */  
  // print the SSID of the network you're attached to:
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  // print your board's IP address:
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);

  // print the received signal strength:
  long rssi = WiFi.RSSI();
  Serial.print("signal strength (RSSI):");
  Serial.print(rssi);
  Serial.println(" dBm");
}
