from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QGridLayout,
    QProgressBar, QScrollArea, QTextEdit,
    QStackedWidget, QTabWidget
)
from PySide6.QtCore import Qt, Signal

from ui import theme
from ui.theme import difficulty_color, difficulty_label, difficulty_name
from ui.widgets.payoff_matrix_widget import PayoffMatrixWidget
from ui.widgets.world_grid_2d_widget import WorldGrid2DWidget


class WarRoomPage(QWidget):
    place_clicked   = Signal(int)
    reset_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("WarRoomPage")

        self._place_buttons:         list[QPushButton] = []
        self._place_base_styles:     list[str]         = []
        self._prob_bars:             list[tuple]        = []
        self._prob_container_layout: QVBoxLayout | None = None
        self._is_2d:    bool = False
        self._grid_size: int = 0
        self._role:     str  = ""
        self._mode:     str  = ""

        self._build_ui()

    def _build_ui(self):
        main = QHBoxLayout(self)
        main.setContentsMargins(16, 16, 16, 16)
        main.setSpacing(16)

        main.addLayout(self._build_left_column())

        self._content_stack = QStackedWidget()

        page_1d = QWidget()
        page_1d.setStyleSheet("background: transparent;")
        lay_1d = QHBoxLayout(page_1d)
        lay_1d.setContentsMargins(0, 0, 0, 0)
        lay_1d.setSpacing(16)
        lay_1d.addLayout(self._build_1d_mid_column(), stretch=1)
        lay_1d.addLayout(self._build_1d_right_column())
        self._content_stack.addWidget(page_1d)

        page_2d = QWidget()
        page_2d.setStyleSheet("background: transparent;")
        lay_2d = QHBoxLayout(page_2d)
        lay_2d.setContentsMargins(0, 0, 0, 0)
        lay_2d.setSpacing(0)
        lay_2d.addWidget(self._build_2d_tabs(), stretch=1)
        self._content_stack.addWidget(page_2d)

        main.addWidget(self._content_stack, stretch=1)

    def _build_left_column(self) -> QVBoxLayout:
        col = QVBoxLayout()
        col.setSpacing(12)

        self._badge_panel = QFrame()
        self._badge_panel.setFixedWidth(220)
        self._badge_panel.setFixedHeight(80)
        self._badge_panel.setStyleSheet(f"""
            QFrame {{
                background-color: {theme.SURFACE};
                border: 1px solid {theme.BORDER};
                border-radius: 12px;
            }}
        """)
        badge_lay = QVBoxLayout(self._badge_panel)
        badge_lay.setContentsMargins(12, 8, 12, 8)
        badge_lay.setSpacing(2)

        badge_row1 = QHBoxLayout()
        badge_row1.setSpacing(0)
        self._lbl_role_badge = QLabel("🎮  —")
        self._lbl_role_badge.setStyleSheet(
            f"color: {theme.INDIGO}; font-weight: 800; font-size: 12px;"
            f" background: transparent; border: none;"
        )
        self._lbl_mode_badge = QLabel("")
        self._lbl_mode_badge.setStyleSheet(
            f"color: {theme.CYAN}; font-weight: 700; font-size: 10px;"
            f" background: transparent; border: none;"
        )
        badge_row1.addWidget(self._lbl_role_badge)
        badge_row1.addStretch()
        badge_row1.addWidget(self._lbl_mode_badge)

        div = QFrame()
        div.setFrameShape(QFrame.Shape.HLine)
        div.setFixedHeight(1)
        div.setStyleSheet(f"background: {theme.BORDER}; border: none;")

        badge_row2 = QHBoxLayout()
        badge_row2.setSpacing(6)
        lbl_round_caption = QLabel("ROUND")
        lbl_round_caption.setStyleSheet(
            f"color: {theme.MUTED2}; font-size: 9px; font-weight: 800;"
            f" letter-spacing: 2px; background: transparent; border: none;"
        )
        self._lbl_round_num = QLabel("1")
        self._lbl_round_num.setStyleSheet(
            f"color: {theme.AMBER}; font-size: 22px; font-weight: 900;"
            f" background: transparent; border: none;"
        )
        badge_row2.addWidget(lbl_round_caption)
        badge_row2.addWidget(self._lbl_round_num)
        badge_row2.addStretch()

        badge_lay.addLayout(badge_row1)
        badge_lay.addWidget(div)
        badge_lay.addLayout(badge_row2)

        score_panel = QFrame()
        score_panel.setProperty("class", "score-panel")
        score_panel.setFixedWidth(220)
        sl = QVBoxLayout(score_panel)
        sl.setAlignment(Qt.AlignTop)
        sl.setSpacing(6)
        sl.setContentsMargins(14, 12, 14, 12)

        lbl_your = QLabel("YOUR SCORE")
        lbl_your.setAlignment(Qt.AlignCenter)
        lbl_your.setProperty("class", "section-label")

        self.val_your_score = QLabel("0")
        self.val_your_score.setAlignment(Qt.AlignCenter)
        self.val_your_score.setProperty("class", "amber-number")

        your_rounds_row = QHBoxLayout()
        lbl_your_rw = QLabel("Rounds Won:")
        lbl_your_rw.setStyleSheet(
            f"color: {theme.MUTED2}; font-size: 10px; background: transparent;"
        )
        self.val_your_rounds = QLabel("0")
        self.val_your_rounds.setStyleSheet(
            f"color: {theme.AMBER}; font-size: 12px; font-weight: 800;"
            f" background: transparent;"
        )
        your_rounds_row.addWidget(lbl_your_rw)
        your_rounds_row.addStretch()
        your_rounds_row.addWidget(self.val_your_rounds)

        div = QFrame()
        div.setFrameShape(QFrame.Shape.HLine)
        div.setStyleSheet(f"background:{theme.BORDER}; border:none; max-height:1px;")

        lbl_opp = QLabel("OPPONENT SCORE")
        lbl_opp.setAlignment(Qt.AlignCenter)
        lbl_opp.setProperty("class", "section-label")

        self.val_opp_score = QLabel("0")
        self.val_opp_score.setAlignment(Qt.AlignCenter)
        self.val_opp_score.setProperty("class", "cyan-number")

        opp_rounds_row = QHBoxLayout()
        lbl_opp_rw = QLabel("Rounds Won:")
        lbl_opp_rw.setStyleSheet(
            f"color: {theme.MUTED2}; font-size: 10px; background: transparent;"
        )
        self.val_opp_rounds = QLabel("0")
        self.val_opp_rounds.setStyleSheet(
            f"color: {theme.CYAN}; font-size: 12px; font-weight: 800;"
            f" background: transparent;"
        )
        opp_rounds_row.addWidget(lbl_opp_rw)
        opp_rounds_row.addStretch()
        opp_rounds_row.addWidget(self.val_opp_rounds)

        for w in (lbl_your, self.val_your_score):
            sl.addWidget(w)
        sl.addLayout(your_rounds_row)
        sl.addWidget(div)
        for w in (lbl_opp, self.val_opp_score):
            sl.addWidget(w)
        sl.addLayout(opp_rounds_row)

        log_panel = QFrame()
        log_panel.setProperty("class", "score-panel")
        log_panel.setFixedWidth(220)
        ll = QVBoxLayout(log_panel)
        ll.setAlignment(Qt.AlignTop)

        lbl_log = QLabel("EVENT LOG")
        lbl_log.setProperty("class", "section-label")
        ll.addWidget(lbl_log)

        self._event_log = QTextEdit()
        self._event_log.setReadOnly(True)
        self._event_log.setStyleSheet(f"""
            QTextEdit {{
                background: transparent; border: none;
                color: {theme.MUTED};
                font-family: "{theme.FONT_MONO}";
                font-size: {theme.FONT_SM}px;
            }}
        """)
        ll.addWidget(self._event_log, stretch=1)

        self._btn_reset = QPushButton("↺  RESET GAME")
        self._btn_reset.setFixedWidth(220)
        self._btn_reset.setFixedHeight(42)
        self._btn_reset.setCursor(Qt.PointingHandCursor)
        self._btn_reset.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                color: {theme.RED};
                border: 1.5px solid {theme.RED};
                border-radius: 10px;
                font-size: {theme.FONT_SM}px;
                letter-spacing: 1px;
            }}
            QPushButton:hover  {{ background: rgba(244,63,94,0.12); }}
            QPushButton:pressed {{ background: rgba(244,63,94,0.25); }}
        """)
        self._btn_reset.clicked.connect(self.reset_requested.emit)

        col.addWidget(self._badge_panel)
        col.addWidget(score_panel)
        col.addWidget(log_panel, stretch=1)
        col.addWidget(self._btn_reset)
        return col

    def _build_1d_mid_column(self) -> QVBoxLayout:
        col = QVBoxLayout()
        col.setSpacing(12)

        self._world_panel_1d = QFrame()
        self._world_panel_1d.setProperty("class", "score-panel")
        self._world_panel_1d.setMinimumHeight(140)
        world_lay = QVBoxLayout(self._world_panel_1d)
        world_lay.setSpacing(8)
        world_lay.setContentsMargins(12, 12, 12, 12)

        self._world_title = QLabel("WORLD — ROUND 1")
        self._world_title.setProperty("class", "section-label")
        world_lay.addWidget(self._world_title)

        self._1d_legend = self._build_difficulty_legend()
        world_lay.addWidget(self._1d_legend)

        strip_scroll = QScrollArea()
        strip_scroll.setWidgetResizable(True)
        strip_scroll.setFrameShape(QFrame.Shape.NoFrame)
        strip_scroll.setStyleSheet("background: transparent;")
        strip_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        strip_scroll.setMinimumHeight(72)
        strip_page = QWidget()
        strip_page.setStyleSheet("background: transparent;")
        self._strip_layout = QHBoxLayout(strip_page)
        self._strip_layout.setSpacing(6)
        self._strip_layout.setContentsMargins(0, 4, 0, 4)
        strip_scroll.setWidget(strip_page)

        world_lay.addWidget(strip_scroll, stretch=1)

        self.matrix_widget_1d = PayoffMatrixWidget("PAYOFF MATRIX  (Hider POV)")

        col.addWidget(self._world_panel_1d)
        col.addWidget(self.matrix_widget_1d, stretch=1)
        return col

    def _build_1d_right_column(self) -> QVBoxLayout:
        col = QVBoxLayout()
        col.setSpacing(12)
        col.setContentsMargins(0, 0, 0, 0)

        stats_grid = QGridLayout()
        stats_grid.setSpacing(8)
        self._stat_labels: dict[str, QLabel] = {}

        for title, display, val, row, c in [
            ("STATUS",     "STATUS",        "—", 0, 0),
            ("ITERATIONS", "ITERATIONS",    "—", 0, 1),
            ("GAME VALUE", "GAME VAL (H↑)", "—", 1, 0),
            ("RUNTIME",    "RUNTIME",       "—", 1, 1),
        ]:
            card = QFrame()
            card.setProperty("class", "stat-card")
            card.setFixedSize(135, 82)
            cl = QVBoxLayout(card)
            cl.setAlignment(Qt.AlignCenter)
            cl.setSpacing(2)
            lt = QLabel(display)
            lt.setProperty("class", "section-label")
            lt.setAlignment(Qt.AlignCenter)
            lt.setWordWrap(False)
            lt.setStyleSheet(
                f"color: {theme.MUTED2}; font-size: 9px; font-weight: 800;"
                f" letter-spacing: 1.5px; background: transparent;"
            )
            lv = QLabel(val)
            lv.setProperty("class", "stat-value")
            lv.setAlignment(Qt.AlignCenter)
            cl.addWidget(lt)
            cl.addWidget(lv)
            stats_grid.addWidget(card, row, c)
            self._stat_labels[title] = lv

        strat_panel = QFrame()
        strat_panel.setProperty("class", "score-panel")
        strat_panel.setFixedWidth(290)
        strat_lay = QVBoxLayout(strat_panel)
        strat_lay.setSpacing(8)

        lbl_strat = QLabel("OPTIMAL MIXED STRATEGY")
        lbl_strat.setProperty("class", "section-label")
        strat_lay.addWidget(lbl_strat)

        bar_scroll = QScrollArea()
        bar_scroll.setWidgetResizable(True)
        bar_scroll.setFrameShape(QFrame.Shape.NoFrame)
        bar_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        bar_scroll.setStyleSheet("background: transparent;")

        self._prob_container = QWidget()
        self._prob_container.setStyleSheet("background: transparent;")
        self._prob_container_layout = QVBoxLayout(self._prob_container)
        self._prob_container_layout.setContentsMargins(0, 0, 0, 0)
        self._prob_container_layout.setSpacing(3)
        bar_scroll.setWidget(self._prob_container)

        strat_lay.addWidget(bar_scroll, stretch=1)

        col.addLayout(stats_grid)
        col.addWidget(strat_panel, stretch=1)
        return col

    def _build_2d_tabs(self) -> QTabWidget:
        self._tab_widget = QTabWidget()
        self._tab_widget.setDocumentMode(False)

        play_tab = QWidget()
        play_tab.setStyleSheet("background: transparent;")
        play_lay = QHBoxLayout(play_tab)
        play_lay.setContentsMargins(12, 12, 12, 12)
        play_lay.setSpacing(16)

        self._grid_widget = WorldGrid2DWidget("")
        self._grid_widget.setStyleSheet("background: transparent;")
        self._grid_widget.cell_clicked.connect(self._on_place_clicked)
        play_lay.addWidget(self._grid_widget, stretch=1)

        stats_col = QVBoxLayout()
        stats_col.setSpacing(8)
        stats_col.setContentsMargins(0, 0, 0, 0)
        stats_col.setAlignment(Qt.AlignTop)

        stats_grid_2d = QGridLayout()
        stats_grid_2d.setSpacing(8)
        self._stat_labels: dict[str, QLabel] = {}

        for title, display, val, row, c in [
            ("STATUS",     "STATUS",        "—", 0, 0),
            ("ITERATIONS", "ITERATIONS",    "—", 0, 1),
            ("GAME VALUE", "GAME VAL (H↑)", "—", 1, 0),
            ("RUNTIME",    "RUNTIME",       "—", 1, 1),
        ]:
            card = QFrame()
            card.setProperty("class", "stat-card")
            card.setFixedSize(135, 82)
            cl = QVBoxLayout(card)
            cl.setAlignment(Qt.AlignCenter)
            cl.setSpacing(2)
            lt = QLabel(display)
            lt.setProperty("class", "section-label")
            lt.setAlignment(Qt.AlignCenter)
            lt.setWordWrap(False)
            lt.setStyleSheet(
                f"color: {theme.MUTED2}; font-size: 9px; font-weight: 800;"
                f" letter-spacing: 1.5px; background: transparent;"
            )
            lv = QLabel(val)
            lv.setProperty("class", "stat-value")
            lv.setAlignment(Qt.AlignCenter)
            cl.addWidget(lt)
            cl.addWidget(lv)
            stats_grid_2d.addWidget(card, row, c)
            self._stat_labels[title] = lv

        stats_col.addLayout(stats_grid_2d)
        stats_col.addStretch()
        play_lay.addLayout(stats_col)

        self._tab_widget.addTab(play_tab, "🎮  Play Board")

        analysis_tab = QWidget()
        analysis_tab.setStyleSheet("background: transparent;")
        analysis_lay = QHBoxLayout(analysis_tab)
        analysis_lay.setContentsMargins(12, 12, 12, 12)
        analysis_lay.setSpacing(16)

        self.matrix_widget = PayoffMatrixWidget(
            "PAYOFF MATRIX  (Hider POV)  ·  axes = cell index 0…N²-1"
        )
        analysis_lay.addWidget(self.matrix_widget, stretch=1)

        strat_panel_2d = QFrame()
        strat_panel_2d.setProperty("class", "score-panel")
        strat_panel_2d.setFixedWidth(290)
        strat_lay_2d = QVBoxLayout(strat_panel_2d)
        strat_lay_2d.setSpacing(8)

        lbl_strat_2d = QLabel("OPTIMAL MIXED STRATEGY")
        lbl_strat_2d.setProperty("class", "section-label")
        strat_lay_2d.addWidget(lbl_strat_2d)

        heatmap_scroll = QScrollArea()
        heatmap_scroll.setWidgetResizable(True)
        heatmap_scroll.setFrameShape(QFrame.Shape.NoFrame)
        heatmap_scroll.setStyleSheet("background: transparent;")
        heatmap_scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        self._heatmap_container = QWidget()
        self._heatmap_container.setStyleSheet("background: transparent;")
        self._heatmap_layout = QGridLayout(self._heatmap_container)
        self._heatmap_layout.setSpacing(3)
        self._heatmap_layout.setContentsMargins(0, 0, 0, 0)
        heatmap_scroll.setWidget(self._heatmap_container)

        strat_lay_2d.addWidget(heatmap_scroll, stretch=1)
        analysis_lay.addWidget(strat_panel_2d)

        self._tab_widget.addTab(analysis_tab, "📊  Analysis")

        return self._tab_widget

    def _build_difficulty_legend(self) -> QWidget:
        w = QWidget()
        w.setStyleSheet("background: transparent;")
        lay = QHBoxLayout(w)
        lay.setContentsMargins(0, 0, 0, 4)
        lay.setSpacing(14)
        for diff, color in theme.DIFFICULTY_COLORS.items():
            badge = QLabel(f"▬ {diff}")
            badge.setStyleSheet(
                f"color: {color}; font-size: 10px; font-weight: 700;"
                f" background: transparent; letter-spacing: 1px;"
            )
            lay.addWidget(badge)
        lay.addStretch()
        return w

    def initialize_world(
        self,
        place_types: list[str],
        place_names: list[str],
        grid_size:   int | None = None,
        role:        str        = "",
        mode:        str        = "",
    ):
        self._place_buttons.clear()
        self._place_base_styles.clear()
        self._is_2d     = grid_size is not None
        self._grid_size = grid_size or 0
        self._role      = role
        self._mode      = mode

        role_icon = "🫥" if role == "Hider" else ("🔍" if role == "Seeker" else "")
        self._lbl_role_badge.setText(f"{role_icon}  {role}" if role else "—")
        mode_icon = "⚡" if mode == "Interactive" else ("🤖" if mode == "Simulation" else "")
        self._lbl_mode_badge.setText(f"{mode_icon} {mode}" if mode else "—")

        if self._is_2d:
            self._grid_widget.load_world(grid_size, place_types, place_names)
            self._place_buttons     = self._grid_widget.buttons
            self._place_base_styles = self._grid_widget.base_styles
            self._content_stack.setCurrentIndex(1)
        else:
            self._place_types = place_types
            self._build_1d_strip(place_types, place_names)
            self._content_stack.setCurrentIndex(0)

    def update_matrix(
        self,
        matrix_data: list[list[int]],
        place_names: list[str] | None = None,
    ):
        n = len(matrix_data)
        if self._is_2d:
            gs = self._grid_size
            if gs:
                labels = [f"{i} ({i // gs},{i % gs})" for i in range(n)]
            else:
                labels = [str(i) for i in range(n)]
            self.matrix_widget.load_matrix(matrix_data, labels)
        else:
            if place_names is None:
                place_names = [str(i) for i in range(n)]
            self.matrix_widget_1d.load_matrix(matrix_data, place_names)

    def update_probabilities(self, probs_list: list[tuple[str, float]]):
        if self._is_2d:
            self._update_heatmap(probs_list)
        else:
            self._update_bars(probs_list)

    def update_scores(self, your_score: float, opp_score: float):
        self.val_your_score.setText(f"{your_score:.1f}")
        self.val_opp_score.setText(f"{opp_score:.1f}")

    def update_rounds_won(self, your_rounds: int, opp_rounds: int):
        self.val_your_rounds.setText(str(your_rounds))
        self.val_opp_rounds.setText(str(opp_rounds))

    def update_stats(
        self,
        status:     str = "",
        iterations: str = "",
        game_value: str = "",
        runtime:    str = "",
    ):
        for key, val in {
            "STATUS":     status,
            "ITERATIONS": iterations,
            "GAME VALUE": game_value,
            "RUNTIME":    runtime,
        }.items():
            if val and key in self._stat_labels:
                self._stat_labels[key].setText(val)

    def set_round(self, n: int):
        self._lbl_round_num.setText(str(n))
        if self._is_2d:
            self._grid_widget.set_title(f"2D GRID — ROUND {n}")
        else:
            self._world_title.setText(f"WORLD 1D STRIP — ROUND {n}")

    def log_event(self, message: str):
        self._event_log.append(f"► {message}")
        sb = self._event_log.verticalScrollBar()
        sb.setValue(sb.maximum())

    def highlight_place(self, index: int, color: str | None = None):
        if self._is_2d:
            self._grid_widget.highlight_cell(index, color)
        else:
            if 0 <= index < len(self._place_buttons):
                btn = self._place_buttons[index]
                if color:
                    btn.setStyleSheet(
                        self._place_base_styles[index]
                        + f"\nQPushButton {{ background-color: {color}; }}"
                    )
                else:
                    btn.setStyleSheet(self._place_base_styles[index])

    def reset(self):
        self.update_scores(0.0, 0.0)
        self.update_rounds_won(0, 0)
        self.update_stats(status="—", iterations="—", game_value="—", runtime="—")
        self.set_round(1)
        self._event_log.clear()
        self.update_probabilities([])
        for i in range(len(self._place_buttons)):
            self.highlight_place(i, None)

    def _build_1d_strip(self, place_types: list[str], place_names: list[str]):
        while self._strip_layout.count():
            item = self._strip_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for idx, (ptype, pname) in enumerate(zip(place_types, place_names)):
            diff_col = difficulty_color(ptype)
            diff_lbl = difficulty_label(ptype)
            diff_nm  = difficulty_name(ptype)

            btn = QPushButton(f"{pname}\n{diff_lbl}\n#{idx}")
            base_style = f"""
                QPushButton {{
                    background-color: {theme.SURFACE2};
                    color: {theme.TEXT};
                    border: 1px solid {theme.BORDER};
                    border-bottom: 3px solid {diff_col};
                    border-radius: 10px;
                    font-family: "{theme.FONT_MONO}";
                    font-size: {theme.FONT_SM}px;
                    font-weight: bold;
                    padding: 6px 6px;
                    min-width: 72px;
                    min-height: 30px;
                    text-align: center;
                }}
                QPushButton:hover {{
                    background-color: {theme.HIGHLIGHT};
                    border: 1px solid {diff_col};
                    border-bottom: 3px solid {diff_col};
                }}
                QPushButton:pressed {{ background-color: {diff_col}; }}
            """
            btn.setStyleSheet(base_style)
            btn.setToolTip(
                f"<b style='color:{theme.AMBER};'>{pname}</b><br/>"
                f"Type: {ptype} · Index: {idx}<br/>"
                f"Difficulty: <span style='color:{diff_col};'>{diff_nm}</span>"
            )
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda checked, i=idx: self._on_place_clicked(i))
            self._strip_layout.addWidget(btn)
            self._place_buttons.append(btn)
            self._place_base_styles.append(base_style)

        self._strip_layout.addStretch()

    def _update_bars(self, probs_list: list[tuple[str, float]]):
        self._prob_bars.clear()
        while self._prob_container_layout.count():
            item = self._prob_container_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self._clear_layout(item.layout())

        for name, prob in probs_list:
            row_w = QWidget()
            row_w.setStyleSheet("background: transparent;")
            rl = QVBoxLayout(row_w)
            rl.setContentsMargins(0, 0, 0, 0)
            rl.setSpacing(2)

            top = QHBoxLayout()
            l_name = QLabel(name)
            l_name.setStyleSheet(f"color:{theme.TEXT}; font-size:{theme.FONT_SM}px;")
            l_val = QLabel(f"{prob:.1f}%")
            l_val.setStyleSheet(
                f"color:{theme.CYAN}; font-size:{theme.FONT_SM}px;"
                f'font-family:"{theme.FONT_MONO}";'
            )
            top.addWidget(l_name)
            top.addStretch()
            top.addWidget(l_val)

            prog = QProgressBar()
            prog.setValue(int(prob))
            prog.setTextVisible(False)

            rl.addLayout(top)
            rl.addWidget(prog)
            self._prob_container_layout.addWidget(row_w)
            self._prob_bars.append((l_name, l_val, prog))

        self._prob_container_layout.addStretch()

    def _update_heatmap(self, probs_list: list[tuple[str, float]]):
        while self._heatmap_layout.count():
            item = self._heatmap_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not probs_list:
            return

        gs       = self._grid_size
        max_prob = max(p for _, p in probs_list) or 1.0
        cell_px  = max(38, min(58, 256 // max(gs, 1)))
        font_px  = max(7, min(10, cell_px // 5))

        for idx, (_, prob) in enumerate(probs_list):
            row, col = divmod(idx, gs)
            intensity  = prob / max_prob
            bg         = self._lerp_color(theme.SURFACE2, theme.CYAN, intensity * 0.80)
            text_color = theme.TEXT_DARK if intensity > 0.55 else theme.TEXT

            cell = QLabel(f"({row},{col})\n{prob:.1f}%")
            cell.setAlignment(Qt.AlignCenter)
            cell.setToolTip(
                f"<b>Cell ({row}, {col})</b><br/>"
                f"Index: {idx}<br/>"
                f"Probability: {prob:.2f}%"
            )
            cell.setFixedSize(cell_px, cell_px)
            cell.setStyleSheet(f"""
                QLabel {{
                    background-color: {bg};
                    color: {text_color};
                    border-radius: 5px;
                    font-family: "{theme.FONT_MONO}";
                    font-size: {font_px}px;
                    font-weight: bold;
                    padding: 1px;
                }}
            """)
            self._heatmap_layout.addWidget(cell, row, col)

    def _on_place_clicked(self, index: int):
        if 0 <= index < len(self._place_buttons):
            name = self._place_buttons[index].text().split("\n")[0]
        else:
            name = str(index)
        self.log_event(f"You selected place {index}: {name}")
        self.place_clicked.emit(index)

    @staticmethod
    def _lerp_color(base: str, accent: str, t: float) -> str:
        def parse(h):
            h = h.lstrip("#")
            return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        br, bg_, bb = parse(base)
        ar, ag, ab  = parse(accent)
        t = max(0.0, min(1.0, t))
        return (
            f"#{int(br+(ar-br)*t):02x}"
            f"{int(bg_+(ag-bg_)*t):02x}"
            f"{int(bb+(ab-bb)*t):02x}"
        )

    @staticmethod
    def _clear_layout(layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                WarRoomPage._clear_layout(item.layout())