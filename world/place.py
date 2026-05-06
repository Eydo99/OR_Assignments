from dataclasses import dataclass

from utils.enums.place_type import PlaceType

@dataclass
class Place:
    win_value:int
    lose_value:int
    place_type:PlaceType