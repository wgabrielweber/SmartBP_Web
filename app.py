import streamlit as st
import os
import logging
from mqtt_manager import MQTTManager
from data_manager import convert_signals_to_lists
from data_logger import load_measures
from app_functions import select_measure_box, selectPlotType, delete_measure_bt, cssStyling
import configs

# Suppress Streamlit warnings by setting log level
os.environ["STREAMLIT_LOG_LEVEL"] = "error"

# Suppress loggers
logging.getLogger("streamlit").setLevel(logging.ERROR)
logging.getLogger("paho").setLevel(logging.CRITICAL)  # Suppress paho-mqtt logs
logging.getLogger().setLevel(logging.ERROR)  # Suppress root logger warnings

# Set page configuration
st.set_page_config(
    page_title="SmartBP Web App",
    page_icon="🩺",
    layout="wide",
)

def request_new_measure_button():   
    # Button to request a new measure
    if st.button("Request New Measure"):
        # Publish the command to request a new measure
        mqtt.publish(mqtt.command_topic, mqtt.array_size)

# Initialize MQTTManager instance only once
if "mqtt_instance" not in st.session_state:
    mqtt_instance = MQTTManager(
        broker_address=configs.BROKER_ADDRESS,
        command_topic=configs.REQUEST_IR_MEASURE_TOPIC,  # Default to IR Only
        data_topic=configs.DATA_TOPIC,
    )
    mqtt_instance.connect()
    mqtt_instance.start_loop()
    mqtt_instance.subscribe_to_data_topic()
    st.session_state["mqtt_instance"] = mqtt_instance

mqtt = st.session_state["mqtt_instance"]

def main():
    # Apply custom CSS styling on the page
    cssStyling()

    # Top container for header and settings
    with st.container():
        st.title("SmartBP Web App 🩺")
        st.subheader("Manage your SmartBP measurements seamlessly.")

    # Sensor parameter selection
    with st.container():
        st.header("Sensor Parameterization")

        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            # Select sensor parameters
            sensor_parameters = [
                "Default",
                "800 Hz - 4 samples",
                "1000 Hz - 8 samples",
                "1600 Hz - 8 samples",
                "1600 Hz - 16 samples",
            ]
            selected_param = st.selectbox("Select Sensor Parameters", sensor_parameters)
            mqtt.update_sensor_param(selected_param)

        with col2:
            # Select measure type
            measure_type = ["IR Only", "RED + IR"]
            selected_measure_type = st.selectbox("Select Type of Measure", measure_type)
            mqtt.update_measure_type(selected_measure_type)

        with col3:
            # Select array size
            set_array_size = ["500", "750", "1000", "1250"]
            selected_array_size = st.selectbox("Set Measure Sample Number", set_array_size)
            mqtt.update_array_size(selected_array_size)

    # Request Measure button with selected parameters info
    with st.container():
        st.header("Request a Measure")

        # Display current selected parameters
        st.write(f"Selected Sensor Parameter: {selected_param}")
        st.write(f"Selected Measure Type: {selected_measure_type}")
        st.write(f"Array Size: {selected_array_size}")

        # Request new measure button
        request_new_measure_button()

    # Third container: Measurement visualization
    with st.container():
        st.header("Measurement Visualization")

        # Load existing measures
        file_path = configs.SENSOR_PARAMETERS[selected_param]
        measures = load_measures(file_path)

        # Measure selection and deletion
        col1, col2 = st.columns([1, 4])  # Wider column for measure selection
        with col1:
            selected_measure = select_measure_box(measures)

        with col2:
            delete_measure_bt(selected_measure, measures, file_path)

        # Check if selected_measure exists (i.e., it's not None or an empty value)
        if selected_measure:
            # Parse the signals strings to lists
            measureForPlot = convert_signals_to_lists(selected_measure)

            # Plot visualization
            plot_buf = selectPlotType(measureForPlot)
            if plot_buf:
                st.image(plot_buf, use_container_width=True)

    # Placeholder for any dynamic updates or waiting states
    st.empty()

if __name__ == "__main__":
    main()
