import streamlit as st
import os
import logging
import configs
from mqtt_manager import MQTTManager
from data_manager import convert_signals_to_lists
from data_logger import load_measures
from app_functions import (select_box_sensor_params, pills_measure_type, pills_sensor_params,
                           select_box_measure, selectPlotType, delete_measure_bt, cssStyling,
                           pending_categorization, categorization_stats)

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

def measurement_screen(file, file_path):
    # Apply custom CSS styling on the page
    cssStyling()

    # Top container for header and settings
    with st.container():
        st.title("SmartBP Web App 🩺")
        st.subheader("Manage your SmartBP measurements seamlessly.")

    # Sensor Parameterization Container
    with st.container():   
        st.header("Sensor Parameterization and Measure Request")

        col1, col2, col3, col4 = st.columns([1, 1, 1, 4])
        with col1:
            # Select box to select the sensor parameters
            selected_param = select_box_sensor_params()           
            mqtt.update_sensor_param(selected_param)

        with col2:
            # Select measure type
            measure_type = ["IR Only", "RED + IR"]
            selected_measure_type = st.selectbox("Select Type of Measure", measure_type)
            mqtt.update_measure_type(selected_measure_type)

        with col3:
            # Select array size
            set_array_size = ["500", "750", "1000", "1250"]
            selected_array_size = st.selectbox("Set the number of samples per measure", set_array_size)
            mqtt.update_array_size(selected_array_size)
        with col4:
            st.empty()

    # Measurement Request Container
    with st.container():
        st.header("Request a Measure")

        # Display current selected parameters
        st.write(f"Selected Sensor Parameter: {selected_param}")
        st.write(f"Selected Measure Type: {selected_measure_type}")
        st.write(f"Array Size: {selected_array_size}")

        # Request new measure button
        request_new_measure_button()

    # Measurement Visualization Container
    with st.container(key="measurement_visualization"):
        st.header("Measurement Visualization")

        # Measure selection and deletion
        col1, col2, col3, col4 = st.columns([1, 2.25, 1, 3.5])  # Wider column for measure selection
        with col1:
            measureType = pills_measure_type()

        with col2:
            measures = pills_sensor_params(file)

        with col3:
            selected_measure = select_box_measure(measures, measureType)

        with col4:
            delete_measure_bt(measures ,selected_measure, measures, file_path)

        with st.container():
            col1, col2 = st.columns([1, 6])
            with col1:
                # Check if selected_measure exists (i.e., it's not None or an empty value)
                if selected_measure:
                    # Parse the signals strings to lists
                    measureForPlot = convert_signals_to_lists(selected_measure)

                    # Plot visualization
                    plot_buf = selectPlotType(measureForPlot)

            with col2:
                st.empty()

        if plot_buf:
            st.image(plot_buf, use_container_width=True)

    # Placeholder for any dynamic updates or waiting states
    st.empty()

def categorization_screen(file, file_path):
    # Top container for header and settings
    with st.container():
        st.title("SmartBP Web App 🩺")
        st.subheader("Categorize your SmartBP measurements.")

    # Pending Categorization Section
    st.header("Pending Categorization")
    st.write("Edit the 'Category' column to categorize your measures.")
    pending_categorization(file, file_path)

    # Categorization Statistics Section
    st.header("Categorization Statistics")
    categorization_stats(file)

def main():  
    
    # Load existing measures
    file_path = configs.MEASURE_LOGGER
    file = load_measures(file_path)

    # Add a sidebar menu for selecting the table to display
    menu_selection = st.sidebar.selectbox("Menu", ("Measures","Categorization"))

    if menu_selection == "Measures":
        measurement_screen(file, file_path)
    elif menu_selection == "Categorization":
        categorization_screen(file, file_path)

if __name__ == "__main__":
    main()




