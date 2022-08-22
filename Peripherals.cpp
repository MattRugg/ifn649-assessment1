#include "DHT.h"
#include "SensorData.hpp"

// DHT sensor type
#define DHTTYPE DHT11   // DHT 11

// Pin mapping
const int dhtPin = 21;     // Digital pin connected to the DHT sensor
const int ledPin = 11;
const int soilPin = 20;

// Initialises the DHT sensor
DHT dht(dhtPin, DHTTYPE);

void hc05Setup()
{
  // Set HC-05 serial baudrate in data mode
  Serial1.begin(9600);
}

void dhtSetup()
{
  dht.begin();
}

void dhtRead(SensorData *sensorData)
{

  // Reading temperature or humidity takes about 250 milliseconds!
  // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
  sensorData->airHumidityPercentage = dht.readHumidity();
  // Read temperature as Celsius (the default)
  sensorData->temperatureCelsius = dht.readTemperature();

  // Check if any reads failed and exit early (to try again).
  if (isnan(sensorData->airHumidityPercentage) || isnan(sensorData->temperatureCelsius))
  {
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  }

  // Compute heat index in Celsius (isFahreheit = false)
  sensorData->heatIndexCelsius = dht.computeHeatIndex(sensorData->temperatureCelsius, 
    sensorData->airHumidityPercentage, false);
}

void soilRead(SensorData *sensorData)
{
  int val = analogRead(soilPin);
  sensorData->soilHumidityPercentage = 100*val/1023;
}

void ledSetup()
{
  // initialize the digital pin as an output.
  pinMode(ledPin, OUTPUT);
}

void ledToggle()
{
  static bool ledState = false;
  digitalWrite(ledPin, ledState);
  ledState = !ledState;
}
