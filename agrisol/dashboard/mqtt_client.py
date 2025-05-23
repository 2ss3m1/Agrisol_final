import json
import threading
import paho.mqtt.client as mqtt
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    print(f"Received MQTT message: {data}")
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "sensor_data_group",  # le même nom de groupe que dans le consumer
        {
        "type": "send_sensor_data",  # doit matcher le nom de la méthode dans le consumer
        "message": data
        }
)

def mqtt_thread():
    client = mqtt.Client()
    client.connect("localhost", 1883, 60)
    client.subscribe("agrisol/data")
    client.on_message = on_message
    client.loop_forever()

def start():
    thread = threading.Thread(target=mqtt_thread)
    thread.daemon = True
    thread.start()
