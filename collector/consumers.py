import json
from asyncio import sleep
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.template.loader import get_template


class CollectorConsumer(WebsocketConsumer):

    groups = ["broadcast"]

    def connect(self):
        # self.room_name = 'loggers_room'
        # self.room_group_name = self.room_name + '_collector'
        # async_to_sync(self.channel_layer.group_add)(
        #     self.room_group_name,
        #     self.channel_name
        # )
        self.accept()
        self.close()
        print(f'--> Connected!')

    def disconnect(self, code):
        # async_to_sync(self.channel_layer.group_discard)(
        #     self.room_group_name,
        #     self.channel_name
        # )
        print(f"--> Disconnected [{code}]!")

    def receive(self, text_data=None, bytes_data=None):
        print("--> Received")
        data = json.loads(text_data)
        message = data['message']
        # async_to_sync(self.channel_layer.group_send)(
        self.send(text_data={
            # self.room_group_name, {
                "type": 'shoot_message',
                "message": message
            }
        )

    def shoot_message(self, msg):
        template = get_template("collector/messenger.html")
        payload = template.render({'msg': {'txt': msg.txt, "tags": msg.tags}}, None)
        self.send(text_data=json.dumps({'data': payload}))
        print("--> Shoot message ")

        # if messages:
        #     for message in messages:
        #         template = get_template("collector/messenger.html")
        #         payload = template.render({'message': message}, None)
        #         self.send(text_data=json.dumps({'data': payload}))
        #         sleep(1)
        # if messages:
        #     for message in messages:
        #         self.send(text_data=json.dumps({'data': message}))
        #         sleep(1)

    # def disconnect(self, code):
    #     print("disconnect", code)
