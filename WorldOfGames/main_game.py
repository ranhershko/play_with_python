from live import load_game, welcome

# your entire code is missing docstrings, method/class/login documnetation.
# class inheritance:
# The correct way you should have done it:
"""
from abc import abstractmethod, ABCMeta
import random
class Game(metaclass=ABCMeta):
    def __init__(self, difficulty):
        self.difficulty = difficulty


    # this is absract since each game class has different logic. if the logic was simply "start playing" you should have put it here
    @abstractmethod
    def game(self):
        '''
        start a game.
        :return: 
        '''
        pass

class MemoryGame(Game)
    def __init__(self):
        super().__init__(self)
        self._secret_list = random.sample(range(1, 101), self.difficulty)

    def game(self):
        '''game logic'''
        
    # other methods related only to this game but not other games
"""


def main():
    print(welcome("Danny"))
    load_game()


if __name__ == '__main__':
    main()