import asyncio, uuid
from channels.layers import get_channel_layer

class WaitingQueue:
    def __init__(self):
        self.users = set()
        self.running = False
        self.lock = asyncio.Lock()

    async def put(self, user):
        async with self.lock:
            self.users.add(user)

    def is_running(self):
        return self.running

    async def start(self):
        self.running = True
        channel_layer = get_channel_layer()
        while True:
            async with self.lock:
                if len(self.users) >= 2:
                    user1 = self.users.pop()
                    user2 = self.users.pop()
                else:
                    await asyncio.sleep(1)
                    continue
            if user1 == user2:
                await channel_layer.send(user1, {
                    "type": "match_found_error",
                    "message": "Match Found Error. Please refresh"
                })
            else:
                match_name = uuid.uuid4()
                await channel_layer.send(user1, {
                    "type": "match_found",
                    "match_name": f'{match_name}'
                })
                await channel_layer.send(user2, {
                    "type": "match_found",
                    "match_name": f'{match_name}'
                })
            await asyncio.sleep(0.5)

    async def delete_from_queue(self, user):
        async with self.lock:
            self.users.discard(user)
