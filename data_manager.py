import numpy as np
import data_logger

def append_new_measure(measure_type, sensor_parameters, formatted_datetime, measureTime, measureFrequency, red_measure, ir_measure):
    """Create a fresh dictionary for each new measure and send it to the data_logger function."""   
    # Initialize a clear dictionary
    sensor_data = {}

    # Prepare the new measure dictionary
    new_measure = {
        "measureType": measure_type,                  # Measure type: IR or Red + IR
        "timestamp": formatted_datetime,              # Store the timestamp of the measurement
        "measureTime": measureTime,                   # Duration of the measurement
        "measureFrequency": measureFrequency,         # Frequency of the measurements
        "IrSignal": ",".join(map(str, ir_measure)),   # IR Measure as a string (to be stored as a single line)
        "RedSignal": ",".join(map(str, red_measure))  # Red Measure as a string (to be stored as a single line)
    }
    
    # Create a fresh dictionary for the sensor data with only this measure
    sensor_data = {
        sensor_parameters: {
            "measures": [new_measure],  # Store the individual measure as a list
        }
    }

    # Save the dictionary in the local file using data_logger
    data_logger.log_measure(sensor_data)

def convert_signals_to_lists(selected_measure):
    """Convert the signal strings to lists of floats for processing."""
    # Create a copy of the selected_measure to maintain the original structure
    updated_measure = selected_measure.copy()

    # Convert signal strings (if present) to lists of integers
    if "IrSignal" in updated_measure:
        updated_measure["IrSignal"] = list(map(int, updated_measure["IrSignal"].split(",")))
    else:
        updated_measure["IrSignal"] = []  # Default to an empty list if not present

    if "RedSignal" in updated_measure:
        if updated_measure["RedSignal"] == "":  # Check if the string is empty
            updated_measure["RedSignal"] = []   # Set to empty list if it's an empty string
        else:
            updated_measure["RedSignal"] = list(map(int, updated_measure["RedSignal"].split(",")))  # Process normally
    else:
        updated_measure["RedSignal"] = []  # Default to an empty list if not present


    # Return the updated measure with parsed signals
    return updated_measure
