import pandas as pd
import numpy as np
import ast
from datetime import datetime, timedelta
import data_analysis
import data_manager

def parse_message(message, sensor_param):
    """Parse the incoming message and store it in the dictionary based on sensor parameters."""
    global sensor_data
    try:
        # Message parse and preprocess
        timestamp, measureTime, red_measure_str, ir_measure_str = message.split(';')
        red_measure = ast.literal_eval(red_measure_str)
        ir_measure = ast.literal_eval(ir_measure_str)
        redMeasure = np.array(red_measure) * -1
        irMeasure = np.array(ir_measure) * -1

        dt = datetime.fromtimestamp(int(timestamp))
        formatted_datetime = dt.strftime("%d/%m/%Y %H:%M:%S")
        measureTime = int(measureTime) / 1000

        # Call data manager function to handle the dictionary 
        data_manager.append_new_measure(sensor_param, formatted_datetime, measureTime, red_measure, ir_measure)

        # Call analysis functions here with the parsed data
        data_analysis.analyze_data(formatted_datetime, measureTime, redMeasure, irMeasure)

        # Calling plot functions to plot data
        plots.plot_raw_sensor_data()
    
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