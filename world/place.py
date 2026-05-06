from dataclasses import dataclass

from utils.enums.place_type import PlaceType

@dataclass
class Place:
    value:int
    place_type:PlaceType