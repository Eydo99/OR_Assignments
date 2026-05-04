from utils.enums.role import Role


class ScoreTracker:
    def __init__(self):
        self.player_score = 0
        self.computer_score = 0
        self.player_rounds_won = 0
        self.computer_rounds_won = 0

    def update_score(self, hider_score:float ,seeker_score:int, player_role: Role)->None:
        if player_role==Role.hider:
            self.player_score += hider_score
            self.computer_score += seeker_score
            if hider_score>0:
                self.player_rounds_won += 1
            else:
                self.computer_rounds_won += 1
        else:
            self.computer_score += hider_score
            self.player_score += seeker_score
            if hider_score>0:
                self.computer_rounds_won += 1
            else:
                self.player_rounds_won += 1

    def reset(self):
        self.player_score = 0
        self.computer_score = 0
        self.player_rounds_won = 0
        self.computer_rounds_won = 0

    def get_score(self)-> tuple[int, int]:
        return self.player_score, self.computer_score

    def get_rounds_won(self)-> tuple[int, int]:
        return self.player_rounds_won,self.computer_rounds_won