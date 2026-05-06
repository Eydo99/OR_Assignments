import sys
import random
from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow
from ui.theme import global_stylesheet
from ui.pages.setup_page import SetupPage
from ui.pages.war_room_page import WarRoomPage

from utils.enums.role import Role
from utils.enums.game_mode import GameModeType
from utils.game_state import GameState
from utils.score_tracker import ScoreTracker
from game_modes.interactive_mode import InteractiveMode
from game_modes.simulation_mode import SimulationMode


ALL_TYPES = ["F", "C", "B", "M", "V", "R"]
TYPE_TO_NAME = {
    "F": "Forest", "C": "Cave", "B": "Beach",
    "M": "Mountain", "V": "Valley", "R": "River",
}


def _generate_demo_world(n: int, dimension: int):
    """Generate random place types/names and a payoff matrix for demo."""
    if dimension == 2:
        total = n * n
    else:
        total = n

    types = [random.choice(ALL_TYPES) for _ in range(total)]
    names = [TYPE_TO_NAME[t] for t in types]

    matrix = [[random.randint(-5, 5) for _ in range(total)] for _ in range(total)]
    for i in range(total):
        matrix[i][i] = 0

    raw = [random.uniform(1, 40) for _ in range(total)]
    total_raw = sum(raw)
    probs = [(names[i], (raw[i] / total_raw) * 100) for i in range(total)]

    return types, names, matrix, probs


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(global_stylesheet())

    window = MainWindow()
    setup_page = SetupPage(window)
    war_room_page = WarRoomPage(window)

    def on_setup_complete(n: int, role: str, mode: str, dimension: int):
        types, names, matrix, probs = _generate_demo_world(n, dimension)

        grid_k = n if dimension == 2 else None
        war_room_page.initialize_world(types, names, grid_size=grid_k, role=role, mode=mode)
        war_room_page.update_matrix(matrix, names)
        war_room_page.update_probabilities(probs)
        war_room_page.update_stats(
            status="Converged", iterations="1000",
            game_value=f"{random.uniform(-3, 3):.2f}",
            runtime=f"{random.uniform(1, 50):.1f}ms"
        )
        
        score_tracker = ScoreTracker()
        player_role = Role.hider if role == "Hider" else Role.seeker
        game_mode_enum = GameModeType.interactive if mode == "Interactive" else GameModeType.simulation
        
        game_state = GameState(
            world_size=n,
            world_dimension=dimension,
            game_mode=game_mode_enum,
            player_role=player_role,
            current_round=1,
            score_tracker=score_tracker
        )
        
        raw_probs = [p[1] / 100.0 for p in probs]
        
        if mode == "Interactive":
            window.active_game = InteractiveMode(game_state, raw_probs, matrix)
            window.active_game.start_game()
            war_room_page.update_scores(0.0, 0.0)
            war_room_page.update_rounds_won(0, 0)
            war_room_page.set_round(1)
        else:
            window.active_game = SimulationMode(game_state, raw_probs, matrix)
            window.active_game.start_game()
            st = window.active_game.game_state.score_tracker
            p_score, c_score = st.get_score()
            p_won, c_won = st.get_rounds_won()
            war_room_page.update_scores(p_score, c_score)
            war_room_page.update_rounds_won(p_won, c_won)
            war_room_page.set_round(window.active_game.game_state.current_round)

        dim_label = f"{n}×{n} 2D grid" if dimension == 2 else f"{n}-place 1D strip"
        war_room_page.log_event(f"World generated: {dim_label}")
        war_room_page.log_event(f"Role: {role} · Mode: {mode}")
        war_room_page.log_event("Matrix computed — click a place to play!")

        window.go_to_war_room()

    setup_page.setup_complete.connect(on_setup_complete)

    def on_reset():
        if hasattr(window, "active_game"):
            window.active_game.reset_game()
        war_room_page.reset()
        
    war_room_page.reset_requested.connect(on_reset)

    def on_place_clicked(idx):
        if not hasattr(window, "active_game"): return
        game = window.active_game
        if game.game_state.game_mode == GameModeType.simulation:
            war_room_page.log_event("Simulation mode already finished.")
            return

        dim = game.game_state.world_dimension
        n_size = game.game_state.world_size
        pos = divmod(idx, n_size) if dim == 2 else idx

        war_room_page.log_event(f"→ Place {idx} click registered")
        game.play_round(pos)
        
        st = game.game_state.score_tracker
        p_score, c_score = st.get_score()
        war_room_page.update_scores(p_score, c_score)
        p_won, c_won = st.get_rounds_won()
        war_room_page.update_rounds_won(p_won, c_won)
        war_room_page.set_round(game.game_state.current_round)

    war_room_page.place_clicked.connect(on_place_clicked)

    window.set_pages(setup_page, war_room_page)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()