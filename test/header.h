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
#define SEND_FREQ (60000)          // How often data should be sent in millisecs. 60,000 = 1 minute

/*------------------------------------ Global Variables ----------------------------------------*/
extern const char* WIFI_SSID;
extern const char* WIFI_PASSWORD;
extern const int LOAD;
extern const int SUPPLY;
extern const int DISCONNECT;
extern const int VOLTAGE;
extern const int CURRENT;
extern u_int8_t currentState;
extern bool change;
extern bool acknowledge;
extern const char* MQTT_BROKER;
extern const char* MQTT_SUB_TOPIC;
extern const char* MQTT_PUB_TOPIC;
extern const char* CLIENT_ID;
extern PubSubClient client;

/*---------------------------------- Function Prototypes ------------------------------------------*/
float readCurrentData();
float readVoltageData();
float computePower(float current, float voltage);
bool configWiFiStation(const char * ssid, const char * passkey);
bool wiFiIsConnected();
uint32_t getUniqueID();
float stopTimer(unsigned long startTime);
void callback(char* topic, byte* payload, unsigned int length);
bool readyToSend(unsigned long prev);
bool sendData(uint8_t state, float voltage, float current, float time);

#endif // HEADER_H