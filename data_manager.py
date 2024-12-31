import numpy as np
import statistics
import data_logger
   
def append_new_measure(sensor_param, formatted_datetime, measureTime, measureFrequency, signals, sqi):
    """Create a fresh dictionary for each new measure and send it to the data_logger function."""   
    # Initialize a clear dictionary
    sensor_data = {}

    # Convert NumPy arrays to strings for JSON compatibility (each array will be stored in a single line)
    signals = {key: ",".join(map(str, value)) if isinstance(value, (np.ndarray, list)) else value for key, value in signals.items()}

    # Prepare the new measure dictionary
    new_measure = {
        "timestamp": formatted_datetime,        # Store the timestamp of the measurement
        "measureTime": measureTime,             # Duration of the measurement
        "measureFrequency": measureFrequency,   # Frequency of the measurements
        "signals": signals,                     # Contains raw and filtered signal data
        "sqi": sqi                              # Signal quality indices
    }
    
    # Create a fresh dictionary for the sensor data with only this measure
    sensor_data = {
        sensor_param: {
            "measures": [new_measure],  # Store the individual measure as a list
        }
    }

    # Save the dictionary in the local file using data_logger
    data_logger.log_measure(sensor_data)

def calculate_sqi_median(data, sensor_param):
    """Calculate the median of the SQI values for a given sensor.
    
    Args:
        data (dict): The dictionary containing all sensor data.
        sensor_param (str): The specific sensor parameter to calculate the median for.
    
    Returns:
        dict: A dictionary containing the median SQI values for the specified sensor.
    """
    # Get the list of all SQI dictionaries for the given sensor
    sqi_values = [measure["sqi"] for measure in data.get(sensor_param, {}).get("measures", [])]
    
    # If there are no measures for this sensor, return an empty dictionary
    if not sqi_values:
        return {}

    # Calculate the median for each SQI value
    median_sqi = {
        key: statistics.median([sqi[key] for sqi in sqi_values if key in sqi])
        for key in sqi_values[0].keys()
    }

    return median_sqi

def convert_signals_to_lists(selected_measure):
    # Create a copy of the selected_measure to maintain the original structure
    updated_measure = selected_measure.copy()
    
    # Convert the signal strings to lists of floats in the signals part
    signals = updated_measure.get("signals", {})
    
    # Define the list of expected signal keys
    signal_keys = [
        "redMeasure", 
        "irMeasure", 
        "redFilteredMA", 
        "irFilteredMA", 
        "redFilteredCheby", 
        "irFilteredCheby"
    ]
    
    # Parse each signal if it exists in the measure
    for key in signal_keys:
        if key in signals:  # Only process if the signal exists
            signals[key] = list(map(float, signals[key].split(',')))
        else:
            signals[key] = []  # If not available, return an empty list
    
    # Return the updated measure with parsed signals
    return updated_measure

"""
def calculate_sqi_median(sensor_param):    
    # Get the list of all SQI dictionaries for the given sensor
    sqi_values = [measure["sqi"] for measure in sensor_data.get(sensor_param, {}).get("measures", [])]
    
    # If there are no measures for this sensor, return an empty dictionary
    if not sqi_values:
        return {}

    # Calculate the median for each SQI value (skewness, kurtosis, etc.)
    median_sqi = {
        "red_ori_skew": statistics.median([sqi["red_ori_skew"] for sqi in sqi_values]),
        "ir_ori_skew": statistics.median([sqi["ir_ori_skew"] for sqi in sqi_values]),
        "red_ori_kurt": statistics.median([sqi["red_ori_kurt"] for sqi in sqi_values]),
        "ir_ori_kurt": statistics.median([sqi["ir_ori_kurt"] for sqi in sqi_values]),
        "red_movavg_skew": statistics.median([sqi["red_movavg_skew"] for sqi in sqi_values]),
        "ir_movavg_skew": statistics.median([sqi["ir_movavg_skew"] for sqi in sqi_values]),
        "red_movavg_kurt": statistics.median([sqi["red_movavg_kurt"] for sqi in sqi_values]),
        "ir_movavg_kurt": statistics.median([sqi["ir_movavg_kurt"] for sqi in sqi_values]),
        "red_cheby_skew": statistics.median([sqi["red_cheby_skew"] for sqi in sqi_values]),
        "ir_cheby_skew": statistics.median([sqi["ir_cheby_skew"] for sqi in sqi_values]),
        "red_cheby_kurt": statistics.median([sqi["red_cheby_kurt"] for sqi in sqi_values]),
        "ir_cheby_kurt": statistics.median([sqi["ir_cheby_kurt"] for sqi in sqi_values])
    }
    
    return median_sqi
"""