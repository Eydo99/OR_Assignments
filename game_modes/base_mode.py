import random
from game_modes.mode import GameMode
from game_modes.simulation_results import SimulationResults
from utils.enums.role import Role
from utils.game_state import GameState
from abc import ABC


class BaseMode(GameMode,ABC):
    def __init__(self, game_state: GameState, probabilities, payoff_matrix):
        self.game_state = game_state
        self.probabilities = probabilities
        self.payoff_matrix = payoff_matrix

    def execute_round(self,player_position):
        world_size = self.game_state.world_size
        world_dimension = self.game_state.world_dimension

        player_role = self.game_state.player_role

        computer_position = 0
        if world_dimension == 1:
            computer_position = random.choices(range(world_size), self.probabilities, k=1)[0]
        else:
            flat_index=random.choices(range(len(self.probabilities)), self.probabilities, k=1)[0]
            computer_position=divmod(flat_index,world_size)

        original_computer_position = computer_position
        original_player_position = player_position
        if world_dimension == 2:
            computer_position = int(computer_position[0] * world_size + computer_position[1])
            player_position = int(player_position[0] * world_size + player_position[1])

        if player_role == Role.hider:
            seeker_score = self.payoff_matrix[computer_position][player_position] * -1
            hider_score = self._proximity_score(self.payoff_matrix[player_position][computer_position], original_player_position,
                                                original_computer_position, world_dimension)
            self.game_state.score_tracker.update_score(hider_score, seeker_score, player_role)
        else:
            seeker_score = self.payoff_matrix[computer_position][player_position] * -1
            hider_score = self._proximity_score(self.payoff_matrix[computer_position][player_position], original_player_position,
                                                original_computer_position, world_dimension)
            self.game_state.score_tracker.update_score(hider_score, seeker_score, player_role)

        self.game_state.current_round += 1


    def reset_game(self) :
        self.game_state.reset_game_state()


    def show_results(self)-> SimulationResults :
        player_score,computer_score=self.game_state.score_tracker.get_score()
        player_rounds_won,computer_rounds_won=self.game_state.score_tracker.get_rounds_won()
        total_rounds=self.game_state.current_round
        return SimulationResults(total_rounds,player_score,computer_score,player_rounds_won,computer_rounds_won)





    def _proximity_score(self,original_score:int,player_position,computer_position,world_dimension:int)->float:
        return self._proximity_score_1d(original_score,player_position,computer_position) if (world_dimension==1) \
            else self._proximity_score_2d(original_score,player_position,computer_position)


    def _proximity_score_1d(self,original_score:int,player_position:int,computer_position:int)->float:
        distance = abs(player_position-computer_position)
        match distance:
            case 1:
                return original_score*0.5
            case 2:
                return original_score*0.75
            case _:
                return original_score

    def _proximity_score_2d(self, original_score: int, player_position: tuple, computer_position: tuple) -> float:
        distance = abs(player_position[0]-computer_position[0])+abs(player_position[1]-computer_position[1])
        match distance:
            case 1:
                return original_score * 0.5
            case 2:
                return original_score * 0.75
            case _:
                return original_score


