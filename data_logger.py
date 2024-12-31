import os
import json
import streamlit as st
from configs import SENSOR_PARAMETERS, MEASURE_LOGGER, SQI_MEDIAN_LOGGER, UNDEFINED_PARAMS

def log_measure(new_data):
    """Append new data to the appropriate JSON file based on the sensor parameter."""
    try:
        for sensor_param, data in new_data.items():
            # Get the file path for the given sensor parameter
            file_path = SENSOR_PARAMETERS.get(sensor_param, UNDEFINED_PARAMS)

            # Load the existing data from the JSON file (if it exists)
            try:
                with open(file_path, 'r') as file:
                    sensor_data = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                # If the file doesn't exist or is empty, initialize an empty dictionary
                print("File not found. Creating new file.")
                sensor_data = {}

            # Add each new measure as a uniquely indexed key
            for i, measure in enumerate(data["measures"], start=len(sensor_data) + 1):
                measure_key = f"measure_{i}"
                sensor_data[measure_key] = measure

            # Save the updated sensor data to the JSON file
            with open(file_path, 'w') as file:
                json.dump(sensor_data, file, indent=4)
            print(f"New measure successfully saved to {file_path}.")         
    
    except Exception as e:
        print(f"Failed to save measure: {e}")

def log_measures(new_data):
    """Append new data to the existing JSON file."""
    try:
        # Load the existing data from the JSON file (if it exists)
        try:
            with open(MEASURE_LOGGER, 'r') as file:
                sensor_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            # If the file doesn't exist or is empty, initialize an empty dictionary
            sensor_data = {}

        # Merge the new data into the existing sensor data
        for sensor_param, data in new_data.items():
            if sensor_param not in sensor_data:
                sensor_data[sensor_param] = {}
            
            # Add each new measure as a uniquely indexed key
            for i, measure in enumerate(data["measures"], start=len(sensor_data[sensor_param]) + 1):
                measure_key = f"measure_{i}"
                sensor_data[sensor_param][measure_key] = measure

        # Save the updated sensor data to the JSON file
        with open(MEASURE_LOGGER, 'w') as file:
            json.dump(sensor_data, file, indent=4)
        print(f"New measure successfully saved to {MEASURE_LOGGER}.")
    
    except Exception as e:
        print(f"Failed to save dictionary: {e}")

def load_measures(file_path):
    """Load measures from the JSON file for the selected parameter."""
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    else:
        return {}