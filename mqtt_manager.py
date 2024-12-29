import paho.mqtt.client as mqtt
import data_parser

class MQTTManager:
    def __init__(self, broker_address, command_topic, data_topic):
        self.client = mqtt.Client()
        self.broker_address = broker_address
        self.command_topic = command_topic
        self.data_topic = data_topic
        self.sensor_param = None

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

    def update_sensor_param(self, param):
        """Update the sensor parameter."""
        self.sensor_param = param

    def on_message(self, client, userdata, msg):
        """Handle incoming MQTT messages."""
        if msg.topic == self.data_topic:
            print(f"Message received at {self.data_topic}. Sensor Parameter: {self.sensor_param}")

            if self.sensor_param:
                self.handle_data_message(msg.payload.decode(), self.sensor_param)
            else:
                print("Sensor parameter not initialized!")

    def handle_data_message(self, message, sensor_param):
        """Pass the message and sensor_param to the parse_message function."""
        try:
            data_parser.parse_message(message, sensor_param)
        except Exception as e:
            print(f"Failed to process message: {e}")