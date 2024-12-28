import pandas as pd
import numpy as np
from scipy.signal import cheby2, filtfilt

data_array = []  # Global data array to store incoming messages
received_data = []  # Global data array to store MQTT received messages

def chebyshev_filter(fs, lowcut=0.01, highcut=15.0):
    """Design a Chebyshev-II bandpass filter."""
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    return cheby2(4, 40, [low, high], btype='bandpass')

def apply_chebyshev_filter(red_signal, ir_signal, fs):
    """Apply the Chebyshev II bandpass filter to the red and IR signals."""
    b, a = chebyshev_filter(fs)
    filtered_red = filtfilt(b, a, red_signal)
    filtered_ir = filtfilt(b, a, ir_signal)
    return filtered_red, filtered_ir