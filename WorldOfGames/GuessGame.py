import random


class GuessGames():
    def __init__(self, difficulty):
        self._difficulty = difficulty
        self._secret_num = random.randint(1, self._difficulty)

    def generate_number(self):
        return self._secret_num

    def get_guess_from_user(self):
        guess_num = input(f"Guess a number between 1 and {self._difficulty}: ")
        while not guess_num.isdigit() and int(guess_num) not in range(1, self._difficulty):
            guess_num = input(f"{guess_num} isn't a number or it isn't in range - guess again a number between 1 and \
                              {self._difficulty}: ")
        return int(guess_num)

    def play(self):
        return self.get_guess_from_user() == self._secret_num


