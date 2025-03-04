import paho.mqtt.client as mqtt

# Define event callbacks
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("/patrol_robot/#") # Subscribe to the topic

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload)) # Print received message

# Create MQTT client instance
client = mqtt.Client(client_id="learn_test")
client.username_pw_set("admin", "public")
# Set up event callbacks
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
client.connect("124.223.72.28", 1883, 60)

# Start the MQTT client loop in a non-blocking way
client.loop_start()

# Publish a message to the topic
client.publish("<topic>", "<message>")

# Wait for incoming messages
while True:
    pass

# Stop the MQTT client loop
client.loop_stop()

if __name__ == '__main__':
    pass



