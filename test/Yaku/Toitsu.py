import unittest

from src.TileManager import _TileManager
from src.Yaku.Toitsu import calculate, get_possible_combinations

class TestKoutsu(unittest.TestCase):
  SAMPLE_TILES = ["m1"]

  def setUp(self):
    self.TileManager = _TileManager()

  # TODO:
  # see issue #1
  def test_toitsu_with_single_hand_possibility(self):
    hand = [self.TileManager.getTile(self.SAMPLE_TILES[0])]
    sample_drawable_tiles = [self.TileManager.getTile(self.SAMPLE_TILES[0]) for i in range(3)]

    possibility = calculate(sample_drawable_tiles, hand, hand[0])

    self.assertEqual(possibility, 0.25)


  def test_toitsu_with_character_tile(self):
    hand = [self.TileManager.getTile("chun")]
    sample_drawable_tiles = [self.TileManager.getTile("chun"), self.TileManager.getTile("chun"), self.TileManager.getTile("chun")]

    possibility = calculate(sample_drawable_tiles, hand, hand[0])

    self.assertEqual(possibility, 0.25)


  def test_toitsu_with_no_drawable_tile(self):
    hand = [self.TileManager.getTile(t) for t in self.SAMPLE_TILES]
    [self.TileManager.getTile(self.SAMPLE_TILES[0]) for _ in range(3)]

    possibility = calculate(self.TileManager.get_drawable_tiles(), hand, hand[0])

    self.assertEqual(possibility, 0)
