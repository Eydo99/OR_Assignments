from dataclasses import dataclass


@dataclass
class SimulationResults:
    total_rounds: int
    player_score: float
    computer_score: float
    player_rounds_won: int
    computer_rounds_won: int