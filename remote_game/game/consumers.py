import asyncio
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .Game import Game
import logging

game_dict = {}

logger = logging.getLogger('transendence')

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.match_name = self.scope['url_route']['kwargs']['match_name']
        self.match_group_name = f'game_{self.match_name}'
        await self.channel_layer.group_add(
            self.match_group_name, self.channel_name
        )
        logger.debug(f'{self.match_group_name} connected')
        self.game_player_num = 0
        if self.match_group_name not in game_dict:
            logger.debug("GameDict Created")
            game_dict[self.match_group_name] = Game(self.match_group_name)
            self.game_player_num = 1
            asyncio.create_task(game_dict[self.match_group_name].start())
        else:
            logger.debug("GameDict Joined")
            self.game_player_num = 2
        await self.accept()

    async def disconnect(self, close_code):
        # 게임 방에서 나가기
        game_dict[self.match_group_name].cancel_ready(self.game_player_num)
        await self.channel_layer.group_discard(
            self.match_group_name,
            self.channel_name
        )
        logger.debug(f'Player{self.game_player_num} Disconnected')
        if not game_dict[self.match_group_name].is_started:
            logger.debug("GameDict Disconnected")
            game_dict.pop(self.match_group_name)

    async def receive(self, text_data=None, bytes_data=None):
        asyncio.create_task(self.handle_msg(text_data))

    async def handle_msg(self, text_data):
        text_data_json = json.loads(text_data)
        msg_type = text_data_json['type']
        if msg_type == 'ready':
            game_dict[self.match_group_name].ready(self.game_player_num)
        elif msg_type == 'update':
            game_dict[self.match_group_name].update(self.game_player_num, text_data_json['key'])

    async def game_update(self, event):
        # logger.debug(f'game update: {event}')
        event_json = json.dumps(event['data'])
        # 모든 플레이어에게 게임 상태 업데이트
        await self.send(text_data=event_json)

    async def game_abnormal_finish(self, event):
        logger.debug(f'game abnormal finish: {event}')
        await self.send(text_data=event['data'])

    async def game_finish(self, event):
        logger.debug(f'game finish: {event}')
        await self.send(text_data=event['data'])