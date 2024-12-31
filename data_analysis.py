import numpy as np
import logging
from scipy.signal import cheby2, filtfilt
from scipy.stats import skew, kurtosis
import data_manager

def filter_signals(sensor_param, formatted_datetime, measureTime, measureFrequency, redMeasure, irMeasure):
    """
    Perform filtering and signal quality analysis on the parsed data.

    Parameters:
    - sensor_param (str): Sensor identifier.
    - formatted_datetime (str): Datetime string for the measurement.
    - measureTime (float): Measurement duration in seconds.
    - measureFrequency (float): Sampling frequency in Hz.
    - redMeasure (list): Unfiltered red signal values.
    - irMeasure (list): Unfiltered infrared signal values.

    Returns:
    None. Appends filtered and analyzed data to the data manager if kurtosis conditions are met.
    """
    # Apply Chebyshev and Moving Average filters to the red and IR signals
    try:
        # Apply filters
        redNormalized = normalize_signal(redMeasure)
        irNormalized = normalize_signal(irMeasure)
        red_movavg_filt = moving_average_filter(redNormalized, 7)
        ir_movavg_filt = moving_average_filter(irNormalized, 7)
        red_cheby_filt = normalize_signal(chebyshev_filter(measureFrequency, redNormalized))
        ir_cheby_filt = normalize_signal(chebyshev_filter(measureFrequency, irNormalized))
    except Exception as e:
        logging.error(f"Filtering error: {e}")
        return

    signals = {
        "redMeasure": redNormalized, "irMeasure": irNormalized,
        "redFilteredMA": red_movavg_filt, "irFilteredMA": ir_movavg_filt,
        "redFilteredCheby": red_cheby_filt, "irFilteredCheby": ir_cheby_filt,
    }

    # Calculate SQI
    sqi = calculateSQI(redNormalized, irNormalized, red_movavg_filt, ir_movavg_filt, red_cheby_filt, ir_cheby_filt)

    print(f'Red Signal Kurtosis: {sqi["red_cheby_kurt"]}, IR Signal Kurtosis: {sqi["ir_cheby_kurt"]}')

    # Check kurtosis values
    if ((-2 < sqi["red_cheby_kurt"] < 5) and (-2 < sqi["ir_cheby_kurt"] < 5)):
        # Append to dictionary
        try:
            data_manager.append_new_measure(
                sensor_param, formatted_datetime, measureTime, measureFrequency, signals, sqi
            )
        except Exception as e:
            logging.error(f"Data append error: {e}")

def normalize_signal(signal):
    """
    Normalize the given signal (numpy array) to the range [0, 1].

    Parameters:
    - signal (numpy array): The signal to be normalized.

    Returns:
    - normalized_signal (numpy array): The normalized signal.
    """
    # Convert signal to numpy array if it's not already
    signal = np.array(signal)
    
    # Calculate min and max of the signal
    min_signal = np.min(signal)
    max_signal = np.max(signal)
    
    # Avoid division by zero in case the signal has no variation (constant signal)
    if max_signal - min_signal == 0:
        # If constant signal, return the original signal or handle as desired
        return signal
    
    # Perform min-max normalization
    normalized_signal = (signal - min_signal) / (max_signal - min_signal)
    
    return normalized_signal

def calculateSQI(redMeasure, irMeasure, red_movavg_filt, ir_movavg_filt, red_cheby_filt, ir_cheby_filt):
    """
    Calculate SQI for the given signals and return as a dictionary.
    """
    try:
        sqi = {
            "red_ori_skew": skew(redMeasure), "ir_ori_skew": skew(irMeasure),
            "red_ori_kurt": kurtosis(redMeasure, fisher=True), "ir_ori_kurt": kurtosis(irMeasure, fisher=True),
            "red_movavg_skew": skew(red_movavg_filt), "ir_movavg_skew": skew(ir_movavg_filt),
            "red_movavg_kurt": kurtosis(red_movavg_filt, fisher=True), "ir_movavg_kurt": kurtosis(ir_movavg_filt, fisher=True),
            "red_cheby_skew": skew(red_cheby_filt), "ir_cheby_skew": skew(ir_cheby_filt),
            "red_cheby_kurt": kurtosis(red_cheby_filt, fisher=True), "ir_cheby_kurt": kurtosis(ir_cheby_filt, fisher=True),
        }
    except Exception as e:
        logging.error(f"SQI calculation error: {e}")
        sqi = {}
    
    return sqi

def moving_average_filter(signal, window_size):
    """Apply a simple moving average filter to the signal."""
    return np.convolve(signal, np.ones(window_size) / window_size, mode='valid')

def chebyshev_filter_design(fs, lowcut=0.01, highcut=15.0):
    """Design a Chebyshev-II bandpass filter."""
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    return cheby2(4, 40, [low, high], btype='bandpass')

def chebyshev_filter(fs, signal):
    """Apply the Chebyshev II bandpass filter to the signal."""
    b, a = chebyshev_filter_design(fs)
    return filtfilt(b, a, signal)

def compute_fft(fs, signal):
    """Compute FFT, corresponding frequencies, and convert magnitude to dB."""
    N = len(signal)
    fft_values = np.fft.fft(signal)
    fft_magnitude = np.abs(fft_values[:N // 2])  # Only take the positive frequencies
    fft_magnitude_db = 20 * np.log10(fft_magnitude + 1e-10)  # Add small value to avoid log(0)
    freqs = np.fft.fftfreq(N, d=1 / fs)[:N // 2]  # Corresponding frequencies
    return freqs, fft_magnitude_db