#include <IRremote.h>

const int RECV_PIN = 7;
IRrecv irrecv(RECV_PIN);
decode_results results;
void setup() {
  Serial.end();
  Serial.begin(9600);
  irrecv.enableIRIn();

}

void loop() {
  int sensorStatus = digitalRead(RECV_PIN); 
  if (sensorStatus == 0){
        Serial.println(sensorStatus);
        delay(1000);
        irrecv.resume();

  }

}
