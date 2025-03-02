import io
import matplotlib.pyplot as plt
import numpy as np
from data_analysis import filter_signal, peak_finder, peak_finder, ppg_heart_beats, ppg_sqa, ppg_process, calculate_avg_beat, normalize_signal

def plot_signals_generic(measure, signals_to_plot, title, labels, colors, alphas=None, linewidths=None, peaks=None, qualities=None):
    """
    Generic function to plot signals with optional peaks and quality indicators.

    Args:
        measure (dict): Dictionary containing measurement metadata.
        signals_to_plot (list of arrays): Signals to plot.
        title (str): Title of the plot.
        labels (list of str): Labels for the signals.
        colors (list of str): Colors for the signals.
        alphas (list of float, optional): Transparency for the signals.
        linewidths (list of float, optional): Line widths for the signals.
        peaks (list of arrays, optional): Peaks to mark on the signals.
        qualities (list of arrays, optional): Quality metrics for the signals.
    """
    # Extract the timestamp and measurement frequency
    dt = measure.get("timestamp", "Unknown Timestamp")
    measure_freq = measure.get("measureFrequency", 0)

    # Define colors for the quality indicators
    quality_colors = ["#32CD32", "#ffa500"]  # Green for one, Orange for another (extend if needed)

    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 5))

    # Plot each signal with its corresponding label, color, and optional style parameters
    for i, signal in enumerate(signals_to_plot):
        alpha = alphas[i] if alphas else 1.0
        linewidth = linewidths[i] if linewidths else 1.0
        ax.plot(signal, label=labels[i], color=colors[i], alpha=alpha, linewidth=linewidth)

        # Plot peaks if provided
        if peaks and peaks[i] is not None:
            ax.plot(peaks[i], signal[peaks[i]], 'o', label=f"{labels[i]} Peaks", color='orange', alpha=0.8)

        # Plot quality indicators if provided
        if qualities and qualities[i] is not None:
            quality_color = quality_colors[i % len(quality_colors)]  # Cycle through colors
            ax.plot(qualities[i], label=f"{labels[i]} Quality", color=quality_color, alpha=0.8)

    # Add the measure frequency as an invisible label for context
    ax.plot([], label=f'Measure Frequency: {measure_freq:.2f} Hz', color='white')

    # Configure plot appearance
    ax.set_title(f'{title} - {dt}')
    ax.set_xlabel('Sample')
    ax.set_ylabel('Value')
    ax.legend(loc='lower left')
    ax.grid(True)

    # Save the figure to a buffer (in-memory image)
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)  # Rewind the buffer to the beginning

    # Close the figure to free up memory
    plt.close(fig)

    return buf  # Return the buffer object

def plotRawSignals(measure):
    """Plot the raw signals from the measure dictionary."""
    red_signal = measure.get("RedSignal", [])
    ir_signal = measure.get("IrSignal", [])

    # Get the measure type
    measure_type = measure.get("measureType", "")

    # Determine which signals to plot based on the measure type
    if measure_type == "IR Only":
        if not ir_signal:
            raise ValueError("Missing necessary IR signal data in the measure.")
        signals = [ir_signal]
        labels = ['Original IR Signal']
        colors = ['#1282b2']
    elif measure_type == "Red + IR":
        if not red_signal or not ir_signal:
            raise ValueError("Missing necessary signal data for Red + IR in the measure.")
        signals = [red_signal, ir_signal]
        labels = ['Original Red Signal', 'Original IR Signal']
        colors = ['#ff2c2c', '#1282b2']
    else:
        raise ValueError(f"Unknown measure type: {measure_type}")
    
    # Pass the Parameters to the plotting function
    return plot_signals_generic(measure, signals, "Original Signals", labels, colors)

def plotCleanedSignals(measure):
    """Plot the cleaned signals from the measure dictionary."""
    red_signal = measure.get("RedSignal", [])
    ir_signal = measure.get("IrSignal", [])
    sampling_rate = measure.get("measureFrequency", 0)

    # Get the measure type
    measure_type = measure.get("measureType", "")

    # Determine which signals to plot based on the measure type
    if measure_type == "IR Only":
        if not ir_signal:
            raise ValueError("Missing necessary IR signal data in the measure.")
        ir_cleaned = filter_signal(ir_signal, sampling_rate)
        signals = [ir_cleaned]
        labels = ['Filtered IR Signal']
        colors = ['#1282b2']
    elif measure_type == "Red + IR":
        if not red_signal or not ir_signal:
            raise ValueError("Missing necessary signal data for Red + IR in the measure.")
        ir_cleaned = filter_signal(ir_signal, sampling_rate)
        red_cleaned = filter_signal(red_signal, sampling_rate)
        signals = [red_cleaned, ir_cleaned]
        labels = ['Filtered Red Signal', 'Filtered IR Signal']
        colors = ['#ff2c2c', '#1282b2']
    else:
        raise ValueError(f"Unknown measure type: {measure_type}")
    
    # Pass the Parameters to the plotting function
    return plot_signals_generic(measure, signals, "Filtered Signals", labels, colors)

