import os
import json
from configs import MEASURE_LOGGER

def log_measure(new_data):
    """
    Append new data to a single JSON file (MEASURE_LOGGER).
    Data is grouped by sensor parameters, with each measure numbered sequentially within its group.
    """
    try:
        # Load the existing data from the JSON file (if it exists)
        try:
            with open(MEASURE_LOGGER, 'r') as file:
                sensor_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            # If the file doesn't exist or is empty, initialize an empty dictionary
            print(f"{MEASURE_LOGGER} not found or empty. Initializing a new file.")
            sensor_data = {}

        # Process the new data
        for sensor_param, data in new_data.items():
            # If the sensor parameter key doesn't exist, create it
            if sensor_param not in sensor_data:
                sensor_data[sensor_param] = {}

            # Get the existing measure count for the sensor parameter
            existing_count = len(sensor_data[sensor_param])

            # Add each new measure with a sequential key
            for measure in data["measures"]:
                measure_key = f"measure_{existing_count + 1}"
                sensor_data[sensor_param][measure_key] = measure
                existing_count += 1  # Increment the count for the next measure

        # Save the updated data back to the JSON file
        with open(MEASURE_LOGGER, 'w') as file:
            json.dump(sensor_data, file, indent=4)

        print(f"New measures successfully saved to {MEASURE_LOGGER}.")
    except Exception as e:
        print(f"Failed to save measure: {e}")

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