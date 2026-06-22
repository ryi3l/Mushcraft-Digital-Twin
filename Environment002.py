'''
Environment002

This code simulates the natural drift of temperature, humidity, and CO2 in a controlled environment, 
such as a mushroom growing chamber, towards ambient conditions. It also adds random sensor noise to 
mimic real-world sensor inaccuracies.

The user can choose to run the simulation for a set number of ticks or in real time with a specified 
interval, and insert the desired number of mushrooms inside the chamber.

'''

# ============================================================================================================================================
# IMPORT LIBRARIES
# ============================================================================================================================================

import random
import csv
import time

# ============================================================================================================================================
# INITIAL CONDITIONS
# =============================================================================================================================================

# --- Outside ambient environment (Philippines) ---
# The natural temperature of the environment outside the chamber.
ambient_temp = 32.0
# The natural humidity of the environment outside the chamber.
ambient_humidity = 70.0
# The natural co2 of the environment outside the chamber.
ambient_co2 = 400.0

# --- Starting conditions inside the chamber ---
# The initial temperature inside the chamber at the start of the simulation.
starting_temp = 22.0
# The initial humidity inside the chamber at the start of the simulation.
starting_humidity = 90.0
# The initial co2 inside the chamber at the start of the simulation.
starting_co2 = 400.0

# --- Current conditions inside the chamber ---
# The current temperature inside the chamber, which will drift towards ambient_temp.
current_temp = starting_temp
# The current humidity inside the chamber, which will drift towards ambient_humidity.
current_humidity = starting_humidity
# The current  humidity inside the chamber, which will drift towards ambient_co2.
current_co2 = starting_co2

# --- How fast the chamber's environment drifts toward ambient ---
# The rate at which the temperature drifts towards ambient_temp.
thermal_decay_rate = 0.002
# The rate at which the humidity drifts towards ambient_humidity.
moisture_decay_rate = 0.003
# The rate at which the co2 drifts towards ambient_co2.
co2_decay_rate = 0.003

# --- Sensor noise settings ---
# The standard deviation of the random noise added to temperature readings.
temp_noise = 0.1
# The standard deviation of the random noise added to humidity readings.
humidity_noise = 0.2
# The standard deviation of the random noise added to the co2 readings.
co2_noise = 10.0

output_file = "chamber_log_environment.csv"

# ============================================================================================================================================
# DRIFT FUNCTION (NEWTON'S LAW OF COOLING)
# ============================================================================================================================================


def drift(current_value, ambient_value, rate):
    '''
    Main drift function to simulate the environment's natural tendency to return to ambient conditions.

    The math formula used here:
            gap          = ambient_value - current_value
            new_value    = current_value + rate * gap

    Example:
            current_value = 22.0 (inside the chamber)
            ambient_value = 32.0 (outside)
            rate          = 0.002

            gap       = 32.0 - 22.0 = 10.0
            change    = 0.002 * 10.0 = 0.02
            new_value = 22.0 + 0.02  = 22.02

    '''
    # How far from ambient
    gap = ambient_value - current_value
    # How much change to do
    change = gap * rate
    # Final value after change
    new_value = current_value + change
    # Return value
    return new_value


# ============================================================================================================================================
# SENSOR NOISE FUNCTION
# ============================================================================================================================================
def add_sensor_noise(value, noise_level):
    '''
    This function adds a random noise to the value using random.gauss method
        Example:
            true_value = 22.02
            noise      = random.gauss(0, 0.1)  -> maybe returns -0.07
            reading    = 22.02 + (-0.07)       = 21.95

    '''
    # Generate random number around 0 with a standard deviation of noise_level
    noise = random.gauss(0, noise_level)
    # Final value after adding noise to the value
    noise_readings = value + noise
    # Return value
    return noise_readings


# ============================================================================================================================================
# CLAMP FUNCTION
# ============================================================================================================================================
def clamp(value, min_value, max_value):
    '''

    This function ensure sensor readings stay within realistic bounds 
        Example:
            0-100% for humidity

    '''
    # If value is less than the minimum
    if value < min_value:
        # Return the minimum
        return min_value
    # Else if value is greater than the maximum
    elif value > max_value:
        # Return the maximum
        return max_value
    # Else if it is neither
    else:
        # Return the value
        return value

