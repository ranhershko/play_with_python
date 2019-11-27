import Utils
from pathlib import Path


class Score:
    def __init__(self, difficulty):
        self.damaged_file = False
        self.user_score_file = Path(Utils.SCORES_FILE_NAME)
        self.difficulty = difficulty
        self.points_of_winning = self.read_score_file()

    def read_score_file(self):
        if self.user_score_file.exists():
            with open(Utils.SCORES_FILE_NAME, "r", encoding='utf-8') as score_file:
                lines = score_file.read().splitlines()
                if len(lines) > 0 and lines[0].strip().isdigit():
                    points_of_winning = int(lines[0].strip())
                else:
                    self.damaged_file = True
                    points_of_winning = 0
        else:
            points_of_winning = 0
            self.write_score_file(update_points=points_of_winning)
        return points_of_winning

    def write_score_file(self, update_points):
        if not self.user_score_file.exists() or self.damaged_file is True or self.points_of_winning != update_points:
            self.points_of_winning = update_points
            with open(Utils.SCORES_FILE_NAME, "w", encoding='utf-8') as score_file:
                score_file.write(str(self.points_of_winning))

    def add_score(self):
        new_score = self.difficulty * 3 + 5 + self.points_of_winning
        self.write_score_file(update_points=new_score)
