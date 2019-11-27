from pathlib import Path
import Utils
from os import getcwd


def score_server():
    my_path = getcwd()
    score_file = Path(Utils.SCORES_FILE_NAME)
    if not score_file.exists():
        jinja2_file_serv = 'error.jinja2'
        score_answer = f"the {Utils.SCORES_FILE_NAME} file doesn't exists"
    else:
        score_f = open(Utils.SCORES_FILE_NAME, 'r', encoding='utf-8')
        try:
            line1 = score_f.read()
            score_answer = line1.strip()
            if score_answer.isdigit():
                jinja2_file_serv = 'score.jinja2'
            else:
                jinja2_file_serv = 'error.jinja2'
                score_answer = f"The score value [{score_answer}] in {Utils.SCORES_FILE_NAME} file isn't a number"
        except:
            jinja2_file_serv = my_path + '\\templates\\' + 'error.jinja2'
            score_answer = f'Something went wrong when reading the {Utils.SCORES_FILE_NAME} file'
        finally:
            score_f.close()
    return jinja2_file_serv, score_answer