# ============================================================================================================================================
# CO2 EMISSION FUNCTION
# ============================================================================================================================================


def co2_emission_rate(value):
    '''

    This function dynamically calculates the chamber's CO2 emission rate, 
    driven by the number of mushroom bags currently inside

    Math formula used here (currently):
            emission = mushroom * 100
            new_value = current_co2 + emission

    Example:
            mushroom = 3
            current_co2 = 460ppm

            emission = 3 * 100 = 300
            new_value = 460 + 300 = 760

    '''
    # If there is at least 1 mushroom
    if value > 0:
        # Calculate the new value for the co2
        emission = value * 100
        new_value = current_co2 + emission
    # If there is no mushroom
    else:
        # Set the new_value to starting_co2
        new_value = starting_co2
    # Return new_value
    return new_value

# ============================================================================================================================================
# OUTPUT FUNCTION
# ============================================================================================================================================


def output(current_temp, current_humidity):
    '''

    Calculates the new physical state of the chamber and generates the 
    corresponding sensor readings.

    Execution Pipeline:
    1. Drift ("current"): Calculates the true physical values drifting toward ambient baseline.
    2. Noise ("sensor"): Simulates hardware inaccuracy by adding Gaussian noise to the true values.
    3. Clamp ("clamped"): Restricts the final noisy readings to valid physical boundaries (min/max).

    '''
    # Current temperature and humidity after drift function using the following variables
    current_temp = drift(current_temp, ambient_temp, thermal_decay_rate)
    current_humidity = drift(
        current_humidity, ambient_humidity, moisture_decay_rate
    )
    # Current temperature and humidity value after adding sensor noise
    sensor_temp = add_sensor_noise(current_temp, temp_noise)
    sensor_humidity = add_sensor_noise(current_humidity, humidity_noise)
    # Check if the value is within set threshold for temperature and humidity
    temp_clamped = clamp(sensor_temp, 0, 100)
    humidity_clamped = clamp(sensor_humidity, 0, 100)
    # Return the current_temp, current_humidity, temp_clamped, humidity_clamped
    return current_temp, current_humidity, temp_clamped, humidity_clamped

# ============================================================================================================================================
# Choose TRUE to calculate for a set number of ticks,
# or FALSE to run in real time with a specified interval.
#
# OUTPUT for New value after drift, noise, and clamp either in real time,
# or for a set number of ticks.
# ============================================================================================================================================


# Input how many mushrooms inside the chamber
mushrooms = int(input("Mushrooms: "))
# Current co2 is calculated based on how much mushroom is inside
current_co2 = co2_emission_rate(mushrooms)

# Input True or False (set input in lower case)
run_in_real_time = (input("Run in real time? (True/False): ")).lower()
# If True run in real time
if run_in_real_time == "true":
    # Input the interval in seconds
    time_ = float(input("Enter interval to run (in seconds): "))
    # Loop for real time to continuously run
    while True:
        # Output function execution
        current_temp, current_humidity, temp_clamped, humidity_clamped = output(
            current_temp, current_humidity)
        # Print the the final value for the 3 parameters
        print(
            f"New value after drift and noise: {temp_clamped:.2f}C -- {humidity_clamped:.2f}% CO2: {current_co2:.2f}"
        )
        # Interval for every loop is based on the input time
        time.sleep(time_)
# If false run based on ticks
elif run_in_real_time == "false":
    # The total duration of the simulation loop, measured in ticks.
    total_ticks = int(input("Enter the number of ticks: "))
    # Advance the simulation tick-by-tick, processing environmental drift and sensor noise.
    for tick in range(total_ticks):
        # Output function execution
        current_temp, current_humidity, temp_clamped, humidity_clamped = output(
            current_temp, current_humidity)
        print(
            f"New value after drift and noise: {temp_clamped:.2f}C -- {humidity_clamped:.2f}% CO2: {current_co2:.2f}"
        )

'''
CO2 emission logic for this code is still at 100ppm/mushroom for testing purposes.

CO2 emission per bag = bagWeight/2 for 60 days
                     = answer/60days
                     = answer/24hours
                     = answer/60minutes

'''