def plotSignalsPeaks(measure):
    """Plot the cleaned signals with detected peaks from the measure dictionary."""
    red_signal = measure.get("RedSignal", [])
    ir_signal = measure.get("IrSignal", [])
    sampling_rate = measure.get("measureFrequency", 0)

    # Get the measure type
    measure_type = measure.get("measureType", "")

    # Initialize signals and peaks
    signals, labels, colors, peaks, = [], [], [], []

    # Process signals based on the measure type
    if measure_type == "IR Only":
        if not ir_signal:
            raise ValueError("Missing necessary IR signal data in the measure.")
        ir_cleaned = filter_signal(ir_signal, sampling_rate)
        ir_peaks_dict = peak_finder(ir_cleaned, sampling_rate)
        ir_peaks = ir_peaks_dict["PPG_Peaks"]
        signals.append(ir_cleaned)
        labels.append("Filtered IR Signal")
        colors.append("#1282b2")
        peaks.append(ir_peaks)
    elif measure_type == "Red + IR":
        if not red_signal or not ir_signal:
            raise ValueError("Missing necessary signal data for Red + IR in the measure.")
        ir_cleaned = filter_signal(ir_signal, sampling_rate)
        ir_peaks_dict = peak_finder(ir_cleaned, sampling_rate)
        ir_peaks = ir_peaks_dict["PPG_Peaks"]
        red_cleaned = filter_signal(red_signal, sampling_rate)
        red_peaks_dict = peak_finder(red_cleaned, sampling_rate)
        red_peaks = red_peaks_dict["PPG_Peaks"]

        signals.extend([red_cleaned, ir_cleaned])
        labels.extend(["Filtered Red Signal", "Filtered IR Signal"])
        colors.extend(["#ff2c2c", "#1282b2"])
        peaks.extend([red_peaks, ir_peaks])
    else:
        raise ValueError(f"Unknown measure type: {measure_type}")

    # Pass the Parameters to the plotting function
    return plot_signals_generic(measure, signals, "Cleaned Signals Peaks", labels, colors, peaks=peaks)

def plotSQA(measure):
    """Plot the cleaned signals with detected peaks from the measure dictionary."""
    red_signal = measure.get("RedSignal", [])
    ir_signal = measure.get("IrSignal", [])
    sampling_rate = measure.get("measureFrequency", 0)

    # Get the measure type
    measure_type = measure.get("measureType", "")

    # Initialize signals and peaks
    signals, labels, colors, peaks, qualities = [], [], [], [], []

    # Process signals based on the measure type
    if measure_type == "IR Only":
        if not ir_signal:
            raise ValueError("Missing necessary IR signal data in the measure.")
        ir_cleaned = filter_signal(ir_signal, sampling_rate)
        ir_peaks_dict = peak_finder(ir_cleaned, sampling_rate)
        ir_peaks = ir_peaks_dict["PPG_Peaks"]
        ir_quality = ppg_sqa(ir_cleaned, ir_peaks, sampling_rate)
        
        signals.append(normalize_signal(ir_cleaned))
        labels.append("Filtered IR Signal")
        colors.append("#1282b2")
        peaks.append(ir_peaks)
        qualities.append(ir_quality)
    elif measure_type == "Red + IR":
        if not red_signal or not ir_signal:
            raise ValueError("Missing necessary signal data for Red + IR in the measure.")
        ir_cleaned = filter_signal(ir_signal, sampling_rate)
        ir_peaks_dict = peak_finder(ir_cleaned, sampling_rate)
        ir_peaks = ir_peaks_dict["PPG_Peaks"]
        ir_quality = ppg_sqa(ir_cleaned, ir_peaks, sampling_rate)

        red_cleaned = filter_signal(red_signal, sampling_rate)
        red_peaks_dict = peak_finder(red_cleaned, sampling_rate)
        red_peaks = red_peaks_dict["PPG_Peaks"]
        red_quality = ppg_sqa(red_cleaned, red_peaks, sampling_rate)

        signals.extend([normalize_signal(red_cleaned), normalize_signal(ir_cleaned)])
        labels.extend(["Filtered Red Signal", "Filtered IR Signal"])
        colors.extend(["#ff2c2c", "#1282b2"])
        peaks.extend([red_peaks, ir_peaks])
        qualities.extend([red_quality, ir_quality])
    else:
        raise ValueError(f"Unknown measure type: {measure_type}")

    # Pass the Parameters to the plotting function
    return plot_signals_generic(measure, signals, "Cleaned Signals Peaks", labels, colors, peaks=peaks, qualities= qualities)

