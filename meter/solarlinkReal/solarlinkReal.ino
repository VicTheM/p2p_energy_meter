#include <Arduino.h>
#include "header.h"
#include "relayControl.h"

WiFiClient espClient;
PubSubClient client(espClient);

const uint8_t relayA = 25; // Purple; rightmost- Normally open
const uint8_t relayB = 26;
const uint8_t relayA2 = 33;
const uint8_t relayB2 = 32;

unsigned long prev = 0;
const unsigned long interval = 3000; // 1s

void handleDisconnected() {

  Serial.println("Disconnected...");
  contactorOff(relayA, relayB);
  sendData(currentState, 0, 0, 0);
}

void handleSending() {

  Serial.println("Sending...");
  contactorOn(relayA, relayB);
  sendData(currentState, readVoltageData(), readCurrentData(), stopTimer(prev));
}

void handleReceiving() {
  Serial.println("Receiving...");
  sendData(currentState, readVoltageData(), readCurrentData(), stopTimer(prev));
}

void handleHouseOn() {
  Serial.println("Oning house power...");
  contactorOn(relayA2, relayB2);
}

void handleHouseOff() {
  Serial.println("Offing house power...");
  contactorOff(relayA2, relayB2);
}



void handleState() {
  switch (currentState) {
    case 0:
      handleDisconnected();
      break;
    case 1:
      handleSending();
      break;
    case 2:
      handleReceiving();
      break;
  }
}

void handleHouseState() {
  switch (houseState) {
  case 4:
    handleHouseOff();
    break;
  case 5:
    handleHouseOn();
    break;
  }
}

void setup()
{
  Serial.begin(115200);

  pinMode(relayA, OUTPUT);
  pinMode(relayB, OUTPUT);
  pinMode(relayA2, OUTPUT);
  pinMode(relayB2, OUTPUT);

  // Initialize relays OFF (inactive)
  relayOff(relayA);
  relayOff(relayB);
  relayOff(relayA2);
  relayOff(relayB2);

  contactorOn(relayA2, relayB2);

  // Connect to the provided wifi
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

void loop() {
  if (!wiFiIsConnected()) {
    configWiFiStation(WIFI_SSID, WIFI_PASSWORD);
    return;
  }

  client.loop();

  if (acknowledge) {
    acknowledge = false;
    Serial.println("Sending acknowledged data");
    sendData(currentState, readVoltageData(), readCurrentData(), 0);
  }

  // Call state machine
  if (change) {
    change = false;
    handleState();
    handleHouseState();
  }

  if (millis() - prev >= interval) {
    prev = millis();

    switch (currentState) {
      case 0: // Disconnected
        Serial.println("Disconnected...");
        sendData(currentState, 0, 0, 0);
        break;

      case 1: // Sending
        Serial.println("Sending...");
        sendData(currentState, readVoltageData(), readCurrentData(), interval);
        break;

      case 2: // Receiving
        Serial.println("Receiving...");
        sendData(currentState, readVoltageData(), readCurrentData(), interval);
        break;
    }
  }
}

