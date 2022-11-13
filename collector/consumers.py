import json
from asyncio import sleep
from channels.generic.websocket import AsyncWebsocketConsumer


class CollectorConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(json.dumps({'test': 'This is a test !'}))
        await sleep(1)
