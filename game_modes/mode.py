from abc import ABC, abstractmethod

class GameMode(ABC):
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def play_round(self):
        pass

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def show_round_results(self):
        pass

