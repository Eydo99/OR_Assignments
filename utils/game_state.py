from dataclasses import dataclass

from utils.enums.game_mode import GameMode
from utils.enums.role import Role
from utils.score_tracker import ScoreTracker

@dataclass
class GameState:
    world_size:int
    world_dimension:int
    game_mode:GameMode
    player_role:Role
    current_round:int
    score_tracker:ScoreTracker

    def reset_game_state(self) -> None:
        self.current_round = 0
        self.score_tracker.reset()