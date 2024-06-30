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






/*------------------------------------ Place holders ----------------------------------------*/
const char* WIFI_SSID = "Electrify";
const char* WIFI_PASSWORD = "Victory111";

/*------------------------------------ GPIO Pins ---------------------------------------------*/
const int LOAD = 18;                                             // Pin to control load relay
const int SUPPLY = 19;                                           // Pin to control supply relay
const int VOLTAGE = 34;                                          // Pin to read voltage
const int CURRENT = 35;                                          // Pin to read current

WiFiClient espClient;
PubSubClient client(espClient);



void setup()
{
  Serial.begin(115200);

  // Set Pin Modes
  pinMode(LOAD, OUTPUT);
  pinMode(SUPPLY, OUTPUT);
  pinMode(VOLTAGE, INPUT);
  pinMode(CURRENT, INPUT);

  // Initializations
  digitalWrite(LOAD, LOW);
  digitalWrite(SUPPLY, LOW);

  // Connext to the provided wifi
  configWiFiStation(WIFI_SSID, WIFI_PASSWORD);
  if (wiFiIsConnected())
  {
    client.setServer(MQTT_BROKER, MQTT_PORT);
    client.setCallback(callback);
  }
  else
  {
    while (!wiFiIsConnected())
    {
      configWiFiStation(WIFI_SSID, WIFI_PASSWORD);
      client.setServer(MQTT_BROKER, MQTT_PORT);
      client.setCallback(callback);
    }
  }

  // Connect and subscribe to the MQTT broker
  while (!client.connected())
  {
    Serial.print("Attempting MQTT connection...");
    if (client.connect(CLIENT_ID))
    {
      Serial.println("connected to broker successfully");
      client.subscribe(MQTT_SUB_TOPIC);
      Serial.print("SUBSCRIBED TO TOPIC: ");
      Serial.println(MQTT_SUB_TOPIC);
    }
    else
    {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" trying again in 5 seconds");
      delay(5000);
    }
  }
}


unsigned long start;
void loop()
{
  if (wiFiIsConnected())
  {
    // The main program logic starts here
    if (acknowledge)
    {
      acknowledge = false;
      sendData(client, currentState, readVoltageData(), readCurrentData(), stopTimer(millis()));
    }

    if (currentState == 0)
    {
      // Disconnect
      digitalWrite(LOAD, LOW);
      digitalWrite(SUPPLY, LOW);
      Serial.print("Disconnected ");
      change = false;
      while (!change)
      {
        Serial.print(".");
        client.loop();
        delay(2000);
      }
    }

    if (currentState == 1)
    {
      // Send
      digitalWrite(LOAD, LOW);
      digitalWrite(SUPPLY, HIGH);
      Serial.println("Sending");
      change = false;
      while (!change)
      {
        start = millis();
        delay(2000);
        sendData(client, currentState, readVoltageData(), readCurrentData(), stopTimer(start));
        Serial.println("calling loop");
        client.loop();
      }
    }

    if (currentState == 2)
    {
      // Receive
      digitalWrite(SUPPLY, LOW);
      digitalWrite(LOAD, HIGH);
      Serial.print("Receiving");
      change = false;
      while (!change)
      {
        start = millis();
        delay(2000);
        sendData(client, currentState, readVoltageData(), readCurrentData(), stopTimer(start));
        Serial.println("calling loop");
        client.loop();
      }

      // No change
    }

    client.loop();
  }
  else
  {
    configWiFiStation(WIFI_SSID, WIFI_PASSWORD);
  }

}







/*--------------------------------------- Function Definitions ----------------------------------------------*/
#ifndef OPERATIONS_H
#define OPERATIONS_H

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

    return (random(0, 100));
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
bool sendData(PubSubClient messenger, uint8_t state, float voltage, float current, float time)
{
  // Esthablish a connection with the broker
  if (!messenger.connected()) {
    while (!messenger.connected()) {
      Serial.print("Attempting MQTT connection...");
      if (messenger.connect("House A"))
      {
        Serial.println("connected");
        messenger.subscribe(MQTT_SUB_TOPIC);
      } else {
        Serial.print("failed, rc=");
        Serial.print(messenger.state());
        Serial.println(" try again in 5 seconds");
        delay(5000);
      }
    }
  }

  JsonDocument doc;

  doc["s"] = state;
  doc["v"] = voltage;
  doc["c"] = current;
  // doc["t"] = time;

  char payload[1024];
  serializeJson(doc, payload);
  doc.clear();

  if (messenger.publish(MQTT_PUB_TOPIC, payload))
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




/**
 * Connects the microcontroller to a wifi network.
 * In a failed attempt, it tries 20 times, each time
 * using 0.65 seeconds
 */
bool configWiFiStation(const char * ssid, const char * passkey)
{
  Serial.println("******************************************************");
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, passkey);

  while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  return (true);
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