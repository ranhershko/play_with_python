from GuessGame import GuessGames
from MemoryGame import MemoryGame
from CurrencyRouletteGame import CurrencyRouletteGame
from Score import Score
import run_score


run_program = True

# Super ugly :)
# use argparse python module
options = "Memory Game - a sequence of numbers will appear for 1 second and you have to guess it back,\
Guess Game - guess a number and see if you chose like the computer,Currency Roulette - try and guess the \
value of a random amount of USD in ILS,Quit".split(',')


def welcome(name):
    return f"Hello {name} and welcome to the World of Games (WoG).\nHere you can find many cool games to play."


# The best practice to implement this method is to create a factory class.
# in python (and in general) factory classes are there to make a generic interface for different kind of related-classes
# the most classic example is cloud utils class, that can be a factory class to initialize either AWS utils or GCP utils, etc
# the benefit it gives that the user that uses your code dont need to do this hard logic of ifs-thens... he just initializes
# the factory class with the type of the cloud and thats it.

# also, for that you will need to use real class inheritence and you dont use it in this code
def selected_game(game_num, difficulty):
    global run_program # this is not required, in python if you define it outside any method scope it will work
    game = object() # You dont need to predefine params in python. just game = MemoryGame is enough
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
            current_score = Score(difficulty)
            current_score.add_score()

        else:
            print("You lose")     # USD = 3.51

    elif game_num == 4:
        print("Goodbye, Check your score in http://localhost (Press CTRL+C to quit)")
        run_score.on_web()
        run_program = False
    return run_program


def load_game():
    global run_program
    while run_program:
        print(f"Please choose a game to play: [1-{len(options)}]")
        for index, option in enumerate(options):
            print(f"{index + 1}. {option}")
        try:
            choice = input("Your choice: ") # here you could set the choice to be already int and not transform it each time
            if not choice.isdigit() or int(choice) not in list(range(1, len(options) + 1)):
                raise ValueError(f"{str(choice)}: Incorrect option, try again: ") # nice for using f strings.. its python 3.7 right?
            else:
                if int(choice) == 4:
                    difficulty = 0
                else:
                    difficulty = input('Please choose game difficulty from 1 to 5: ')
                    while not difficulty.isdigit() or not (1 <= int(difficulty) <= 5):
                        difficulty = input(f"{difficulty} isn't a number or isn't between 1 to 5 \
                                            - Please choose game difficulty from 1 to 5: ")
                run_program = selected_game(int(choice), int(difficulty))
        except KeyboardInterrupt: # But what if i really want to exit the game? i cant until i finish it? since you catch my ctrl-c
            run_program = selected_game(4, 0)
        except ValueError as ve:
            print(ve) # if you want to print real app errors, we use logger module for that. there you can set sevirity level

