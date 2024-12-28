# Global dictionary to store sensor data
sensor_data = {}

def append_new_measure(sensor_param, formatted_datetime, measureTime, red_measure, ir_measure):
    """Append a new measure to the global sensor data dictionary."""
    # Prepare the data to be added
    parsed_message_data = {
        "formatted_datetime": formatted_datetime,
        "measureTime": measureTime,
        "red_measure": red_measure,
        "ir_measure": ir_measure
    }

    # Check if the sensor_param already exists in the dictionary, if not, initialize it
    if sensor_param not in sensor_data:
        sensor_data[sensor_param] = []

    # Append the parsed data to the sensor's list
    sensor_data[sensor_param].append(parsed_message_data)
    print(f"Data stored under sensor parameter: {sensor_param}")