import requests
import random


# the correct way is to use inheritence from a generic game class
class CurrencyRouletteGame():
    def __init__(self,difficulty):
        self._difficulty = difficulty
        self._usd_amount = random.randint(1, 100)

    def get_money_interval(self):
        usd_value = requests.get(
            f"https://api.exchangeratesapi.io/latest?base=USD&symbols=ILS").json()['rates']['ILS'] #['ILS']
        # i'd move this complex calc to dedicated method or split to few lines. hard to folliw the calcs
        return self._usd_amount * usd_value - (5 - self._difficulty), self._usd_amount * usd_value + (
                5 - self._difficulty)

    def get_guess_from_user(self):
        user_guess = input(f"Try to guess the value of a {self._usd_amount}$ amount in ILS: ") # make it int at this stage
        number = user_guess.isdigit() # as mention below, make you check here.. dont "wait for the last minute" to get an exception
        while not number:
            try:
                user_guess = int(input(f"Your input {user_guess} isn't a number. \
                                       Try to guess the value of {self._usd_amount}$ amount in ILS: "))
            except ValueError: # i dont like it that you allow your app to get to edge case where an exception thrown
                               # simply manage the user input and dont let it get closer to app exception throw
                print(f"Your input {user_guess} isn't a number.")
                continue
            else:
                break
        return int(user_guess)

    def play(self):
        nis_min, nis_max = self.get_money_interval()
        user_guess = self.get_guess_from_user()
        return nis_min <= user_guess <= nis_max

