from engine.game_engine import GameEngine
from utils.enums.game_mode import GameModeType
from utils.enums.role import Role

engine = GameEngine(
    world_size=4,
    world_dimension=1,
    player_role=Role.seeker,
    game_mode_type=GameModeType.interactive
)

setup = engine.initialize_game()

print("Probabilities:", setup.probabilities)
print("Player role:", setup.game_state.player_role)
print("Game mode:", setup.game_state.game_mode)

# Run simulation
setup.mode.start_game()
for i in range(5):
    setup.mode.play_round(player_position=2)

results = setup.mode.show_results()
print("Results:", results)