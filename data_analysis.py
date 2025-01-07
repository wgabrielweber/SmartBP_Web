import numpy as np
import neurokit2 as nk

########## NEUROKIT2 FUNCTIONS ##########
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
    nk.ppg_quality(ppg_cleaned, ppg_pw_peaks, sampling_rate, method='templatematch', approach=None)




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