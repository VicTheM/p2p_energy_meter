/*--------------------------------------------------------------------------------------------
    Entry Point

    This is the main entrance to the program, if you want to debug, start from this file
    The algorithm will be defined soon
    Please note that this file uses some global variables which are decleared in the
    header.h file and defined in the operations.cpp file

----------------------------------------------------------------------------------------------*/


#include "header.h"

WiFiClient espClient;
PubSubClient client(espClient);

void setup()
{
  Serial.begin(115200);

  // Set Pin Modes
  pinMode(LOAD, OUTPUT);
  pinMode(SUPPLY, OUTPUT);
  // pinMode(VOLTAGE, INPUT);
  // pinMode(CURRENT, INPUT);
  pinMode(DISCONNECT, OUTPUT);

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


// The Main Loop
unsigned long start = 0;
unsigned int temp = 0;
unsigned long prev = 0;
void loop()
{
  start = millis();
  if (wiFiIsConnected())
  {
    // The main program logic starts here
    if (acknowledge)
    {
      acknowledge = false;
      Serial.println("Sending acknoledged data");
      sendData(currentState, readVoltageData(), readCurrentData(), 0);
    }

    if (currentState == 0)
    {
      // Disconnect
      digitalWrite(LOAD, LOW);
      digitalWrite(SUPPLY, LOW);
      digitalWrite(DISCONNECT, HIGH);
      Serial.print("Disconnected ");

      prev = millis();
      change = false;
      sendData(currentState, 0, 0, 0);
      while (!change)
      {
        if (readyToSend(prev));
        {
          Serial.print(".");
          prev = millis();
        }
        delay(500);
        client.loop();
      }
    }

    if (currentState == 1)
    {
      // Send
      digitalWrite(DISCONNECT, LOW);
      digitalWrite(LOAD, LOW);
      digitalWrite(SUPPLY, HIGH);
      Serial.println("Sending");

      change = false;
      sendData(currentState, readVoltageData(), readCurrentData(), 0.5);
      prev = millis();
      while (!change)
      {
        if (readyToSend(prev))
        {
          sendData(currentState, readVoltageData(), readCurrentData(), stopTimer(prev));
          prev = millis();
        }
        delay(500);
        client.loop();
      }
    }

    if (currentState == 2)
    {
      // Receive
      digitalWrite(DISCONNECT, LOW);
      digitalWrite(SUPPLY, LOW);
      digitalWrite(LOAD, HIGH);
      Serial.println("Receiving");

      change = false;
      sendData(currentState, readVoltageData(), readCurrentData(), 0.5);
      prev = millis();
      while (!change)
      {
        start = millis();
        if (readyToSend(prev))
        {
          sendData(currentState, readVoltageData(), readCurrentData(), stopTimer(prev));
          prev = millis();
        }
        delay(500);
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
