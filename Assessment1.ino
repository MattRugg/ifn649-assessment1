#include "Peripherals.hpp"

// the setup() method runs once, when the sketch starts
void setup() {

  // initialise the debug serial
  Serial.begin(9600);
  Serial.println("IFN649 - Assessment 1");

  // initialise peripherals
  hc05Setup();
  ledSetup();
  buzzerSetup();
  dhtSetup();
}

void loop() 
{
  static elapsedMillis dataSendInterval;

  // fetch data and send it every 1.5 seconds
  if (dataSendInterval > 1500)
  {
    sendSensorData();
    dataSendInterval = 0;
  }

  // process commands from bluetooth serial
  // TODO change it to Serial1 when happy with commands
  if (Serial.available() > 0)
  {
    String str = Serial.readString().trim();
    Serial.print("received: ");
    Serial.println(str);

    // Proccess command received
    if(str == "LED_ON") 
    {
      ledOn();
    } 
    else if (str == "LED_OFF") 
    {
      ledOff();
    }
    else if (str == "BUZZER_TRACK1")
    {
      buzzerPlayTrack(0);
    } 
    else if (str == "BUZZER_TRACK2")
    {
      buzzerPlayTrack(1);
    }
    else
    {
      Serial.println("Command does not exist");
    }
      
  }  
}

void sendSensorData() 
{
  // Instantiates a data object
  SensorData *data = new SensorData;

  // Read from sensors and populate data object
  dhtRead(data);
  soilRead(data);

  // send data via bluetooth serial
  Serial1.println(data->toString());
}
