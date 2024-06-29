/*----------------------------------------------------------------------------------------------

THE ROOT HEADER FILE. FOR COMPILIATION AND UPLOADEING OF CODE, RUNT THE setup.py SCRIPT
THIS SCRIPT FIRST CREATES OR OVERWRITE THE FILE "MAIN.INO", THEN FROM TOP TO BOTTOM IT
INSERTS THE HEADER.H FILE, METER.INO FILE AND OTHER .CPP FILE IN ANY ORDER

------------------------------------------------------------------------------------------------*/
#ifndef HEADER_H
#define HEADER_H

#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <Preferences.h>
#include <PubSubClient.h>

#define MQTT_PORT 1883

/*---------------------------------- Global Variables -------------------------------------------*/
u_int8_t currentState  = 0;
bool change = false;
bool acknowledge = false;

/*-------------------------------------- Test Variables ------------------------------------------*/
const char* MQTT_BROKER = "test.mosquitto.org";
const char* MQTT_SUB_TOPIC = "commands/1/2232332606"; // of the form "commands/<node>/<deviceID>"
const char* MQTT_PUB_TOPIC = "data/1/2232332606";     // of the form "data/<node>/<deviceID>"
const char* CLIENT_ID = "House A";

/*---------------------------------- Function Prototypes ------------------------------------------*/
float readCurrentData();
float readVoltageData();
float computePower(float current, float voltage);
bool configWiFiStation(const char * ssid, const char * passkey);
bool wiFiIsConnected();
uint32_t getUniqueID();
float stopTimer(unsigned long startTime);
void callback(char* topic, byte* payload, unsigned int length);
bool sendData(PubSubClient messenger, uint8_t state, float voltage, float current, float time);

#endif // HEADER_H