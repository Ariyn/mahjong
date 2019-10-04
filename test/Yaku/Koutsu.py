import unittest

from src.TileManager import _TileManager
from src.Yaku.Koutsu import calculate, get_possible_combinations

class TestKoutsu(unittest.TestCase):
    SAMPLE_TILES = ["m1", "m2", "m4", "m5"]
    RYANMEN_WAITING_TILES = ["m4", "m5"]

    def setUp(self):
        self.TileManager = _TileManager()

    # TODO:
    # see issue #1
    def test_koutsu_with_quater_possibility(self):
        hand = [self.TileManager.getTile(t) for t in self.SAMPLE_TILES]
        only_require_tiles = [self.TileManager.getTile("m3") for i in range(4)]

        possibility = calculate(only_require_tiles, hand, hand[0])
        self.assertEqual(possibility[0][1], 0.25)


    def test_koutsu_when_no_drawable_tile(self):
        hand = [self.TileManager.getTile(t) for t in self.SAMPLE_TILES]
        [self.TileManager.getTile("m3") for i in range(4)]

        possibility = calculate(self.TileManager.get_drawable_tiles(), hand, hand[0])
        self.assertEqual(possibility[0][1], 0)


    def test_koutsu_when_ryanmen(self):
        hand = [self.TileManager.getTile(t) for t in self.RYANMEN_WAITING_TILES]

        possibility = calculate(self.TileManager.get_drawable_tiles(), hand, hand[0])
        most_percent = max(possibility, key=lambda p: p[1])

        self.assertTrue(most_percent[0] in (("m3", "m4", "m5"), ("m4", "m5", "m6")))


    def test_possible_combinations(self):
        target = self.TileManager.getTile("m3")

        combinations = get_possible_combinations(target)

        self.assertEqual(combinations[0], ("m1", "m2", "m3"))
        self.assertEqual(combinations[1], ("m2", "m3", "m4"))
        self.assertEqual(combinations[2], ("m3", "m4", "m5"))
    