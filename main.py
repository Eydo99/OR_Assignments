import sys
import time
from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow
from ui.theme import global_stylesheet
from ui.pages.setup_page import SetupPage
from ui.pages.war_room_page import WarRoomPage

from engine.game_engine import GameEngine
from utils.enums.role import Role
from utils.enums.game_mode import GameModeType


# ── Place-type helpers ────────────────────────────────────────────────────────

_PLACE_TYPE_NAMES = {
    "Easy": ("B", [
        "Corniche", "Stanly Bridge", "Gleem Bay", "Montaza", "Qaitbay",
        "Bibliotheca", "Mamoura", "Sporting Club", "Sidi Gaber", "Mahatet Raml",
        "Antoniades", "Shallalat", "Fouad Street", "San Stefano", "Miami",
        "Mandara", "Smouha", "Green Plaza", "Tivoli Dome", "Carrefour"
    ]),
    "Neutral": ("V", [
        "Camp Caesar", "Cleopatra", "Loran", "Rushdi", "Kafr Abdou",
        "Ibrahimiya", "Shatby", "Moharam Bek", "Fleming", "Bacos",
        "Victoria", "Zizinia", "Bolkly", "Moustafa Kamel", "Gianaclis",
        "Saba Pasha", "Schutz", "Smouha", "San Saba", "El Iqubal"
    ]),
    "Hard": ("F", [
        "Zan'et ElSetaat", "Manshia", "Attarine", "Karmouz", "Mina ElBasal",
        "Kom ElShoqafa", "El Labban", "Wardian", "Dekheila", "El Max",
        "AbuQir", "El Awayed", "El Hadara", "Souq El Gom3a", "El Sa3a",
        "Asafra", "Agami", "Amriya", "Borg El Arab", "Abu Suleiman"
    ])

}


def _world_to_ui_lists(world):
    """Flatten a World (list[list[Place]]) into (place_types, place_names) with unique names."""
    place_types: list[str] = []
    place_names: list[str] = []
    
    # Count how many of each type we've used
    type_counters = {"Easy": 0, "Neutral": 0, "Hard": 0}
    
    for row in world:
        for place in row:
            place_type_value = place.place_type.value
            code, name_list = _PLACE_TYPE_NAMES.get(place_type_value, ("V", ["Valley"]))
            
            # Get unique name by cycling through the list
            name_index = type_counters[place_type_value] % len(name_list)
            name = name_list[name_index]
            type_counters[place_type_value] += 1
            
            place_types.append(code)
            place_names.append(name)
    
    return place_types, place_names


def _payoff_to_list(matrix) -> list[list[int]]:
    """Convert numpy ndarray to nested list of ints."""
    return [[int(matrix[r][c]) for c in range(matrix.shape[1])]
            for r in range(matrix.shape[0])]


