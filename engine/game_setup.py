from dataclasses import dataclass
import numpy as np

from game_modes.base_mode import BaseMode
from utils.game_state import GameState
from world.world import World


@dataclass
class GameSetup:
    probabilities: list
    game_state: GameState
    mode: BaseMode
    world: World
    payoff_matrix: np.ndarray
    game_value: float
    iteration_count: int
    solver_method: str  # "Simplex" or "2-Phase"
    solver_status: str  # "Optimal", "Infeasible", "Unbounded"