import streamlit as st

# Accessing MQTT information
BROKER_ADDRESS = st.secrets["mqtt"]["broker_address"]
COMMAND_TOPIC = st.secrets["mqtt"]["command_topic"]
REQUEST_MEASURE_TOPIC = st.secrets["mqtt"]["request_measure_topic"]
REQUEST_IR_MEASURE_TOPIC = st.secrets["mqtt"]["request_ir_measure_topic"]
SENSOR_SETUP_TOPIC = st.secrets["mqtt"]["sensor_setup_topic"]
DATA_TOPIC = st.secrets["mqtt"]["data_topic"]

# Accessing MongoDB information
MONGO_URI = st.secrets["mongo"]["uri"]
DB_NAME = st.secrets["mongo"]["db_name"]
COLLECTION_NAME = st.secrets["mongo"]["collection_name"]

# Accessing sensor parameters mapping
SENSOR_PARAMETERS = {
    "Default": st.secrets["sensor_parameters"]["default"],
    "800 Hz - 4 samples": st.secrets["sensor_parameters"]["samples4_freq800"],
    "1000 Hz - 8 samples": st.secrets["sensor_parameters"]["samples8_freq1000"],
    "1600 Hz - 8 samples": st.secrets["sensor_parameters"]["samples8_freq1600"],
    "1600 Hz - 16 samples": st.secrets["sensor_parameters"]["samples16_freq1600"],
}
