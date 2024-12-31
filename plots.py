import io
import matplotlib.pyplot as plt

def plot_signals_generic(measure, signals_to_plot, title, labels, colors, alphas=None, linewidths=None):
    """Generic function to plot signals and return the image as a buffer."""
    # Extract the timestamp and measurement frequency
    dt = measure.get("timestamp", "Unknown Timestamp")
    measure_freq = measure.get("measureFrequency", 0)

    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 5))

    # Plot each signal with its corresponding label, color, and optional style parameters
    for i, signal in enumerate(signals_to_plot):
        alpha = alphas[i] if alphas else 1.0
        linewidth = linewidths[i] if linewidths else 1.0
        ax.plot(signal, label=labels[i], color=colors[i], alpha=alpha, linewidth=linewidth)

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

def plotRawData(measure):
    """Plot the raw signals from the measure dictionary."""
    signals = measure.get("signals", {})
    red_signal = signals.get("redMeasure", [])
    ir_signal = signals.get("irMeasure", [])

    if not red_signal or not ir_signal:
        raise ValueError("Missing necessary signal data in the measure.")

    labels = ['Original Red Signal', 'Original IR Signal']
    colors = ['#ff2c2c', '#1282b2']
    return plot_signals_generic(measure, [red_signal, ir_signal], "Original Signals", labels, colors)

def plotFilteredDataCheby(measure):
    """Plot the filtered signals from the measure dictionary."""
    signals = measure.get("signals", {})
    sqi = measure.get("sqi", {})
    
    red_signal = signals.get("redFilteredCheby", [])
    ir_signal = signals.get("irFilteredCheby", [])

    red_sqi = sqi.get("red_cheby_skew", 0)
    ir_sqi = sqi.get("ir_cheby_skew", 0)

    if not red_signal or not ir_signal:
        raise ValueError("Missing necessary signal data in the measure.")

    labels = [
        f'Filtered Red Signal: SQI {red_sqi:.3f}', 
        f'Filtered IR Signal: SQI {ir_sqi:.3f}'
    ]
    colors = ['#ff2c2c', '#1282b2']
    return plot_signals_generic(measure, [red_signal, ir_signal], "Filtered Signals [Chebyshev II]", labels, colors)

def plotRawAndFilteredDataCheby(measure):
    """Plot the raw and filtered signals for comparison."""
    signals = measure.get("signals", {})
    sqi = measure.get("sqi", {})
    
    red_signal = signals.get("redMeasure", [])
    ir_signal = signals.get("irMeasure", [])
    red_cheby_signal = signals.get("redFilteredCheby", [])
    ir_cheby_signal = signals.get("irFilteredCheby", [])

    red_cheby_sqi = sqi.get("red_cheby_skew", 0)
    ir_cheby_sqi = sqi.get("ir_cheby_skew", 0)

    if not red_cheby_signal or not ir_cheby_signal:
        raise ValueError("Missing necessary signal data in the measure.")

    labels = [
        'Original Red Signal', 
        'Original IR Signal', 
        f'Filtered Red Signal [Cheby II]: SQI {red_cheby_sqi:.3f}', 
        f'Filtered IR Signal [Cheby II]: SQI {ir_cheby_sqi:.3f}',
    ]
    colors = ['#ff2c2c', '#2596be', '#ff2c2c', '#2596be', '#f28822', '#1db280']
    alphas = [0.75, 0.75, 1.0, 1.0]
    linewidths = [0.5, 0.5, 1.0, 1.0]
    
    signals_to_plot = [
        red_signal, ir_signal, 
        red_cheby_signal, ir_cheby_signal, 
    ]
    return plot_signals_generic(measure, signals_to_plot, "Raw and Filtered Signals Comparison [Chebyshev II]", labels, colors, alphas, linewidths)

