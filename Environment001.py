'''
Environment001

This code simulated the natural drift of temperature in a controlled environment,such as a mushroom 
growing chamber, towards ambient conditions. it also adds random sensor noise to mimic rea-world sensor 
inaccuracies.

The user can choose to run the simulation for a set number of ticks or in real time with a specified
interval.

'''

# ============================================================================================================================================
# IMPORT LIBRARIES
# ============================================================================================================================================

import random
import csv
import time

# ============================================================================================================================================
# INITIAL CONDITIONS
# ambient_temp - the natural temperature of the environment outside the chamber.
# ambient_humidity - the natural humidity of the environment outside the chamber.
# starting_temp - the initial temperature inside the chamber at the start of the simulation.
# starting_humidity - the initial humidity inside the chamber at the start of the simulation.
# current_temp - the current temperature inside the chamber, which will drift towards ambient_temp.
# current_humidity - the current humidity inside the chamber, which will drift towards ambient_humidity.
# thermal_decay_rate - the rate at which the temperature drifts towards ambient_temp.
# moisture_decay_rate - the rate at which the humidity drifts towards ambient_humidity.
# temp_noise - the standard deviation of the random noise added to temperature readings.
# humidity_noise - the standard deviation of the random noise added to humidity readings.
# =============================================================================================================================================

ambient_temp = 32.0
ambient_humidity = 70.0

starting_temp = 22.0
starting_humidity = 90.0

current_temp = starting_temp
current_humidity = starting_humidity

thermal_decay_rate = 0.002
moisture_decay_rate = 0.003

temp_noise = 0.1
humidity_noise = 0.2

""" total_ticks = 600 """

output_file = "chamber_log_environment.csv"

""" run_in_real_time = True """

# ============================================================================================================================================
# Main drift function to simulate the environment's natural tendency
# to return to ambient conditions.
# ============================================================================================================================================


def drift(current_value, ambient_value, rate):
    gap = ambient_value - current_value
    change = gap * rate
    new_value = current_value + change
    return new_value

# ============================================================================================================================================
# Function for adding sensor noise to the readings,
# simulating real-world sensor inaccuracies.
# ============================================================================================================================================


def add_sensor_noise(value, noise_level):
    noise = random.gauss(0, noise_level)
    noise_readings = value + noise
    return noise_readings


''' sensor_temp = add_sensor_noise(current_temp, temp_noise) '''
''' sensor_humidity = add_sensor_noise(current_humidity, humidity_noise) '''

# ============================================================================================================================================
# Clamp function to ensure sensor readings stay within realistic bounds (e.g., 0-100% for humidity).
# ============================================================================================================================================


def clamp(value, min_value, max_value):
    if value < min_value:
        return min_value
    elif value > max_value:
        return max_value
    else:
        return value

# ============================================================================================================================================
# Choose TRUE to calculate for a set number of ticks,
# or FALSE to run in real time with a specified interval.
#
# OUTPUT for New value after drift and noise, either in real time,
# or for a set number of ticks.
# ============================================================================================================================================


run_in_real_time = (input("Run in real time? (True/False): ")).lower()
if run_in_real_time == "true":
    time_ = float(input("Enter interval to run (in seconds): "))
    while True:
        current_temp = drift(current_temp, ambient_temp, thermal_decay_rate)
        sensor_temp = add_sensor_noise(current_temp, temp_noise)
        temp_clamped = clamp(sensor_temp, 0, 100)
        print(f"New value after drift and noise: {temp_clamped:.2f}")
        time.sleep(time_)
elif run_in_real_time == "false":
    total_ticks = int(input("Enter the number of ticks: "))
    for tick in range(total_ticks):
        current_temp = drift(current_temp, ambient_temp, thermal_decay_rate)
        sensor_temp = add_sensor_noise(current_temp, temp_noise)
        temp_clamped = clamp(sensor_temp, 0, 100)
        print(f"New value after drift and noise: {temp_clamped:.2f}")
