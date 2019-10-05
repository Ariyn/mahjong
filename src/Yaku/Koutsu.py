from itertools import combinations

from ..tile import Tile
from ..TileManager import TileManager
from ..Utils import mul

def calculate(drawable_tiles, hand, target):
    assert target in hand
    if not target.is_koutsu_possible:
        return [(None, 0)]

    possible_combinations = get_possible_combinations(target)

    possibilities = {
        target.name: 1
    }

    for possible_number in target.possible_combinations["koutsu"]:
        tile = Tile(target.type, possible_number)

        if tile not in hand:
            possibilities[tile.name] = drawable_tiles.count(tile) / len(drawable_tiles) / 4
        else:
            possibilities[tile.name] = 1

    koutsu_possibility = []

    for tiles in possible_combinations:
        percent = mul([possibilities[tile.name] for tile in tiles])
        koutsu_possibility.append((tiles, percent))

    return koutsu_possibility


def get_possible_combinations(target):
    koutsu_tiles = sorted([Tile(target.type, t) for t in target.possible_combinations["koutsu"]] + [target], key=lambda t: t.number)

    possible_combinations = []
    for i in range(max(0, len(koutsu_tiles)-2)):
        possible_combinations.append((koutsu_tiles[i], koutsu_tiles[i+1], koutsu_tiles[i+2]))

    return possible_combinations