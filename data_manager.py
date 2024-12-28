# Global dictionary to store sensor data
sensor_data = {}

def append_new_measure(sensor_param, formatted_datetime, measureTime, measureFrequency, signals, sqi):
    """Append a new measure to the global sensor data dictionary."""
    
    # Prepare the data to be added
    new_measure = {
        "timestamp": formatted_datetime,        # Store the timestamp of the measurement
        "measureTime": measureTime,             # Duration of the measurement
        "measureFrequency": measureFrequency,   # Frequency of the measurements
        "signals": signals,                     # Contains raw and filtered signal data
        "sqi": sqi                              # Signal quality indices
    }
    
    # Check if the sensor_param already exists in the dictionary, if not, initialize it
    if sensor_param not in sensor_data:
        sensor_data[sensor_param] = []
    
    # Append the parsed data to the sensor's list
    sensor_data[sensor_param].append(new_measure)
    print(f"Data stored under sensor parameter: {sensor_param}")