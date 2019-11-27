from os import system, name, getcwd

SCORES_FILE = 'Scores.txt'
my_path = getcwd()
SCORES_FILE_NAME = (my_path + '\\' + SCORES_FILE).strip()
BAD_RETURN_CODE = 50


def screen_cleaner():
    console = system
    os_type = name
    if os_type == 'nt':
        console('cls')
    else:
        console('clear')

