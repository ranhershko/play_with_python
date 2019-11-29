import random
from time import sleep

# the correct way is to use inheritence from a generic game class
class MemoryGame():
    def __init__(self, difficulty):
        self._difficulty = difficulty
        self._secret_list = random.sample(range(1, 101), self._difficulty)

    def generate_sequence(self):
        print(f'{self._secret_list}', end="")
        sleep(1)
        print('                                \r', end="")

    def get_list_from_user(self):
        print(f"Try to guess from memory ", end="")
        print("the number you " if self._difficulty == 1 else f"the {self._difficulty} numbers list you ", end="")
        print(f"currently saw", end="")
        print(" - please enter comma separated values list: " if self._difficulty > 1 else "")
        secret_list = input().split(',')
        # very hard to read and follow
        # try avoiding large one liners, make the code short, with spaces, lines...
        while len(set([num for num in secret_list if num.isdigit()])) != self._difficulty:
            secret_list = input(f"The input {[num for num in secret_list]} you enter are not as request - try again: ")\
                .split(',')
        secret_list = [int(num) for num in secret_list]
        return secret_list

    def play(self):
        self.generate_sequence()
        return len(set(self._secret_list)) == len((set([num for num in self.get_list_from_user()]))
                                                  .intersection(set(self._secret_list)))
