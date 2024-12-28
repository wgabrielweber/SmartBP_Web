import streamlit as st
from mqtt_manager import MQTTManager
import configs

# Set page configuration
st.set_page_config(
    page_title="SmartBP App",
    page_icon="🩺",
    layout="wide",
)

# Global variables to hold the selected sensor parameter
selected_sensor_param = None

mqtt_manager = MQTTManager(
        broker_address=configs.BROKER_ADDRESS,
        command_topic=configs.COMMAND_TOPIC,
        data_topic=configs.DATA_TOPIC
)

def main():
    # Store the selected sensor parameters in session state to persist between runs
    if 'selected_sensor_param' not in st.session_state:
        st.session_state.selected_sensor_param = None

    # Display a selectbox to choose the sensor parameter
    sensor_parameters = ['800 Hz - 4 samples', '1000 Hz - 8 samples', '1000 Hz - 8 samples', '1600 Hz - 16 samples']  # List of available sensor parameters
    st.session_state.selected_sensor_param = st.selectbox("Select Sensor Parameters", sensor_parameters)

    if st.button("Request New Measure"):
        # Publish the command to request a new measure
        mqtt_manager.publish_command("new_measure")
        st.info("Measurement requested. Waiting for data...")

    # Display a placeholder while waiting for data
    st.empty()

    # Stop MQTT when the app ends
    if st.session_state.get("stop_mqtt"):
        mqtt_manager.stop()

if __name__ == "__main__":
    main()