def _probs_to_ui(probs, place_names: list[str]) -> list[tuple[str, float]]:
    """Raw probability list → list of (name, percent) for UI bars/heatmap."""
    total = sum(probs) or 1.0
    return [(place_names[i], (probs[i] / total) * 100) for i in range(len(probs))]


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(global_stylesheet())

    window     = MainWindow()
    setup_page = SetupPage(window)
    war_room   = WarRoomPage(window)

    # ── Setup complete → initialise real backend, populate War Room ───────────
    def on_setup_complete(n: int, role: str, mode: str, dimension: int):
        player_role = Role.hider  if role == "Hider" else Role.seeker
        game_mode_enum = (GameModeType.interactive if mode == "Interactive"
                          else GameModeType.simulation)

        war_room.log_event("Initialising engine …")

        # ── Real backend call ─────────────────────────────────────────────────
        t0 = time.perf_counter()
        engine = GameEngine(
            world_size      = n,
            world_dimension = dimension,
            player_role     = player_role,
            game_mode_type  = game_mode_enum,
        )
        try:
            setup = engine.initialize_game()
        except Exception as exc:
            war_room.log_event(f"⚠ Engine error: {exc}")
            window.go_to_war_room()
            return
        elapsed_ms = (time.perf_counter() - t0) * 1000

        # Store handles for later callbacks
        window.active_game  = setup.mode
        window.active_setup = setup

        # ── Derive UI data from real World ────────────────────────────────────
        place_types, place_names = _world_to_ui_lists(setup.world)
        payoff_list = _payoff_to_list(setup.payoff_matrix)
        probs_ui    = _probs_to_ui(setup.probabilities, place_names)

        # ── Populate War Room UI ──────────────────────────────────────────────
        grid_k = n if dimension == 2 else None
        war_room.initialize_world(place_types, place_names,
                                  grid_size=grid_k, role=role, mode=mode)
        war_room.update_matrix(payoff_list, place_names)
        war_room.update_probabilities(probs_ui)
        war_room.update_stats(
            status     = setup.solver_status,
            iterations = f"{setup.iteration_count} ({setup.solver_method})",
            game_value = f"{setup.game_value:.3f}",
            runtime    = f"{elapsed_ms:.1f} ms",
        )

        # ── Start game mode ───────────────────────────────────────────────────
        setup.mode.start_game()

        if game_mode_enum == GameModeType.simulation:
            # start_game() already played 100 rounds
            st = setup.mode.game_state.score_tracker
            p_score, c_score = st.get_score()
            p_won,   c_won   = st.get_rounds_won()
            war_room.update_scores(p_score, c_score)
            war_room.update_rounds_won(p_won, c_won)
            war_room.set_round(setup.mode.game_state.current_round)
            war_room.log_event("Simulation complete — 100 rounds auto-played")
        else:
            war_room.update_scores(0.0, 0.0)
            war_room.update_rounds_won(0, 0)
            war_room.set_round(1)

        dim_label = f"{n}×{n} 2D grid" if dimension == 2 else f"{n}-place 1D strip"
        war_room.log_event(f"World: {dim_label} · solved in {elapsed_ms:.1f} ms")
        war_room.log_event("Nash equilibrium strategy computed ✓")
        if game_mode_enum == GameModeType.interactive:
            war_room.log_event("Click a place to play your round!")

        window.go_to_war_room()

    setup_page.setup_complete.connect(on_setup_complete)

    # ── Reset ─────────────────────────────────────────────────────────────────
    def on_reset():
        if hasattr(window, "active_game"):
            window.active_game.reset_game()
        war_room.reset()
        war_room.log_event("Game reset — ready for a new round")

    war_room.reset_requested.connect(on_reset)

    # ── Place clicked (Interactive mode only) ─────────────────────────────────
    def on_place_clicked(idx: int):
        if not hasattr(window, "active_game") or not hasattr(window, "active_setup"):
            return

        game = window.active_game
        setup = window.active_setup

        if game.game_state.game_mode == GameModeType.simulation:
            war_room.log_event("Simulation already finished — press Reset to replay.")
            return

        dim    = game.game_state.world_dimension
        n_size = game.game_state.world_size
        pos    = divmod(idx, n_size) if dim == 2 else idx

        prev_round = game.game_state.current_round
        
        # Play round and get computer's position
        computer_idx = game.play_round(pos)

        st = game.game_state.score_tracker
        p_score, c_score = st.get_score()
        p_won,   c_won   = st.get_rounds_won()

        war_room.update_scores(p_score, c_score)
        war_room.update_rounds_won(p_won, c_won)
        war_room.set_round(game.game_state.current_round)
        
        # Show where the opponent played
        place_types, place_names = _world_to_ui_lists(setup.world)
        if 0 <= computer_idx < len(place_names):
            war_room.show_opponent_move(place_names[computer_idx], computer_idx)
            war_room.log_event(
                f"Round {prev_round + 1} · You: {p_score:.1f}  Opp: {c_score:.1f} · "
                f"Opponent chose {place_names[computer_idx]}"
            )
        else:
            war_room.log_event(
                f"Round {prev_round + 1} · You: {p_score:.1f}  Opp: {c_score:.1f}"
            )

    war_room.place_clicked.connect(on_place_clicked)

    # ── Launch ────────────────────────────────────────────────────────────────
    window.set_pages(setup_page, war_room)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()