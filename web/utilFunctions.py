"""
ALL UTILITY FUNCTIONS USED IN THE WEB APPLICATION
"""

def calculate_energy(data):
  """
  Calculates the energy consumed from either a list single tuple or a list of multiple tuples containing voltage, current, and duration data.

  Args:
      data: Either a single array representing a data point or a list of arrays, where each array contains:
          - Index 2: Voltage in volts
          - Index 3: Current in milliamperes (mA)
          - Index 4: Duration in seconds

  Returns:
      The total energy consumed in joules.
  """

  if len(data) > 1:
    # If a list of arrays is provided, calculate energy for each entry
    total_energy = 0
    for entry in data:
      voltage = entry[2]
      current = entry[3] / 1000  # Convert mA to A
      duration = entry[4]
      energy = voltage * current * duration
      total_energy += energy 
    return total_energy
  else:
    # If a single array is provided, calculate energy directly
    data = data[0]
    voltage = data[2]
    current = data[3] / 1000  # Convert mA to A
    duration = data[4]

    return round(voltage * current * duration, 2)