def plot_ppg_process(measure):
    """Plot the processed signals with detected peaks from the measure dictionary."""
    red_signal = measure.get("RedSignal", [])
    ir_signal = measure.get("IrSignal", [])
    sampling_rate = measure.get("measureFrequency", 0)

    # Get the measure type
    measure_type = measure.get("measureType", "")

    ir_signals, ir_info = ppg_process(ir_signal, sampling_rate)

    # Initialize signals and peaks
    signals, labels, colors, peaks, qualities = [], [], [], [], []

    # Process signals based on the measure type
    if measure_type == "IR Only":
        if not ir_signal:
            raise ValueError("Missing necessary IR signal data in the measure.")
        # Process signal
        ir_signals, ir_info = ppg_process(ir_signal, sampling_rate)

        # Extract processed signals
        ir_cleaned = ir_signals["PPG_Clean"]
        ir_peaks = ir_info["PPG_Peaks"]
        ir_rate = np.median(np.array(ir_signals["PPG_Rate"]))
        ir_quality = ir_signals["PPG_Quality"]

        signals.append(normalize_signal(ir_cleaned))
        labels.append("Filtered IR Signal")
        colors.append("#1282b2")
        peaks.append(ir_peaks)
    elif measure_type == "Red + IR":
        if not red_signal or not ir_signal:
            raise ValueError("Missing necessary signal data for Red + IR in the measure.")
        # Process signals
        ir_signals, ir_info = ppg_process(ir_signal, sampling_rate)
        red_signals, red_info = ppg_process(red_signal, sampling_rate)

        ir_cleaned = filter_signal(ir_signal, sampling_rate)
        ir_peaks_dict = peak_finder(ir_cleaned, sampling_rate)
        ir_peaks = ir_peaks_dict["PPG_Peaks"]
        ir_quality = ppg_sqa(ir_cleaned, ir_peaks, sampling_rate)

        red_cleaned = filter_signal(red_signal, sampling_rate)
        red_peaks_dict = peak_finder(red_cleaned, sampling_rate)
        red_peaks = red_peaks_dict["PPG_Peaks"]
        red_quality = ppg_sqa(red_cleaned, red_peaks, sampling_rate)

        signals.extend([normalize_signal(red_cleaned), normalize_signal(ir_cleaned)])
        labels.extend(["Filtered Red Signal", "Filtered IR Signal"])
        colors.extend(["#ff2c2c", "#1282b2"])
        peaks.extend([red_peaks, ir_peaks])
        qualities.extend([red_quality, ir_quality])
    else:
        raise ValueError(f"Unknown measure type: {measure_type}")

    # Pass the Parameters to the plotting function
    return plot_signals_generic(measure, signals, "Cleaned Signals Peaks", labels, colors, peaks=peaks, qualities= qualities)

def plot_beats(measure):
    """Plot the processed signals with detected peaks from the measure dictionary."""
    ir_signal = measure.get("IrSignal", [])
    sampling_rate = measure.get("measureFrequency", 0)

    # Clean the signal and extract its beats
    ir_clean = filter_signal(ir_signal, sampling_rate)
    ir_peaks_dict = peak_finder(ir_clean, sampling_rate)
    ir_peaks = ir_peaks_dict["PPG_Peaks"]
    ir_beats = ppg_heart_beats(ir_clean, ir_peaks, sampling_rate)

    average_signal_df = calculate_avg_beat(ir_beats)

    # Initialize the plot
    fig, ax = plt.subplots(figsize=(8, 5))

    # Loop through each beat in the dictionary and plot its signal
    for beat_index, beat_info in ir_beats.items():
        # Get the time data (index of the sub-dictionary)
        time_data = beat_info.index  # Index represents time
        signal_data = beat_info['Signal']  # Signal values for the y-axis

        # Plot each beat with a distinct label
        ax.plot(time_data, signal_data, linewidth = 0.75, alpha=0.85, color='silver')
    
    # Plot average beat
    ax.plot(average_signal_df["Time"], average_signal_df["Average Signal"],linewidth=6, alpha=0.75, label="Average Signal", color="royalblue")

    # Add a vertical dotted line at time = 0
    ax.axvline(x=0, color='dimgrey', linestyle='--', linewidth=1.25)

    # Configure plot appearance
    ax.set_title(f"Processed Beats - IR Only")
    ax.set_xlabel('Time (s)')  # Assuming each beat data is indexed by time
    ax.set_ylabel('PPG Value')
    ax.grid(False)
    ax.legend(loc='upper right')

    # Save the figure to a buffer (in-memory image)
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)  # Rewind the buffer to the beginning

    # Close the figure to free up memory
    plt.close(fig)

    return buf  # Return the buffer object