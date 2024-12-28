import paho.mqtt.client as mqtt
import data_parser

class MQTTManager:
    def __init__(self, broker_address, command_topic, data_topic):
        self.client = mqtt.Client()
        self.broker_address = broker_address
        self.command_topic = command_topic
        self.data_topic = data_topic

        # Set callbacks
        self.client.on_message = self.on_message

    def connect(self):
        """Connect to the MQTT broker."""
        self.client.connect(self.broker_address)

    def start_loop(self):
        """Start the MQTT client loop."""
        self.client.loop_start()

    def stop_loop(self):
        """Stop the MQTT client loop."""
        self.client.loop_stop()

    def publish(self, topic, message):
        """Publish a message to a topic."""
        self.client.publish(topic, message)

    def subscribe_to_data_topic(self):
        """Subscribe to the data topic."""
        self.client.subscribe(self.data_topic)

    def on_message(self, client, userdata, msg):
        """Handle incoming MQTT messages."""
        if msg.topic == self.data_topic:
            # Use session state to get the selected sensor parameter from the Streamlit app
            from app import st
            selected_sensor_param = st.session_state.selected_sensor_param
            self.handle_data_message(msg.payload.decode(), selected_sensor_param)

    def handle_data_message(self, message, sensor_param):
        """Pass the message and sensor_param to the parse_message function."""
        try:
            # Call parse_message function
            data_parser.parse_message(message, sensor_param)
            print(f"Message processed. Sensor parameters: {sensor_param}")
        except Exception as e:
            print(f"Failed to process message: {e}")