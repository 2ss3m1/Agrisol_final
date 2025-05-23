import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer


class SensorDataConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("sensor_data_group", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("sensor_data_group", self.channel_name)

    async def receive(self, text_data):
        # Si tu veux tester l'envoi manuel depuis le navigateur
        await self.send(text_data=json.dumps({
            'message': 'Message reçu'
        }))

    async def send_sensor_data(self, event):
       data = event['message']
       print("send_sensor_data appelé avec:", data)
       await self.send(text_data=json.dumps(data))
