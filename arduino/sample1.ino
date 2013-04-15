#define MOISTURE_PIN 0
#define LIGHT_PIN 1
#define TEMPERATURE_PIN 2

int moisture_value;
int light_value;
int temperature_value;

void print_sensor_value(char *value){
}


void setup() {
  Serial.begin(9600); //open serial port
}

void loop() {
  
moisture_value = analogRead(MOISTURE_PIN); // read the value from the moisture-sensing probes

Serial.print("moisture=");
Serial.println( moisture_value );

delay(10);

light_value = analogRead(LIGHT_PIN);
Serial.print("light=");
Serial.println( light_value );

delay(10);

temperature_value = analogRead(TEMPERATURE_PIN);
Serial.print("temperature=");
Serial.println( temperature_value);

delay(1000);

}
