import numpy as np
from engine.game_setup import GameSetup
from game_modes.interactive_mode import InteractiveMode
from game_modes.simulation_mode import SimulationMode
from utils.enums.game_mode import  GameModeType
from lp.lp_builder import LPBuilder
from lp.payoff_matrix_generator import PayoffMatrix
from simplex.parser import Parser
from simplex.simplex_solver import SimplexSolver
from simplex.tableau_matrix import TableauMatrix
from utils.enums.role import Role
from utils.game_state import GameState
from utils.score_tracker import ScoreTracker
from world.world import World
from world.world_generator import WorldGenerator


class GameEngine:
    def __init__(self, world_size, world_dimension, player_role, game_mode_type,
             easy_win_score=2, neutral_win_score=1, hard_win_score=1,
             easy_lose_score=-3, neutral_lose_score=-1, hard_lose_score=-1):
        self.easy_win_score = easy_win_score
        self.neutral_win_score = neutral_win_score
        self.hard_win_score = hard_win_score
        self.easy_lose_score = easy_lose_score
        self.neutral_lose_score = neutral_lose_score
        self.hard_lose_score = hard_lose_score
        self.player_role = player_role
        self.game_mode_type = game_mode_type
        self.world_dimension = world_dimension
        self.world_size = world_size

    def initialize_game(self)->GameSetup:
        world:World =WorldGenerator(self.world_size,self.world_dimension,self.easy_win_score,self.neutral_win_score
                                    ,self.hard_win_score,self.easy_lose_score,self.neutral_lose_score,
                                    self.hard_lose_score).generate_world()
        payoff_matrix:np.ndarray=PayoffMatrix(world).generate_payoff_matrix()
        computer_role= Role.hider if (self.player_role == Role.seeker) else Role.seeker
        lp_problem_dict=LPBuilder(payoff_matrix,computer_role).build_lp_problem()
        LP_problem=Parser(lp_problem_dict).build_lp_problem()
        tableau_matrix=TableauMatrix(LP_problem)
        tableau_matrix.build_tableau_matrix()
        solution_dict=SimplexSolver(tableau_matrix,LP_problem).solve()
        probabilities=solution_dict['variables'][:-1]
        game_state=GameState(self.world_size,self.world_dimension,self.game_mode_type,self.player_role,0,ScoreTracker())
        game_mode=InteractiveMode(game_state,probabilities,payoff_matrix) if (self.game_mode_type==GameModeType.interactive)\
            else SimulationMode(game_state,probabilities,payoff_matrix)
        return GameSetup(probabilities,game_state,game_mode)




