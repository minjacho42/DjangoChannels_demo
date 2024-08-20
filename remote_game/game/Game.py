import asyncio
from channels.layers import get_channel_layer
from remote_game.game_objects.Ball import Ball
from remote_game.game_objects.Paddle import Paddle

import logging

logger = logging.getLogger('transendence')

class Game:
    canvas_width = 800
    canvas_height = 600
    def __init__(self, id):
        self.id = id
        self.is_started = False
        self.player1_ready = False
        self.player2_ready = False
        self.player1_score = 0
        self.player2_score = 0
        self.player1_key = {
            'upPressed' : False,
            'downPressed' : False,
        }
        self.player2_key = {
            'upPressed' : False,
            'downPressed' : False,
        }
        self.__ball = Ball((Game.canvas_width - 15) / 2, (Game.canvas_height - 15) / 2)
        self.__left_paddle = Paddle(50, (Game.canvas_height - 100) / 2)
        self.__right_paddle = Paddle(Game.canvas_width - 50 - 10, (Game.canvas_height - 100) / 2)
        self.game_over = False


    async def start(self):
        self.is_started = True
        channel_layer = get_channel_layer()
        while not self.player1_ready or not self.player2_ready:
            await asyncio.sleep(1)
        # logger.debug('All players ready!')
        asyncio.create_task(self.__calculate())
        while self.player1_ready and self.player2_ready:
            await channel_layer.group_send(
                self.id,
                {
                    'type': 'game_update',
                    'data': {
                        'status': 'done' if self.game_over else 'in progress',
                        'player1Score': self.player1_score,
                        'player2Score': self.player2_score,
                        'ball': {
                            'x': self.__ball.x,
                            'y': self.__ball.y,
                        },
                        'paddleL': {
                            'x': self.__left_paddle.x,
                            'y': self.__left_paddle.y,
                        },
                        'paddleR': {
                            'x': self.__right_paddle.x,
                            'y': self.__right_paddle.y,
                        },
                    },
                }
            )
            if self.game_over:
                break
            await asyncio.sleep(1/30)
        if not self.game_over: # 게임 비정상 종료
            await channel_layer.group_send(
                self.id,
                {
                    'type': 'game_abnormal_finish',
                    'data' : 'Player Exited'
                }
            )
        else:
            await channel_layer.group_send(
                self.id,
                {
                    'type': 'game_finish',
                    'data' : 'Game Over'
                }
            )
        self.is_started = False

    def ready(self, player_num):
        if player_num == 1:
            self.player1_ready = True
        elif player_num == 2:
            self.player2_ready = True

    def cancel_ready(self, player_num):
        # logger.debug(f'player{player_num} cancel ready')
        if player_num == 1:
            self.player1_ready = False
        if player_num == 2:
            self.player2_ready = False

    def update(self, player_num, event):
        # logger.info(f'{player_num} {event}')
        if player_num == 1:
            self.player1_key['upPressed'] = event.get('upPressed')
            self.player1_key['downPressed'] = event.get('downPressed')
        if player_num == 2:
            self.player2_key['upPressed'] = event.get('upPressed')
            self.player2_key['downPressed'] = event.get('downPressed')
        # logger.info(f'{1} {self.player1_key}')
        # logger.info(f'{2} {self.player2_key}')

    def is_started(self):
        return self.is_started

    async def __calculate(self):
        while not self.game_over and self.player1_ready and self.player2_ready:
            await asyncio.sleep(1/60)
            if self.player1_key['upPressed']:
                self.__left_paddle.dy = min(-Paddle.vInit, self.__left_paddle.dy - self.__left_paddle.accel)
            if self.player1_key['downPressed']:
                self.__left_paddle.dy = max(Paddle.vInit, self.__left_paddle.dy + self.__left_paddle.accel)
            if not self.player1_key['upPressed'] and not self.player1_key['downPressed']:
                self.__left_paddle.dy = 0
            if self.player2_key['upPressed']:
                self.__right_paddle.dy = min(-Paddle.vInit, self.__right_paddle.dy - self.__right_paddle.accel)
            if self.player2_key['downPressed']:
                self.__right_paddle.dy = max(Paddle.vInit, self.__right_paddle.dy + self.__right_paddle.accel)
            if not self.player2_key['upPressed'] and not self.player2_key['downPressed']:
                self.__right_paddle.dy = 0

            self.__left_paddle.move(self.canvas_height)
            self.__right_paddle.move(self.canvas_height)

            self.__ball.move(Game.canvas_height, self.__left_paddle, self.__right_paddle)

            if self.__ball.x < -50:
                self.player2_score += 1
                self.__ball.reset((Game.canvas_width - 15) / 2, (Game.canvas_height - 15) / 2, 'R')
            elif self.__ball.x > Game.canvas_width + 50:
                self.player1_score += 1
                self.__ball.reset((Game.canvas_width - 15) / 2, (Game.canvas_height - 15) / 2, 'L')\

            if self.player1_score >= 5 or self.player2_score >= 5:
                self.game_over = True