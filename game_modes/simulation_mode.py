import random

from game_modes.mode import GameMode
from utils.enums.role import Role
from utils.game_state import GameState


class SimulationMode(GameMode):
    def __init__(self,game_state:GameState,probabilities,payoff_matrix) :
        self.game_state = game_state
        self.probabilities = probabilities
        self.payoff_matrix = payoff_matrix


    def play_round(self):
        bot_role=self.game_state.player_role

        bot_move=random.randint(0,self.game_state.worldSize-1)
        computer_move=random.choices(range(self.game_state.worldSize),self.probabilities,k=1)[0]

        if bot_role==Role.hider:
            self.game_state.score_tracker.update_score(self.payoff_matrix[bot_move][computer_move], bot_role)
        else:
            self.game_state.score_tracker.update_score(self.payoff_matrix[computer_move][bot_move],bot_role)

    def start_game(self) :
        self.reset_game()
        for _ in range(100):
            self.play_round()

    def reset_game(self) :
        self.game_state.reset_game_state()

    def show_results(self)-> dict[str,int] :
        results = dict()
        results["bot_score"],results["computer_score"] = self.game_state.score_tracker.get_score()
        results["bot_rounds_won"],results["computer_rounds_won"] = self.game_state.score_tracker.get_rounds_won()
        return results



