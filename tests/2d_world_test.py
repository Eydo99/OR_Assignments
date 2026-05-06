from engine.game_engine import GameEngine
from utils.enums.game_mode import GameModeType
from utils.enums.role import Role

engine = GameEngine(
    world_size=4,
    world_dimension=2,
    player_role=Role.hider,
    game_mode_type=GameModeType.simulation
)

setup = engine.initialize_game()
print("Probabilities:", setup.probabilities)
print("Number of probabilities:", len(setup.probabilities))

setup.mode.start_game()
results = setup.mode.show_results()
print("Results:", results)