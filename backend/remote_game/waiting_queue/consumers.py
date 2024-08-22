import asyncio
import json

from channels.generic.websocket import AsyncWebsocketConsumer
from . import WaitingQueue

WaitingQueue = WaitingQueue.WaitingQueue()

class WaitingQueueConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if not WaitingQueue.is_running():  # Assuming you have a way to check if it's already running
            asyncio.create_task(WaitingQueue.start())
        await WaitingQueue.put(self.channel_name)
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        pass

    async def disconnect(self, code):
        await WaitingQueue.delete_from_queue(self.channel_name)

    async def match_found(self, event):
        match_name = event['match_name']
        await self.send(text_data=match_name)
        await self.close(code=1000)

    async def match_found_error(self, event):
        message = event['message']
        await self.send(text_data=message)
        await self.close(code=1000)