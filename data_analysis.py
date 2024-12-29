import numpy as np
import logging
from scipy.signal import cheby2, filtfilt
from scipy.stats import skew, kurtosis
import data_manager

def filter_signals(sensor_param, formatted_datetime, measureTime, measureFrequency, redMeasure, irMeasure):
    """
    Perform filtering and signal quality analysis on the parsed data.
    Call the dictionary appender if kurtosis conditions are met.
    """
    # Apply Chebyshev and Moving Average filters to the red and IR signals
    try:
        # Apply filters
        red_movavg_filt = apply_chebyshev_filter(measureFrequency, redMeasure)
        ir_movavg_filt = apply_chebyshev_filter(measureFrequency, irMeasure)
        red_cheby_filt = moving_average_filter(redMeasure, 10)
        ir_cheby_filt = moving_average_filter(irMeasure, 10)
    except Exception as e:
        logging.error(f"Filtering error: {e}")
        return

    signals = {
        "redMeasure": redMeasure, "irMeasure": irMeasure,
        "redFilteredMA": red_movavg_filt, "irFilteredMA": ir_movavg_filt,
        "redFilteredCheby": red_cheby_filt, "irFilteredCheby": ir_cheby_filt,
    }

    # Calculate SQI
    sqi = calculateSQI(redMeasure, irMeasure, red_movavg_filt, ir_movavg_filt, red_cheby_filt, ir_cheby_filt)

    print(f'Red Signal Kurtosis: {sqi["red_cheby_kurt"]}, IR Signal Kurtosis: {sqi["ir_cheby_kurt"]}')

    # Check kurtosis values
    if -2 < sqi["red_cheby_kurt"] < 5 and -2 < sqi["ir_cheby_kurt"] < 5:
        # Append to dictionary
        try:
            data_manager.append_new_measure(
                sensor_param, formatted_datetime, measureTime, measureFrequency, signals, sqi
            )
        except Exception as e:
            logging.error(f"Data append error: {e}")
    
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

def chebyshev_filter(fs, lowcut=0.01, highcut=15.0):
    """Design a Chebyshev-II bandpass filter."""
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    return cheby2(4, 40, [low, high], btype='bandpass')

def apply_chebyshev_filter(fs, signal):
    """Apply the Chebyshev II bandpass filter to the signal."""
    b, a = chebyshev_filter(fs)
    return filtfilt(b, a, signal)
