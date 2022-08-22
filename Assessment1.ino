#include "Peripherals.hpp"

// the setup() method runs once, when the sketch starts
void setup() {

  // initialise the debug serial
  Serial.begin(9600);
  Serial.println("IFN649 - Assessment 1");

  // initialise peripherals
  hc05Setup();
  ledSetup();
  dhtSetup();
}

void loop() {
  // Instantiates a data object
  SensorData *data = new SensorData;

  // Read from sensors and populate data object
  dhtRead(data);
  soilRead(data);

  // Shows activity using led
  ledToggle();

  // send data via bluetooth serial
  Serial1.println(data->toString());
  
  delay(1000); // wait for a second
}
