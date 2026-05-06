import random

from utils.enums.place_type import PlaceType
from world.place import Place


class WorldGenerator:
    def __init__(self, world_size, world_dimension, easy_score=2, neutral_score=1, hard_score=3):
        self.world_size = world_size
        self.world_dimension = world_dimension
        self.easy_score = easy_score
        self.neutral_score = neutral_score
        self.hard_score = hard_score

    def generate_world(self)->list[list[Place]]:
        world: list[list[Place]] = []
        if self.world_dimension == 1:
            world_1d: list[Place] =[]
            for _ in range(self.world_size):
                place_type=random.choice(list(PlaceType))
                place_score=self._assign_score(place_type)
                world_1d.append(Place(place_score, place_type))
            world.append(world_1d)
        else:
            for _ in range(self.world_size):
                world_nd: list[Place] = []
                for _ in range(self.world_size):
                    place_type = random.choice(list(PlaceType))
                    place_score = self._assign_score(place_type)
                    world_nd.append(Place(place_score, place_type))
                world.append(world_nd)
        return world



    def _assign_score(self, place_type:PlaceType)->int:
        match place_type:
            case PlaceType.easy:
                return self.easy_score

            case PlaceType.neutral:
                return self.neutral_score

            case PlaceType.hard:
                return self.hard_score

