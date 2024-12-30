import streamlit as st
from mqtt_manager import MQTTManager
from data_manager import convert_signals_to_lists
from data_logger import load_measures
from app_functions import select_measure_box, selectPlotType
from plots import plotRawData, plotRawAndFilteredData, plotFilteredData, plotFFT
import configs

# Set page configuration
st.set_page_config(
    page_title="SmartBP App",
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
    # Display a selectbox to choose the sensor parameter
    sensor_parameters = ['Default', '800 Hz - 4 samples', '1000 Hz - 8 samples', '1600 Hz - 8 samples', '1600 Hz - 16 samples']
    selected_param = st.selectbox("Select Sensor Parameters", sensor_parameters)

    # Update the parameter in the MQTTManager
    mqtt.update_sensor_param(selected_param)

    # Get the file path for the selected parameter
    file_path = configs.SENSOR_PARAMETERS[selected_param]

    # Load existing measures
    measures = load_measures(file_path)
    
    # Function to handle the request of a new measure button
    request_new_measure_button()
    
    # Function to handle the box to select the measure
    selected_measure = select_measure_box(measures)

    # Parse the signals strings to lists
    selected_measure = convert_signals_to_lists(selected_measure)

    # Function to handle the box to select the plot type
    plot_buf = selectPlotType(selected_measure)

    # If plot buffer is available, display the plot
    if plot_buf:
        st.image(plot_buf, use_container_width=True)

    # Display a placeholder while waiting for data
    st.empty()

if __name__ == "__main__":
    main()