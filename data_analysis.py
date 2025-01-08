import numpy as np
import pandas as pd
import neurokit2 as nk

########## NEUROKIT2 BASED FUNCTIONS ##########
def filter_signal(ppg_signal, sampling_rate):
    """Return an array with the filtered signal."""
    filtered_signal = nk.ppg_clean(ppg_signal, sampling_rate, heart_rate=None, method="elgendi")
    return filtered_signal

def peak_finder(ppg_cleaned, sampling_rate):
    """Return a dictionary with PPG info"""
    ppg_info = nk.ppg_findpeaks(ppg_cleaned, sampling_rate, method='elgendi', show=False)
    return ppg_info

def ppg_heart_beats(ppg_cleaned, peaks, sampling_rate, show=False):
    """
    Return a dict containing DataFrames for all segmented hearbeats.
    """
    ppg_epochs = nk.ppg_segment(ppg_cleaned, peaks, sampling_rate)
    return ppg_epochs

def ppg_sqa(ppg_cleaned, ppg_pw_peaks, sampling_rate):
    """
    Return a vector containing the quality index ranging from 0 to 1 for "templatematch" method,
    or an unbounded value (where 0 indicates high quality) for "disimilarity" method.
    """
    quality = nk.ppg_quality(ppg_cleaned, ppg_pw_peaks, sampling_rate, method='templatematch', approach=None)
    return quality

def ppg_process(ppg, sampling_rate):
    """
    Return for signals: dataframe with PPG_Raw, PPG_Clean, PPG_Rate, PPG_Peaks
    Return for info: dictionary containing the information of peaks and the signals sampling rate 
    """
    signals, info = nk.ppg_process(ppg, sampling_rate)
    return signals, info

def calculate_avg_beat(ir_beats):
    """
    Calculate the average beat from a dictionary of beats.

    Args:
        ir_beats (dict): Dictionary containing individual beats, where keys are beat indices 
                         and values are DataFrames with columns: 'Signal', 'Index', and 'Label'.

    Returns:
        pd.DataFrame: A DataFrame with the average signal and the corresponding time.
    """
    # Extract time indices and signals from each beat
    signals = []
    time_index = None

    for beat_df in ir_beats.values():
        if time_index is None:
            time_index = beat_df.index  # Use the index of the first beat as the reference
        
        # Ensure the signal is valid (handle NaN if present)
        signal = beat_df["Signal"].values
        if np.isnan(signal).any():
            #print("Warning: NaN values found in beat. Replacing NaN with zeros.")
            signal = np.nan_to_num(signal)
        
        signals.append(signal)

    # Stack all signals and compute the mean along the columns (time axis)
    signals_stack = np.vstack(signals)
    average_signal = np.nanmean(signals_stack, axis=0)  # Use nanmean to ignore NaN values

    # Create a DataFrame with the average signal and time
    average_signal_df = pd.DataFrame({
        "Time": time_index,  # Time is the index from the original DataFrame
        "Average Signal": average_signal
    })

    return average_signal_df

########## CUSTOM FUNCTIONS ##########
def fourier_bandpass_filter(signal, fs, low_cutoff=0.1, high_cutoff=10):
    """Apply Fourier-based bandpass filter to the signal while preserving baseline."""
    # Compute the frequency bins
    freqs = np.fft.fftfreq(len(signal), d=1/fs)
    
    # Perform FFT
    fft_signal = np.fft.fft(signal)
    
    # Save the DC component
    dc_component = fft_signal[0]
    
    # Zero out frequencies outside the bandpass range
    fft_signal[(np.abs(freqs) < low_cutoff) | (np.abs(freqs) > high_cutoff)] = 0
    
    # Restore the DC component if low_cutoff > 0
    if low_cutoff > 0:
        fft_signal[0] = dc_component
    
    # Inverse FFT to get the filtered signal
    return np.fft.ifft(fft_signal).real

def normalize_signal(signal, range_min=0, range_max=1):
    """Normalize the input data to a specified range."""
    signal = np.array(signal)  # Ensure input is a numpy array for easier manipulation
    signal_min = np.min(signal)
    signal_max = np.max(signal)

    # Avoid division by zero if all values in data are the same
    if signal_max == signal_min:
        return np.full_like(signal, range_min)  # Fill with the minimum of the range

    # Normalize to [0, 1] and then scale to the desired range
    normalized_data = (signal - signal_min) / (signal_max - signal_min)
    normalized_data = normalized_data * (range_max - range_min) + range_min

    return normalized_data