def plotFilteredDataMAF(measure):
    """Plot the filtered signals from the measure dictionary."""
    signals = measure.get("signals", {})
    sqi = measure.get("sqi", {})
    
    red_signal = signals.get("redFilteredMA", [])
    ir_signal = signals.get("irFilteredMA", [])

    red_sqi = sqi.get("red_movavg_skew", 0)
    ir_sqi = sqi.get("ir_movavg_skew", 0)

    if not red_signal or not ir_signal:
        raise ValueError("Missing necessary signal data in the measure.")

    labels = [
        f'Filtered Red Signal: SQI {red_sqi:.3f}', 
        f'Filtered IR Signal: SQI {ir_sqi:.3f}'
    ]
    colors = ['#ff2c2c', '#1282b2']
    return plot_signals_generic(measure, [red_signal, ir_signal], "Filtered Signals [MAF]", labels, colors)

def plotRawAndFilteredDataMAF(measure):
    """Plot the raw and filtered signals for comparison."""
    signals = measure.get("signals", {})
    sqi = measure.get("sqi", {})
    
    red_signal = signals.get("redMeasure", [])
    ir_signal = signals.get("irMeasure", [])
    red_movavg_signal = signals.get("redFilteredMA", [])
    ir_movavg_signal = signals.get("irFilteredMA", [])

    red_movavg_sqi = sqi.get("red_movavg_skew", 0)
    ir_movavg_sqi = sqi.get("ir_movavg_skew", 0)

    if not red_signal or not ir_signal:
        raise ValueError("Missing necessary signal data in the measure.")

    labels = [
        'Original Red Signal', 
        'Original IR Signal', 
        f'Filtered Red Signal [Mov Avg]: SQI {red_movavg_sqi:.3f}', 
        f'Filtered IR Signal [Mov Avg]: SQI {ir_movavg_sqi:.3f}'
    ]
    colors = ['#ff2c2c', '#2596be', '#ff2c2c', '#2596be']
    alphas = [0.75, 0.75, 1.0, 1.0]
    linewidths = [0.5, 0.5, 1.0, 1.0]
    
    signals_to_plot = [
        red_signal, ir_signal, 
        red_movavg_signal, ir_movavg_signal
    ]
    return plot_signals_generic(measure, signals_to_plot, "Raw and Filtered Signals Comparison [MAF]", labels, colors, alphas, linewidths)

def plotFilteredDataComparison(measure):
    """Plot the raw and filtered signals for comparison."""
    signals = measure.get("signals", {})
    sqi = measure.get("sqi", {})
    
    red_cheby_signal = signals.get("redFilteredCheby", [])
    ir_cheby_signal = signals.get("irFilteredCheby", [])
    red_movavg_signal = signals.get("redFilteredMA", [])
    ir_movavg_signal = signals.get("irFilteredMA", [])

    red_movavg_sqi = sqi.get("red_movavg_skew", 0)
    ir_movavg_sqi = sqi.get("ir_movavg_skew", 0)
    red_cheby_sqi = sqi.get("red_cheby_skew", 0)
    ir_cheby_sqi = sqi.get("ir_cheby_skew", 0)

    if not red_cheby_signal or not ir_cheby_signal:
        raise ValueError("Missing necessary signal data in the measure.")

    labels = [
        f'Filtered Red Signal [Cheby II]: SQI {red_cheby_sqi:.3f}', 
        f'Filtered IR Signal [Cheby II]: SQI {ir_cheby_sqi:.3f}',
        f'Filtered Red Signal [Mov Avg]: SQI {red_movavg_sqi:.3f}', 
        f'Filtered IR Signal [Mov Avg]: SQI {ir_movavg_sqi:.3f}'
    ]
    colors = ['#ff2c2c', '#2596be', '#990000', '#003399']
    alphas = [0.75, 0.75, 0.75, 0.75]
    linewidths = [1.0, 1.0, 1.0, 1.0]
    
    signals_to_plot = [
        red_cheby_signal, ir_cheby_signal, 
        red_movavg_signal, ir_movavg_signal
    ]
    return plot_signals_generic(measure, signals_to_plot, "Filtered Signals Comparison", labels, colors, alphas, linewidths)

def plotFFT():
    return None