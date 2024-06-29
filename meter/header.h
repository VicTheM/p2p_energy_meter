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

// Global variables
String MQTT_BROKER = "test.mosquitto.org";
String MQTT_PORT = "1883";
String MQTT_SUB_TOPIC = "commands/1/2232332606";    // of the form "commands/<node>/<deviceID>"
String MQTT_PUB_TOPIC = "data/1/2232332606";        // of the form "data/<node>/<deviceID>"

// Constants
const int LOAD = 18;            // Pin to control load relay
const int SUPPLY = 19;          // Pin to control supply relay
const int VOLTAGE = 34;         // Pin to read voltage
const int CURRENT = 35;         // Pin to read current



// Function prototypes
float readCurrentData();
float readVoltageData();
float computePower(float current, float voltage);

bool configWiFiStation(String ssid, String passkey);
bool wiFiIsConnected();

uint32_t getUniqueID();
float stopTimer(unsigned long startTime);



#endif // HEADER_H