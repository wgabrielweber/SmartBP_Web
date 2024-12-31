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
        mqtt.publish(configs.COMMAND_TOPIC, "new_measure")

# Initialize MQTTManager instance only once
if "mqtt_instance" not in st.session_state:
    mqtt_instance = MQTTManager(
        broker_address=configs.BROKER_ADDRESS,
        command_topic=configs.COMMAND_TOPIC,
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

    # Layout for sensor parameter selection and request button
    with st.container():
        col1, col2 = st.columns([1, 4])  # Wider column for parameter selection
        with col1:
            sensor_parameters = [
                "Default",
                "800 Hz - 4 samples",
                "1000 Hz - 8 samples",
                "1600 Hz - 8 samples",
                "1600 Hz - 16 samples",
            ]
            selected_param = st.selectbox("Select Sensor Parameters", sensor_parameters)

            # Update the parameter in the MQTTManager
            mqtt.update_sensor_param(selected_param)

        with col2:
            request_new_measure_button()

    # Load existing measures
    file_path = configs.SENSOR_PARAMETERS[selected_param]
    measures = load_measures(file_path)

    # Layout for measure selection and deletion
    with st.container():
        col1, col2 = st.columns([1, 4])  # Wider column for measure selection
        with col1:
            selected_measure = select_measure_box(measures)
            
        with col2:
            delete_measure_bt(selected_measure, measures, file_path)
            
    # Check if selected_measure exists (i.e., it's not None or an empty value)
    if selected_measure:
        # Parse the signals strings to lists
        measureForPlot = convert_signals_to_lists(selected_measure)

    # Layout for plot display
    with st.container():
        st.subheader("Measurement Visualization")
        if selected_measure:
            plot_buf = selectPlotType(measureForPlot)
            if plot_buf:
                st.image(plot_buf, use_container_width=True)

    # Placeholder for any dynamic updates or waiting states
    st.empty()

if __name__ == "__main__":
    main()