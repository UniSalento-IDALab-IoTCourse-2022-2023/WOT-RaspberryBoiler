#!/usr/bin/python3

import random
import time

# performance data
def generate_open_performance_data():
  # Generate random performance data
  performance_data = random.randint(0, 65535)
  print("performance_data: " + str(performance_data))
  
  # Build the OpenTherm message for Performance data
  message = (0b10000000000000000000000000000000 |  # Start bit (always 1)
              (0b000000 << 24) |                   # Command ID (0b000000 for Performance data)
              (0x7B << 16) |                       # Data ID (0x7B for Performance data)
              (performance_data & 0xFFFF))         # Data value
  
  return message

def extract_open_performance_data(data):
  # Extract the data ID from the value
  data_id = (data >> 16) & 0xFF

  # Extract the data value from the value
  data_value = data & 0xFFFF

  # Check if the data ID is for performance data
  if data_id == 0x7B:
    # The performance data is a 16-bit unsigned integer value
    performance_data = data_value
    return performance_data
  else:
    print("Not a performance data")



# Maintenance data
def generate_open_maintenance_data():
  # Generate random Maintenance data
  maintenance_data = random.randint(0, 65535)
  print("maintenance_data: " + str(maintenance_data))
  
  # Build the OpenTherm message for Maintenance data
  message = (0b10000000000000000000000000000000 |  # Start bit (always 1)
              (0b000000 << 24) |                   # Command ID (0b000000 for Maintenance data)
              (0x7D << 16) |                       # Data ID (0x7D for Maintenance data)
              (maintenance_data & 0xFFFF))         # Data value
  
  return message

def extract_open_maintenance_data(data):
  # Extract the data ID from the value
  data_id = (data >> 16) & 0xFF

  # Extract the data value from the value
  data_value = data & 0xFFFF

  # Check if the data ID is for Maintenance data
  if data_id == 0x7D:
    # The Maintenance data is a 16-bit unsigned integer value
    maintenance_data = data_value
    return maintenance_data
  else:
    print("Not a Maintenance data")



# water usage data
def generate_open_water_data():
  # Generate random water usage data
  water_usage = random.randint(0, 65535)
  print("water_usage: " + str(water_usage))
  
  # Build the OpenTherm message for Water Flow data
  message = (0b10000000000000000000000000000000 |  # Start bit (always 1)
              (0b000000 << 24) |                   # Command ID (0b000000 for Water Flow data)
              (0x5C << 16) |                       # Data ID (0x5C for Water Flow data)
              (water_usage & 0xFFFF))              # Data value
  
  return message

def extract_open_water_data(data):
  # Extract the data ID from the value
  data_id = (data >> 16) & 0xFF

  # Extract the data value from the value
  data_value = data & 0xFFFF

  # Check if the data ID is for water usage data
  if data_id == 0x5C:
    # The water usage data is a 16-bit unsigned integer value
    water_usage = data_value
    return water_usage
  else:
    print("Not a water usage data")



# temperature data
def generate_open_temperature_data():
  # Generate random temperature data
  temperature_data = round(random.uniform(20.0, 25.0), 2)
  print("temperature_data: " + str(temperature_data))
  data_value = int(temperature_data * 256)
  
  # Build the OpenTherm message for Room Setpoint data
  message = (0b10000000000000000000000000000000 |  # Start bit (always 1)
              (0b000000 << 24) |                   # Command ID (0b000000 for Room Setpoint data)
              (0x28 << 16) |                       # Data ID (0x28 for Room Setpoint data)
              (data_value & 0xFFFF))               # Data value
  
  return message

def extract_open_temperature_data(data):
  # Extract the data ID from the value
  data_id = (data >> 16) & 0xFF

  # Extract the data value from the value
  data_value = data & 0xFFFF

  # Check if the data ID is for temperature data
  if data_id == 0x28:
    # Convert the data value to a temperature in degrees Celsius
    temperature = data_value / 256.0
    return temperature
  else:
    print("Not a temperature data")



# energy consumption data
def generate_open_energy_data():
  # Generate random energy consumption data
  energy_data = random.randint(0, 65535)
  print("energy_data: " + str(energy_data))
  
  # Build the OpenTherm message for Energy Counter data
  message = (0b10000000000000000000000000000000 |  # Start bit (always 1)
              (0b000000 << 24) |                   # Command ID (0b000000 for Energy Counter data)
              (0x7C << 16) |                       # Data ID (0x7C for Energy Counter data)
              (energy_data & 0xFFFF))                   # Data value
  
  return message

def extract_open_energy_data(data):
  # Extract the data ID from the value
  data_id = (data >> 16) & 0xFF

  # Extract the data value from the value
  data_value = data & 0xFFFF

  # Check if the data ID is for Energy consumption data
  if data_id == 0x7C:
    # The Energy consumption data is a 16-bit unsigned integer value
    energy_consumption = data_value
    return energy_consumption
  else:
    print("Not an Energy consumption data")


while True:
  # generate datas
  temperature_data = generate_open_temperature_data()
  print(f"Generated OpenTherm temperature data: {temperature_data}")
  print(f"Temperature: {extract_open_temperature_data(temperature_data)} °C")

  energy_data = generate_open_energy_data()
  print(f"Generated OpenTherm energy consumption data: {energy_data}")
  print(f"Energy consumption: {extract_open_energy_data(energy_data)} units")

  water_usage = generate_open_water_data()
  print(f"Generated OpenTherm water usage data: {water_usage}")
  print(f"Water usage: {extract_open_water_data(water_usage)} units")

  maintenance_data = generate_open_maintenance_data()
  print(f"Generated OpenTherm Maintenance data: {maintenance_data}")
  print(f"Maintenance data: {extract_open_maintenance_data(maintenance_data)} units")

  performance_data = generate_open_performance_data()
  print(f"Generated OpenTherm Performance data: {performance_data}")
  print(f"Performance data: {extract_open_performance_data(performance_data)} units")

  # convert Open Therm data in viewable data


  time.sleep(3)
