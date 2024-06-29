/*---------------------------------------------------------------------------------------------------------

CONNECTION RELATED FUNCTIONS ARE DEFINED HERE. THIS FILE WORKS WITH SOME GLOBAL VARIABLES LIKE SSID AND
PASSKEY. THE FOLLOWING FUNCTIONS ARE DEFINED HERE

    * configWifiStation
    * wifiIsConnected
    * callback

THE CALLBACK FUNCTION IS THE FUNCTION THAT GETS EXECUTED WHEN A MESSAGE ARRIVES AT THE TOPIC THIS MICRO
CONTROLLER IS SUBSCRIBED TO

------------------------------------------------------------------------------------------------------------*/

#ifndef CONNECTIONS_H
#define CONNECTIONS_H
#include "header.h"




/**
 * Connects the microcontroller to a wifi network.
 * In a failed attempt, it tries 20 times, each time
 * using 0.65 seeconds
 */
bool configWiFiStation(const char * ssid, const char * passkey)
{
    unsigned int WiFiConnectAttempt = 20;
    WiFi.mode(WIFI_STA);
    Serial.print("\n\n\nConnecting WiFi to ");
    Serial.println(ssid);

    WiFi.begin(ssid, passkey);
    while (((!wiFiIsConnected()) && (WiFiConnectAttempt != 0)))
    {
      // Loop to reattempt wifi connection if not connected and connect Attempt not exceeded
      WiFi.begin(ssid, passkey);
      Serial.print(".");
      WiFiConnectAttempt -= 1;
      delay(500);
    }

    if (wiFiIsConnected()){
        Serial.print("\nWiFi Connected to ");
        Serial.print(ssid);
        Serial.print(" \nIP Address: ");
        Serial.println(WiFi.localIP());
        return (true);
    }
    Serial.println("Wifi Connection Failed");
    return (false);
}





bool wiFiIsConnected(){
    return (WiFi.status() == WL_CONNECTED);
}





/**
 * This function gets executed everytime a message is sent to the device
 *
 * @topic: The topic the message arrived at
 * @payload: The message
 * @length: Length of message in bytes
 *
 * This function does the following
 *  - Splits the json message into variables
 *  - Updates global variables accordingly
 *      . currentState to set device new state
 *      . change to signify a change of state
 *  - Prints the received message
 */
void callback(char* topic, byte* payload, unsigned int length)
{
  bool ack = true;
  u_int8_t state = 3;

  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");

  char message[length + 1];
  memcpy(message, payload, length);
  message[length] = '\0';
  Serial.println(message);

  JsonDocument jsonDoc;
  DeserializationError error = deserializeJson(jsonDoc, message);
  
  if (error)
  {
    Serial.print("deserializeJson() failed: ");
    Serial.println(error.c_str());
    return;
  }

  // Extract values. Provision will be made for updating other variables
  if (jsonDoc.containsKey("state"))
  {
    state = jsonDoc["state"];
  }

  if (jsonDoc.containsKey("ack"))
  {
    ack = jsonDoc["ack"];
  }

  // Print extracted values
  Serial.print("State: ");
  Serial.println(state);
  Serial.print("Ack: ");
  Serial.println(ack);

  // The Logic
  if (state == 3)
  {
    acknowledge = true;
  }
  else if (state == 0 || state == 1 || state == 2)
  {
    currentState = state;
    change = true;
  }
  else
  {
    ;
  }

}
#endif // CONNECTIONS_H