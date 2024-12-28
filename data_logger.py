import json
from configs import JSON_LOGGER_OW, JSON_LOGGER_AP

def save_to_json(dictionary):
    """Overwrite JSON file with the current dictionary."""
    try:
        with open(JSON_LOGGER_OW, 'w') as file:
            json.dump(dictionary, file, indent=4)
        print(f"Dictionary saved to {JSON_LOGGER_OW}.")
    except Exception as e:
        print(f"Failed to save dictionary: {e}")

def append_to_json(new_entry):
    """Append a new entry to the JSON file."""
    try:
        try:
            with open(JSON_LOGGER_AP, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []

        data.append(new_entry)
        with open(JSON_LOGGER_AP, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"New entry appended to {JSON_LOGGER_AP}.")
    except Exception as e:
        print(f"Failed to append entry: {e}")

def append_new_measure(sensor_param, formatted_datetime, measureTime, red_measure, ir_measure):

    return