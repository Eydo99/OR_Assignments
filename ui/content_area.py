from PySide6.QtWidgets import QWidget, QVBoxLayout, QStackedWidget
from PySide6.QtGui import QColor

from ui.pages.problem_setup_page import ProblemSetupPage
from ui.pages.coefficients_page import CoefficientsPage
from ui.pages.solution_page import SolutionPage
from ui.pages.tableau_steps_page import TableauStepsPage
from core.simplex_solver import SimplexSolver


class ContentArea(QWidget):
    """Central area that hosts a QStackedWidget with the four section pages."""

    def __init__(self):
        super().__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor("#111827"))
        self.setPalette(palette)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.stack = QStackedWidget()
        self.stack.setObjectName("TransparentWidget")
        layout.addWidget(self.stack)

        # ── Pages ──
        self.problem_setup = ProblemSetupPage()
        self.coefficients = CoefficientsPage()
        self.solution = SolutionPage()
        self.tableau_steps = TableauStepsPage()

        self.stack.addWidget(self.problem_setup)      # index 0
        self.stack.addWidget(self.coefficients)        # index 1
        self.stack.addWidget(self.solution)            # index 2
        self.stack.addWidget(self.tableau_steps)       # index 3

        # ── Wire variable / constraint changes → coefficients page ──
        self.problem_setup.variables_changed.connect(self._rebuild_coefficients)
        self.problem_setup.constraints_changed.connect(self._rebuild_coefficients_constraints)

        # ── Wire coefficients changes → tableau preview live update ──
        self.coefficients.data_changed.connect(self.problem_setup.update_preview_data)

        # ── Wire reset across pages ──
        self.problem_setup.reset_requested.connect(self._on_reset)

        # ── Wire solve (stub – prints data dict) ──
        self.problem_setup.solve_requested.connect(self._on_solve)

    # ── Public API ──
    def set_page(self, index: int):
        if 0 <= index < self.stack.count():
            self.stack.setCurrentIndex(index)

    # ── Internal slots ──
    def _rebuild_coefficients(self, num_vars):
        self.coefficients.rebuild(
            num_vars,
            self.problem_setup.get_num_constraints(),
        )

    def _rebuild_coefficients_constraints(self, num_constraints):
        self.coefficients.rebuild(
            self.problem_setup.get_num_variables(),
            num_constraints,
        )

    def _on_reset(self):
        self.coefficients.reset()
        self.solution.reset()
        self.tableau_steps.reset()

    def _on_solve(self):
        """Pass data to the core Parser and TableauMatrix to verify integration."""
        coeff_data = self.coefficients.get_data()
        data = {
            "obj_fn_type": self.problem_setup.get_objective_type(),
            "obj_fn_values": coeff_data["obj_fn_values"],
            "constraints": coeff_data["constraints"],
            "restrictions": self.problem_setup.get_restrictions(),
        }
        
        print("─" * 50)
        print("SOLVE requested with data:")
        for k, v in data.items():
            print(f"  {k}: {v}")
            
        print("\n--- CORE SOLVER LOGIC OUTPUT ---")
        try:
            from core.parser import Parser
            from core.tableau_matrix import TableauMatrix
            import numpy as np
            
            # 1. Parse UI data into LPProblem
            parser = Parser(data)
            lp_problem = parser.build_lp_problem()
            
            # 2. Build initial TableauMatrix
            tm = TableauMatrix(lp_problem)
            tm.build_tableau_matrix()
            
            print("Initial Basis Indices:", tm.initial_basis)
            print("Artificial Columns:", tm.artificial_cols)
            print("\nInitial Tableau Matrix:")
            np.set_printoptions(suppress=True, formatter={'float_kind': lambda x: f"{x:.2f}"})
            print(np.round(tm.tableau_matrix, 2))

            solver = SimplexSolver(tm, lp_problem)
            result = solver.solve()
            print("Result:", solver.result)
            print("Solution:", result)
            self.solution.reset()
            self.set_page(2)
            if solver.result == "optimal":
                self.solution.show_solution(result)
            elif solver.result == "unbounded":
                self.solution.show_unbounded()
            elif solver.result == "infeasible":
                self.solution.show_infeasible()
            
        except Exception as e:
            print(f"Error executing core solver logic: {e}")
            import traceback
            traceback.print_exc()
            
        print("─" * 50)