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
        delay(10000);
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
        delay(10000);
        sendData(client, currentState, readVoltageData(), readCurrentData(), stopTimer(start));
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
        delay(10000);
        sendData(client, currentState, readVoltageData(), readCurrentData(), stopTimer(start));
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
