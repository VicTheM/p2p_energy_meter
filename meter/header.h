/* 
    The root header file for the firmware code that will be uploaded
    to the esp32
    
    This file contains structures, function prototypes and global'
    Variables
*/

#ifndef HEADER_H
#define HEADER_H

#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <Preferences.h>

/*----------------- Global Variables -----------------------*/
unit8_t currentState  = 0;
bool change = false;
bool acknowledge = false;

/*----------------- Function Prototypes --------------------*/
float readCurrentData();
float readVoltageData();
float computePower(float current, float voltage);
bool configWiFiStation(const char * ssid, const char * passkey);
bool wiFiIsConnected();
uint32_t getUniqueID();
float stopTimer(unsigned long startTime);
void callback(char* topic, byte* payload, unsigned int length);
bool sendData(PubSubClient messenger, uint8_t state, float voltage, float current, String time);



#endif // HEADER_H