#ifndef OPERATIONS_H
#define OPERATIONS_H

#include "header.h"

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
computePower(float current, float voltage)
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

#endif // OPERATIONS_H