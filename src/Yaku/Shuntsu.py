from itertools import combinations

from ..tile import Tile
from ..TileManager import TileManager
from ..Utils import mul

def calculate(drawable_tiles, hand, target):
    assert target in hand
    # every tile in mahjong is shuntsu_possible.

    completed_combination_size = hand.count(target)
    drawable_combination_size = drawable_tiles.count(target)

    possibility = 1
    for i in range(3 - completed_combination_size):
      possibility *= drawable_combination_size / 4 /len(drawable_tiles)

    return possibility


def get_possible_combinations(target):
    return target.possible_combinations