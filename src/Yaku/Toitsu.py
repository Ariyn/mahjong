from itertools import combinations

from ..tile import Tile
from ..TileManager import TileManager
from ..Utils import mul

def calculate(drawable_tiles, hand, target):
    assert target in hand
    # every tile in mahjong is toitsu_possible.

    completed_combination_size = hand.count(target)
    drawable_combination_size = drawable_tiles.count(target)

    possibility = 1
    for i in range(2 - completed_combination_size):
      possibility *= drawable_combination_size / 4 / len(drawable_tiles)

    return [((target, target), possibility)]


def get_possible_combinations(target):
    return target.possible_combinations