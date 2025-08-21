#ifndef RELAY_CONTROL_H
#define RELAY_CONTROL_H

#include <Arduino.h>

// Functions for active-low relay control
void relayOn(uint8_t pin);
void relayOff(uint8_t pin);

// Functions for controlling a latching contactor
void contactorOn(uint8_t pinA, uint8_t pinB);
void contactorOff(uint8_t pinA, uint8_t pinB);

#endif
