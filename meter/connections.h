#ifndef CONNECTIONS_H
#define CONNECTIONS_H
#include "header.h"


bool configWiFiStation(String ssid, String passkey){
    unsigned int WiFiConnectAttempt = 20; // Number of attempts to connect to wifi network
    // WiFi.disconnect(true);
    WiFi.mode(WIFI_STA); // Configures WiFi in Station point

    Serial.print("\n\n\nConnecting WiFi to " + ssid);

    WiFi.begin(ssid, passkey);
    while (((!wiFiIsConnected()) && (WiFiConnectAttempt != 0))){ // Loop to reattempt wifi connection if not connected and connect Attempt not exceeded
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

#endif // CONNECTIONS_H