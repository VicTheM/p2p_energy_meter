#include "relayControl.h"

// Basic relay functions (active-low)
void relayOn(uint8_t pin) {
    digitalWrite(pin, LOW);  // Active low
}

void relayOff(uint8_t pin) {
    digitalWrite(pin, HIGH); // Active low
}

// Contactor control logic
// Contactor ON: B off, pulse A
void contactorOn(uint8_t pinA, uint8_t pinB) {
    relayOff(pinB);           // Ensure B is OFF
    relayOn(pinA);            // Pulse A
    delay(500);               // Pulse width
    relayOff(pinA);           // Release A
}

// Contactor OFF: A off, pulse B
void contactorOff(uint8_t pinA, uint8_t pinB) {
    relayOff(pinA);           // Ensure A is OFF
    relayOn(pinB);            // Pulse B
    delay(500);               // Pulse width
    relayOff(pinB);           // Release B
}
