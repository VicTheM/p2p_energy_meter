#include "header.h"
#include "connections.h"

void setup() {
  Serial.begin(9600);

  // Set Pin Modes
  pinMode(LOAD, OUTPUT);
  pinMode(SUPPLY, OUTPUT);
  pinMode(VOLTAGE, INPUT);
  pinMode(CURRENT, INPUT);


}