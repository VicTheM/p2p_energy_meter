#ifndef OPERATIONS_H
#define OPERATIONS_H
#include "header.h"

/*------------------------------------ Global Definitions ----------------------------------------*/
const char* WIFI_SSID = "Electrify"; // "unilag.wifi.int23"
const char* WIFI_PASSWORD = "Victory111"; //"2524767676"
const char* MQTT_BROKER = "test.mosquitto.org";
const char* MQTT_SUB_TOPIC = "commands/1/001"; // of the form "commands/<node>/<deviceID>"
const char* MQTT_PUB_TOPIC = "data/1/001";
const char* CLIENT_ID = "House A";

u_int8_t currentState  = 0;
bool change = false;
bool acknowledge = false;


/*------------------------------------ Function Definiions ----------------------------------------*/
/**
 * This function gets a unique ID for every esp32 hardware it is called on
 *
 * Return: A uint32_t bit number
 */
uint32_t getUniqueID()
{
  uint64_t chipid_64_bits = ESP.getEfuseMac(); // The chip ID is a 64-bit number
  uint32_t chipid_32_bits = (uint32_t)(chipid_64_bits >> 32) ^ (uint32_t)chipid_64_bits; // Convert to 32 bit
  
  return (chipid_32_bits);
}


/**
 * Interfaces with the ammeter module via one of the esp32 pins
 *
 * Return: Float, the current in milliAmps
 */
float readCurrentData()
{
    // For now, let's just return a random number

    return (random(220, 350));
}


/**
 * Interfaces with the voltemeter module via one of the esp32 pins
 *
 * Return: Float, the voltage in Volts
 */
float readVoltageData()
{
    // For now let's just assume it's 9 volts

    return (9);
}


/**
 * Multiplies the voltage by current to get power
 *
 * Return: Float, the power in Watts
 */
float computePower(float current, float voltage)
{
    return (current * voltage);
}


/**
 * This function checks how long several lines of code used between a start time and current time
 * Description: The start time should have been previously called using mills()
 *              It also caters for overflow
 *
 * Return: The elapsed time in seconds
 */
float stopTimer(unsigned long startTime) {
  unsigned long currentTime = millis();
  unsigned long elapsedTime;

  if (currentTime >= startTime) {
    elapsedTime = currentTime - startTime;
  } else {
    // Handle overflow
    elapsedTime = (4294967295 - startTime + currentTime + 1);
  }

  return elapsedTime / 1000.0; // Convert milliseconds to seconds
}


/**
 * Send the MQTT data to the broker in the format as described in the documentation
 *
 * Return: 1 success, 0 failed
 */
bool sendData(uint8_t state, float voltage, float current, float time)
{
  // Esthablish a connection with the broker
  if (!client.connected()) {
    while (!client.connected()) {
      Serial.print("Attempting MQTT connection...");
      if (client.connect("House A"))
      {
        Serial.println("connected");
        client.subscribe(MQTT_SUB_TOPIC);
      } else {
        Serial.print("failed, rc=");
        Serial.print(client.state());
        Serial.println(" try again in 5 seconds");
        delay(5000);
      }
    }
  }

  JsonDocument doc;

  doc["state"] = state;
  doc["voltage"] = voltage;
  doc["current"] = current;
  doc["duration"] = time;

  char payload[1024];
  serializeJson(doc, payload);

  if (client.publish(MQTT_PUB_TOPIC, payload))
  {
    Serial.println("Message Pubilshed Successfully");
    return (true);
  }
  else
  {
    Serial.println("Publish Unsuccessful");
    return (false);
  }

  return (false);
}



#endif // OPERATIONS_H