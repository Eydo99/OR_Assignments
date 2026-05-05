from abc import ABC, abstractmethod

class GameMode(ABC):
    @abstractmethod
    def start_game(self):
        pass

    @abstractmethod
    def play_round(self,player_position=None):
        pass

    @abstractmethod
    def reset_game(self):
        pass

    @abstractmethod
    def show_results(self):
        pass

