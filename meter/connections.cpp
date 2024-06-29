#ifndef CONNECTIONS_H
#define CONNECTIONS_H
#include "header.h"


bool configWiFiStation(const char * ssid, const char * passkey)
{
    unsigned int WiFiConnectAttempt = 20;
    ssid = String(ssid);
    passkey = String(passkey);
    WiFi.mode(WIFI_STA);
    Serial.print("\n\n\nConnecting WiFi to " + ssid);

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
        Serial.print("\nWiFi Connected to " + ssid + "\nIP Address: ");
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
  bool ack;

  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");

  char message[length + 1];
  memcpy(message, payload, length);
  message[length] = '\0';
  Serial.println(message);

  StaticJsonDocument<200> jsonDoc;
  DeserializationError error = deserializeJson(jsonDoc, message);
  
  if (error)
  {
    Serial.print("deserializeJson() failed: ");
    Serial.println(error.c_str());
    return;
  }

  // Extract values. Provision will be made for updating other variables
  if (jsonDoc.containsKey("state") && jsonDoc.containsKey("ack"))
  {
    state = jsonDoc["state"];
    ack = jsonDoc["ack"];

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
  else
  {
    Serial.println("Required keys not found in JSON");
  }
}
#endif // CONNECTIONS_H