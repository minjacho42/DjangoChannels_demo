import asyncio
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .Game import Game
import logging
import urllib.parse

game_dict = {}

logger = logging.getLogger('transendence')

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # 쿼리 문자열을 파싱하여 match_name과 id를 가져오기
        query_string = self.scope['query_string'].decode('utf-8')
        query_params = urllib.parse.parse_qs(query_string)

        # match_name과 id 추출
        match_name = query_params.get('match_name', [None])[0]
        user_id = query_params.get('id', [None])[0]
        if match_name and user_id:
            self.match_group_name = f'game_{match_name}'
            self.user_id = user_id
            await self.channel_layer.group_add(
                self.match_group_name, self.channel_name
            )
        else:
            await self.close()
            return
        logger.debug(f'{self.match_group_name} connected')
        self.game_player_num = 0
        if self.match_group_name not in game_dict:
            logger.debug("GameDict Created")
            game_dict[self.match_group_name] = Game(self.match_group_name)
            self.game = game_dict[self.match_group_name]
            self.game_player_num = 1
            asyncio.create_task(self.game.start())
        elif not game_dict[self.match_group_name].player_is_full:
            logger.debug("GameDict Joined")
            self.game = game_dict[self.match_group_name]
            self.game_player_num = 2
            self.game.player_is_full = True
        else:
            await self.close(1000)
        await self.accept()

    async def disconnect(self, close_code):
        # 게임 방에서 나가기
        self.game.cancel_ready(self.game_player_num)
        await self.channel_layer.group_discard(
            self.match_group_name,
            self.channel_name
        )
        logger.debug(f'Player{self.game_player_num} Disconnected')
        if not game_dict[self.match_group_name].is_started:
            logger.debug("GameDict Disconnected")
            game_dict.pop(self.match_group_name)

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        msg_type = text_data_json['type']
        if msg_type == 'ready':
            self.game.ready(self.game_player_num)
        elif msg_type == 'update':
            self.game.update(self.game_player_num, text_data_json['key'])

    # async def handle_msg(self, text_data):
    #     # logger.debug(f'input received: {text_data}')
    #     text_data_json = json.loads(text_data)
    #     msg_type = text_data_json['type']
    #     if msg_type == 'ready':
    #         game_dict[self.match_group_name].ready(self.game_player_num)
    #     elif msg_type == 'update':
    #         game_dict[self.match_group_name].update(self.game_player_num, text_data_json['key'])

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