import random
from GuessGame import GuessGames
from MemoryGame import MemoryGame
from CurrencyRouletteGame import CurrencyRouletteGame

run_program = True
options = "Memory Game - a sequence of numbers will appear for 1 second and you have to guess it back,\
Guess Game - guess a number and see if you chose like the computer,Currency Roulette - try and guess the \
value of a random amount of USD in ILS,Quit".split(',')


def welcome(name):
    return f"Hello {name} and welcome to the World of Games (WoG).\nHere you can find many cool games to play."


def selected_game(game_num, difficulty):
    global run_program
    game = object()
    if game_num in [1, 2, 3]:
        if game_num == 1:
            game = MemoryGame(difficulty)
            game.generate_sequence()

        elif game_num == 2:
            game = GuessGames(difficulty)
            game.generate_number()

        elif game_num == 3:
            game = CurrencyRouletteGame(difficulty)

        its_awin = game.play()
        if its_awin:
            print("You win")
        else:
            print("You lose")     # USD = 3.51

    elif game_num == 4:
        print("Goodbye")
        run_program = False
    return run_program


def load_game():
    global run_program
    while run_program:
        print(f"Please choose a game to play: [1-{len(options)}]")
        for index, option in enumerate(options):
            print(f"{index + 1}. {option}")
        try:
            choice = input("Your choice: ")
            if not choice.isdigit() or int(choice) not in list(range(1, len(options) + 1)):
                raise ValueError(f"{str(choice)}: Incorrect option, try again: ")
            else:
                if int(choice) == 4:
                    difficulty = 0
                else:
                    difficulty = input('Please choose game difficulty from 1 to 5: ')
                    while not difficulty.isdigit() or not (1 <= int(difficulty) <= 5):
                        difficulty = input(f"{difficulty} isn't a number or isn't between 1 to 5 \
                                            - Please choose game difficulty from 1 to 5: ")
                run_program = selected_game(int(choice), int(difficulty))
        except KeyboardInterrupt:
            run_program = selected_game(4, 0)
        except ValueError as ve:
            print(ve)

