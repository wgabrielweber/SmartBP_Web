import matplotlib.pyplot as plt
import io

def plot_raw_sensor_data(sensor_param, formatted_datetime, measureTime, redMeasure, irMeasure):

    return

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