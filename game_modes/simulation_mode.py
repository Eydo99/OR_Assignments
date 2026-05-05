import random
from game_modes.base_mode import BaseMode
from utils.enums.role import Role




class SimulationMode(BaseMode):

    def play_round(self,player_position=None):
        world_dimension = self.game_state.world_dimension
        world_size = self.game_state.world_size
        player_position=random.randint(0, world_size - 1) if(world_dimension==1)\
            else (random.randint(0, world_size - 1),random.randint(0, world_size - 1))
        self.execute_round(player_position)


    def start_game(self) :
        self.reset_game()
        for _ in range(100):
            self.play_round()





