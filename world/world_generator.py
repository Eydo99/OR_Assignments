import random

from utils.enums.place_type import PlaceType
from world.place import Place
from world.world import World


class WorldGenerator:
    def __init__(self, world_size, world_dimension, easy_win_score=2, neutral_win_score=1, hard_win_score=1
                 ,easy_lose_score=-1, neutral_lose_score=-1, hard_lose_score=-3):
        self.world_size = world_size
        self.world_dimension = world_dimension
        self.easy_win_score = easy_win_score
        self.neutral_win_score = neutral_win_score
        self.hard_win_score = hard_win_score
        self.easy_lose_score = easy_lose_score
        self.neutral_lose_score = neutral_lose_score
        self.hard_lose_score = hard_lose_score

    def generate_world(self)->World:
        world: list[list[Place]] = []
        if self.world_dimension == 1:
            world_1d: list[Place] =[]
            for _ in range(self.world_size):
                place_type=random.choice(list(PlaceType))
                place_win_score,place_lose_score=self._assign_score(place_type)
                world_1d.append(Place(place_win_score,place_lose_score ,place_type))
            world.append(world_1d)
        else:
            for _ in range(self.world_size):
                world_nd: list[Place] = []
                for _ in range(self.world_size):
                    place_type = random.choice(list(PlaceType))
                    place_win_score, place_lose_score = self._assign_score(place_type)
                    world_nd.append(Place(place_win_score, place_lose_score, place_type))
                world.append(world_nd)
        return world



    def _assign_score(self, place_type:PlaceType)-> tuple[int, int]:
        match place_type:
            case PlaceType.easy:
                return self.easy_win_score,self.easy_lose_score

            case PlaceType.neutral:
                return self.neutral_win_score,self.neutral_lose_score

            case PlaceType.hard:
                return self.hard_win_score,self.hard_lose_score

