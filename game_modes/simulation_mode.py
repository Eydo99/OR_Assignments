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
        world_size = self.game_state.world_size
        world_dimension = self.game_state.world_dimension
        bot_role=self.game_state.player_role

        bot_position=random.randint(0, world_size - 1) if(world_dimension==1)\
            else (random.randint(0, world_size - 1),random.randint(0, world_size - 1))


        #TODO:2D computer position after hany finish the 2d probability matrix
        computer_position=random.choices(range(world_size), self.probabilities, k=1)[0]

        if bot_role==Role.hider:
            seeker_score=self.payoff_matrix[bot_position][computer_position]*-1
            hider_score = self._proximity_score(self.payoff_matrix[bot_position][computer_position], bot_position,
                                                computer_position,world_dimension)
            self.game_state.score_tracker.update_score(hider_score,seeker_score, bot_role)
        else:
            seeker_score = self.payoff_matrix[computer_position][bot_position] * -1
            hider_score=self._proximity_score(self.payoff_matrix[computer_position][bot_position], bot_position,
                                              computer_position,world_dimension)
            self.game_state.score_tracker.update_score(hider_score,seeker_score, bot_role)

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

    def _proximity_score(self,original_score:int,bot_position,computer_position,world_dimension:int)->float:
        return self._proximity_score_1d(original_score,bot_position,computer_position) if (world_dimension==1) \
            else self._proximity_score_2d(original_score,bot_position,computer_position)


    def _proximity_score_1d(self,original_score:int,bot_position:int,computer_position:int)->float:
        distance = abs(bot_position-computer_position)
        match distance:
            case 1:
                return original_score*0.5
            case 2:
                return original_score*0.75
            case _:
                return original_score

    def _proximity_score_2d(self, original_score: int, bot_position: tuple, computer_position: tuple) -> float:
        distance = abs(bot_position[0]-computer_position[0])+abs(bot_position[1]-computer_position[1])
        match distance:
            case 1:
                return original_score * 0.5
            case 2:
                return original_score * 0.75
            case _:
                return original_score




