import numpy as np
import ast
from datetime import datetime
import data_manager

# Sensor parameters mapping
SENSOR_PARAM_MAP = {
    1: "800 Hz - 4 samples",
    2: "1000 Hz - 8 samples",
    3: "1600 Hz - 8 samples",
    4: "1600 Hz - 16 samples",
}

def parse_message(message):
    """Parse the incoming message and process it based on sensor parameters and detected signal type."""
    try:
        # Split the message into parts
        parts = message.split(';')

        # Validate that the message has at least three parts (sensorParameters, timestamp, measureTime)
        if len(parts) < 3:
            raise ValueError("Message does not have enough parts")

        # Extract and process message components
        sensor_param_value = int(parts[0])  # Convert sensor parameter to integer
        timestamp = parts[1]
        measure_time = parts[2]

        # Map the sensor parameter value to its string representation
        sensor_parameters = SENSOR_PARAM_MAP.get(sensor_param_value, "Unknown")
        if sensor_parameters == "Unknown":
            raise ValueError(f"Invalid sensor parameter value: {sensor_param_value}")

        # Detect the number of arrays in the message (1 = IR Only, 2 = RED + IR)
        if len(parts) == 4:  # IR Only
            ir_measure_str = parts[3]
            red_measure = []  # No red signal in this mode
            ir_measure = ast.literal_eval(ir_measure_str)
            measure_type = "IR Only"
        elif len(parts) == 5:  # RED + IR
            red_measure_str = parts[3]
            ir_measure_str = parts[4]
            red_measure = ast.literal_eval(red_measure_str)
            ir_measure = ast.literal_eval(ir_measure_str)
            measure_type = "Red + IR"
        else:
            raise ValueError("Unexpected number of parts in the message")

        # Convert measurements to numpy arrays and adjust polarity
        red_measure = np.array(red_measure) * -1 if red_measure else np.array([])
        ir_measure = np.array(ir_measure) * -1 if ir_measure else np.array([])

        # Format timestamp
        dt = datetime.fromtimestamp(int(timestamp))
        formatted_datetime = dt.strftime("%d/%m/%Y %H:%M:%S")
        measure_time = int(measure_time) / 1000
        measure_frequency = len(red_measure or ir_measure) / measure_time

        # Call analysis functions with the parsed data
        data_manager.append_new_measure(
            measure_type, sensor_parameters, formatted_datetime, measure_time, measure_frequency, red_measure, ir_measure
        )

    except Exception as e:
        print(f"Failed to parse message: {e}")
