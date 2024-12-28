# data_analysis.py

import pandas as pd
import numpy as np
import ast
import matplotlib.pyplot as plt
import io
from datetime import datetime, timedelta
from scipy.signal import cheby2, filtfilt

def load_data(file_path):
    """Load CSV data."""
    return pd.read_csv(file_path)

def parse_last_line(file_path):
    """Parse the last line of the CSV file for signal data."""
    with open(file_path, 'r') as file:
        data = file.readlines()

    last_line = data[-1].strip()
    try:
        timestamp, measureTime, red_measure_str, ir_measure_str = last_line.split(';')
        red_measure = ast.literal_eval(red_measure_str)
        ir_measure = ast.literal_eval(ir_measure_str)
    except ValueError as e:
        raise ValueError(f"Error parsing line: {last_line}")

    dt = datetime.fromtimestamp(int(timestamp))
    formatted_datetime = dt.strftime("%d/%m/%Y %H:%M:%S")
    measureTime = int(measureTime) / 1000
    return formatted_datetime, measureTime, np.array(red_measure)*-1, np.array(ir_measure)*-1

def design_bandpass_filter(fs, lowcut=0.5, highcut=8.0):
    """Design a Chebyshev-II bandpass filter."""
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    return cheby2(4, 40, [low, high], btype='bandpass')

def apply_filter(red_signal, ir_signal, fs):
    """Apply the bandpass filter to the red and IR signals."""
    b, a = design_bandpass_filter(fs)
    filtered_red = filtfilt(b, a, red_signal)
    filtered_ir = filtfilt(b, a, ir_signal)
    return filtered_red, filtered_ir

def plot_signals(dt, measure_freq, red_signal, ir_signal, filtered_red, filtered_ir):
    """Plot the original and filtered signals and return the image as a buffer."""
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    # Original signals
    axes[0].plot(red_signal, label='Original Red Signal')
    axes[0].plot(ir_signal, label='Original IR Signal')
    axes[0].plot([], label=f'Measure Frequency: {measure_freq:.2f} Hz', color='white')
    axes[0].set_title(f'Original Signals - {dt}')
    axes[0].set_xlabel('Sample')
    axes[0].set_ylabel('Value')
    axes[0].legend()
    axes[0].grid(True)

    # Filtered signals
    axes[1].plot(filtered_red, label='Filtered Red Signal', linewidth=2)
    axes[1].plot(filtered_ir, label='Filtered IR Signal', linewidth=2)
    axes[1].plot([], label=f'Measure Frequency: {measure_freq:.2f} Hz', color='white')
    axes[1].set_title(f'Filtered Signals - {dt}')
    axes[1].set_xlabel('Sample')
    axes[1].set_ylabel('Value')
    axes[1].legend()
    axes[1].grid(True)

    fig.tight_layout()

    # Save the figure to a buffer (in-memory image)
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)  # Rewind the buffer to the beginning

    # Close the figure to free up memory
    plt.close(fig)

    return buf  # Return the buffer object