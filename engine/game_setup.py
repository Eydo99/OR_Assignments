from dataclasses import dataclass

from game_modes.base_mode import BaseMode
from utils.game_state import GameState


@dataclass
class GameSetup:
    probabilities: list
    game_state: GameState
    mode: BaseMode