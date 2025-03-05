import paho.mqtt.client as mqtt
import data_parser
from configs_st import REQUEST_MEASURE_TOPIC, REQUEST_IR_MEASURE_TOPIC, SENSOR_SETUP_TOPIC

class MQTTManager:
    def __init__(self, broker_address, command_topic, data_topic):
        self.client = mqtt.Client()
        self.broker_address = broker_address
        self.command_topic = command_topic
        self.data_topic = data_topic
        self.sensor_param = 2
        self.measure_type = REQUEST_IR_MEASURE_TOPIC 
        self.array_size = 750

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
        print(f'publishing "{message}" on {topic}')
        self.client.publish(topic, message)

    def subscribe_to_data_topic(self):
        """Subscribe to the data topic."""
        print(f'Subscribed to {self.data_topic}')
        self.client.subscribe(self.data_topic)

    def update_measure_type(self, measure_type):
        """
        Update the measure type and set the appropriate command topic.
        """
        self.measure_type = measure_type
        if measure_type == "RED + IR":
            self.command_topic = REQUEST_MEASURE_TOPIC
        elif measure_type == "IR Only":
            self.command_topic = REQUEST_IR_MEASURE_TOPIC
        else:
            raise ValueError(f"Invalid measure type: {measure_type}")

    def update_array_size(self, measure_samples):
        """
        Update the number of samples of a measure.
        The value should match one of the selectable values.
        """
        valid_samples = ["500", "750", "1000", "1250"]
        if measure_samples not in valid_samples:
            raise ValueError(f"Invalid array size: {measure_samples}")
        self.array_size = measure_samples

    def update_sensor_param(self, param):
        """
        Update the sensor parameter and publish a message to the SENSOR_SETUP_TOPIC.
        """
        sensor_param_map = {
            "Default": 2,
            "800 Hz - 4 samples": 1,
            "1000 Hz - 8 samples": 2,
            "1600 Hz - 8 samples": 3,
            "1600 Hz - 16 samples": 4,
        }

        if param not in sensor_param_map:
            raise ValueError(f"Invalid sensor parameter: {param}")

        new_sensor_param = sensor_param_map[param]

        # Only publish if the parameter has changed
        if new_sensor_param != self.sensor_param:
            self.sensor_param = new_sensor_param
            self.publish(SENSOR_SETUP_TOPIC, self.sensor_param)

    def on_message(self, client, userdata, msg):
        """
        Handle incoming MQTT messages.
        Forward messages received on the data topic.
        """
        if msg.topic == self.data_topic:
            print(f"Message received at {self.data_topic}. Forwarding for processing.")
            self.handle_data_message(msg.payload.decode())

    def handle_data_message(self, message):
        """
        Pass the message to the parse_message function for processing.
        """
        try:
            data_parser.parse_message(message)
        except Exception as e:
            print(f"Failed to process message: {e}")