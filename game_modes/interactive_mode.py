from game_modes.base_mode import BaseMode


class InteractiveMode(BaseMode):

    def play_round(self,player_position=None):
        self.execute_round(player_position)

    def start_game(self):
        self.reset_game()
