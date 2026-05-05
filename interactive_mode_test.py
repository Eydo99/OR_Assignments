from utils.enums.role import Role
from utils.game_state import GameState
from utils.score_tracker import ScoreTracker
from game_modes.interactive_mode import InteractiveMode

# Mock data
score_tracker = ScoreTracker()

game_state = GameState(
    world_size=4,
    game_mode=None,
    player_role=Role.seeker,
    current_round=0,
    score_tracker=score_tracker,
    world_dimension=1
)

payoff_matrix = [
    [-1,  1,  1,  1],
    [ 2, -1,  2,  2],
    [ 1,  1, -3,  1],
    [ 2,  2,  2, -1]
]

probabilities = [0.25, 0.25, 0.25, 0.25]

game = InteractiveMode(game_state, probabilities, payoff_matrix)
game.start_game()

# Simulate 5 rounds with human choosing position 2 each time
for i in range(5):
    game.play_round(player_position=2)
    results = game.show_results()
    print(f"Total rounds: {results.total_rounds}")
    print(f"Player score: {results.player_score}, Computer score: {results.computer_score}")
    print(f"Player rounds won: {results.player_rounds_won}, Computer rounds won: {results.computer_rounds_won}")