#include <MCP3008.h>
 
// define pin connections
#define CLOCK_PIN 9
#define MISO_PIN 10
#define MOSI_PIN 11
#define CS_PIN 12
 
// put pins inside MCP3008 constructor
MCP3008 adc(CLOCK_PIN, MOSI_PIN, MISO_PIN, CS_PIN);
 
void setup() 
{
  Serial.begin(9600); // open serial port
}
 
void loop() 
{  
  // lees de voltage uit van de temperatuur sensor.
  int reading = adc.readADC(0); // lees kanaal 1 van de MCP3008 ADC.
 
  // converteer de waarde naar een voltage, voor 3.3v arduino gebruik 3.3
  float voltage = reading * 5.0;
  voltage /= 1024.0; 
 
  // print de voltage naar de console.
  Serial.print(voltage); Serial.println(" volts");
 
  // converteer van 10 mV per graad met 500mV offset naar graden (voltage - 500mV) x 100).
  float temperatureC = (voltage - 0.5) * 100;
 
  // print de temperatuur naar de console.
  Serial.print(temperatureC); Serial.println(" degrees C");
 
  delay(1000); // wacht een seconde.
}
