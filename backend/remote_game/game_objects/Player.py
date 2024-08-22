import logging

logger = logging.getLogger('transendense')

class Player:
    def __init__(self, userid):
        self.__id = userid
        self.__is_ready = False
        self.__score = 0
        self.__is_winner = False
        self.__input = {
            'upPressed' : False,
            'downPressed' : False,
        }

    def get_id(self):
        return self.__id

    def get_is_ready(self):
        return self.__is_ready

    def get_score(self):
        return self.__score

    def get_is_winner(self):
        return self.__is_winner

    def get_input(self):
        return self.__input

    def set_is_ready(self, is_ready):
        self.__is_ready = is_ready

    def increment_score(self):
        self.__score += 1

    def set_winner(self, is_winner):
        self.__is_winner = is_winner

    def set_losser(self, is_winner):
        self.__is_winner = is_winner

    def set_input(self, key_input):
        self.__input = key_input