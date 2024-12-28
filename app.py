import os
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
import time
import paho.mqtt.client as mqtt
from data_analysis import load_data, parse_last_line, apply_filter, plot_signals

# Set page configuration
st.set_page_config(
    page_title="Central de Medições",
    page_icon="🩺",
    layout="wide",
)

# MQTT broker information
BROKER_ADDRESS = "192.168.15.12"
TOPIC = "prototype_esp/command"  # Replace with your MQTT topic

# MQTT callback function to confirm the message was sent
def on_publish(client, userdata, mid):
    st.session_state.mqtt_publish_success = True
    st.session_state.success_message_time = time.time()  # Record the time of success

def main():
    # MQTT trigger inside the main loop
    if st.button("Request New Measure"):
        # Set up MQTT client and connect to broker
        client = mqtt.Client()
        client.on_publish = on_publish
        client.connect(BROKER_ADDRESS)

        # Send MQTT message
        client.publish(TOPIC, "new_measure")

        # Start the MQTT client loop in the background to ensure the message is sent
        client.loop_start()
        time.sleep(2)  # Give some time for the message to be sent
        client.loop_stop()  # Stop the MQTT client loop
        client.disconnect()

    # Wait for the measure to be done
    time.sleep(7)

    # CSV file path
    csv_file = "C:/Users/wgabr/TCC/CollectedData/red_ir_comparison.csv"
    
     # Read and process data
    try:
        dt, measure_time, red_signal, ir_signal = parse_last_line(csv_file)
        fs = len(red_signal) / measure_time

        # Apply bandpass filter to signals
        filtered_red, filtered_ir = apply_filter(red_signal, ir_signal, fs)

        # Get the plot as an in-memory image
        plot_buffer = plot_signals(dt, fs, red_signal, ir_signal, filtered_red, filtered_ir)

        # Display the plot in Streamlit using st.image
        st.image(plot_buffer, use_container_width=True)

    except Exception as e:
        st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()