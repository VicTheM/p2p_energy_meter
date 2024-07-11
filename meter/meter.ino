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

const int sends = 27;
const int receives = 17;
const int disconnect = 15; // should be the disconnect pin

void setup()
{
  Serial.begin(115200);

  // Set Pin Modes
  pinMode(disconnect, OUTPUT);
  pinMode(sends, OUTPUT);
  pinMode(receives, OUTPUT);

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
      digitalWrite(sends, LOW);
      digitalWrite(receives, LOW);
      digitalWrite(disconnect, HIGH);
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
      digitalWrite(disconnect, LOW);
      digitalWrite(receives, LOW);
      digitalWrite(sends, HIGH);
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
      digitalWrite(disconnect, LOW);
      digitalWrite(sends, LOW);
      digitalWrite(receives, HIGH);
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
