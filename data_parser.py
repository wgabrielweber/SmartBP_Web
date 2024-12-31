import numpy as np
import ast
from datetime import datetime
import data_analysis

def parse_message(message, sensor_param):
    """Parse the incoming message and store it in the dictionary based on sensor parameters."""
    global sensor_data
    try:
        # Split the message into parts
        parts = message.split(';')
        
        # Ensure there are at least 4 parts (deviceid, timestamp, measureTime, and the two lists)
        if len(parts) < 4:
            raise ValueError("Message does not have enough parts")

        deviceid = parts[0]
        timestamp = parts[1]
        measureTime = parts[2]
        # Extract the red and IR measurements (should be the last two parts of the message)
        red_measure_str = parts[3]
        ir_measure_str = parts[4] if len(parts) > 4 else '[]'  # Handle the case where only red_measure_str exists
        
        # Message parse and preprocess
        red_measure = ast.literal_eval(red_measure_str)
        ir_measure = ast.literal_eval(ir_measure_str)
        redMeasure = np.array(red_measure) * -1
        irMeasure = np.array(ir_measure) * -1

        dt = datetime.fromtimestamp(int(timestamp))
        formatted_datetime = dt.strftime("%d/%m/%Y %H:%M:%S")
        measureTime = int(measureTime) / 1000
        measureFrequency = len(redMeasure) / measureTime

        # Call analysis functions here with the parsed data
        data_analysis.filter_signals(sensor_param, formatted_datetime, measureTime, measureFrequency, redMeasure, irMeasure)
    
    except Exception as e:
        print(f"Failed to parse message: {e}")


def parse_last_line(file_path):
    """Parse the last line of the CSV file for signal data."""
    with open(file_path, 'r') as file:
        data = file.readlines()

    last_line = data[-1].strip()
    try:
        return parse_message(last_line)
    except ValueError as e:
        raise ValueError(f"Error parsing line: {last_line}")