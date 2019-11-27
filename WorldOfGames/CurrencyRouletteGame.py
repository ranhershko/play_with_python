import requests
import random


class CurrencyRouletteGame():
    def __init__(self,difficulty):
        self._difficulty = difficulty
        self._usd_amount = random.randint(1, 100)

    def get_money_interval(self):
        usd_value = requests.get(
            f"https://api.exchangeratesapi.io/latest?base=USD&symbols=ILS").json()['rates']['ILS'] #['ILS']
        return self._usd_amount * usd_value - (5 - self._difficulty), self._usd_amount * usd_value + (
                5 - self._difficulty)

    def get_guess_from_user(self):
        user_guess = input(f"Try to guess the value of a {self._usd_amount}$ amount in ILS: ")
        number = user_guess.isdigit()
        while not number:
            try:
                user_guess = int(input(f"Your input {user_guess} isn't a number. \
                                       Try to guess the value of {self._usd_amount}$ amount in ILS: "))
            except ValueError:
                print(f"Your input {user_guess} isn't a number.")
                continue
            else:
                break
        return int(user_guess)

    def play(self):
        nis_min, nis_max = self.get_money_interval()
        user_guess = self.get_guess_from_user()
        return nis_min <= user_guess <= nis_max

