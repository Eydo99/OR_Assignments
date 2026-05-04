from utils.enums.role import Role

class Validator:
    @staticmethod
    def validate_move(move,world_size:int,dimension:int)-> bool | None:
        if dimension==1:
            return Validator._validate_move_1d(move,world_size)
        elif dimension==2:
            return Validator._validate_move_2d(move,world_size)
        return None

    @staticmethod
    def validate_role(player_role:Role)->bool:
        return True if (player_role==Role.hider or player_role==Role.seeker) else False

    @staticmethod
    def validate_world_size(world_size:int)->bool:
        return True if world_size>0 else False

    @staticmethod
    def _validate_move_1d(move: int, world_size: int) -> bool:
        return True if (0<=move<world_size) else False

    @staticmethod
    def _validate_move_2d(move: tuple[int, int], world_size: int) -> bool:
        return True if (0<=move[0]<world_size and 0<=move[1]<world_size) else False


