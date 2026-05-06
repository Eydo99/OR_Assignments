from world.place import Place
from world.world import World
import numpy as np


class PayoffMatrix:
    def __init__(self,world:World):
        self.world=world

    def generate_payoff_matrix(self)->np.ndarray:
        places:list[Place] = []
        for dimension in self.world:
            for place in dimension:
                places.append(place)

        payoff_matrix= np.zeros((len(places),len(places)))

        for i,hider_place in enumerate(places):
            for j,seeker_place in enumerate(places):
                if i==j:
                    payoff_matrix[i][j]=hider_place.lose_value
                else:
                 payoff_matrix[i][j]=hider_place.win_value
        return payoff_matrix


