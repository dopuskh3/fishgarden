/*
  vim:set ft=c:syn on;
  Blink
  Turns on an LED on for one second, then off for one second, repeatedly.
 
  This example code is in the public domain.
 */

bool commandAvailable = false;
String command = "";
int pumpPin = 13;

void setup() {                
  Serial.begin(9600);
  command.reserve(200);
  pinMode(pumpPin, OUTPUT);
}

void serialEvent() {
  while (Serial.available()) {
   // get the new byte:
   char inChar = (char)Serial.read();
   // add it to the inputString:
   if (inChar == '\r'){
     continue;
   }
   if (inChar == '\n') {
     commandAvailable = true;
     continue;
   }
   command += inChar;
  }
}

void processCommand(){
  if(commandAvailable){
     commandAvailable = false;
     if (command.startsWith("light=")){
       int start = command.indexOf('=');
       String value=command.substring(start+1);
       int value = value.toInt();
       if ( value == 0 ){
         digitalWrite(light_pin, LOW);
         Serial.println("light=LOW");
       } else {
         digitalWrite(light_pin, HIGH);
         Serial.println("light=HIGH");
       }
     }
     command = "";
  }
}

void loop() {
  processCommand();
}
