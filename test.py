from utils.enums.role import Role
from utils.game_state import GameState
from utils.score_tracker import ScoreTracker
from game_modes.simulation_mode import SimulationMode

# Mock data
score_tracker = ScoreTracker()

game_state = GameState(
    world_size=4,
    game_mode=None,  # placeholder
    player_role=Role.seeker,
    current_round=0,
    score_tracker=score_tracker,
    world_dimension=1
)

# 4x4 payoff matrix from assignment
payoff_matrix = [
    [-1,  1,  1,  1],
    [ 2, -1,  2,  2],
    [ 1,  1, -3,  1],
    [ 2,  2,  2, -1]
]

# Equal probabilities for 4 locations
probabilities = [0.25, 0.25, 0.25, 0.25]

sim = SimulationMode(game_state, probabilities, payoff_matrix)
sim.start_game()

results = sim.show_results()
print(results)