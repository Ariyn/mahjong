import json

from .TileManager import _TileManager
from .Yaku import Kantsu, Koutsu, Shuntsu, Toitsu

class Simulator:
  def __init__(self, player_num=4):
    self.TileManager = _TileManager()
    self.player_num = player_num
    self.user_hands = [sorted(self.TileManager.getRandomTile(i, size=13)) for i in range(self.player_num)]
    self.dora = self.TileManager.get_dora_tile()

  def run_single(self, strategy):
    for i, p in enumerate(self.user_hands):
      p += self.TileManager.getRandomTile(i)

      print(f"p{i} hand {self.print_hand(p)}")

      discard_tile, percent = strategy.discard(self.TileManager, p, i)
      p.remove(discard_tile)

      self.TileManager.discard(i, discard_tile)

      completes = {
        "kantsu": {t: self.TileManager.get_complete_combination(Kantsu, p, t) for t in p},
        "shuntsu": {t: self.TileManager.get_complete_combination(Shuntsu, p, t) for t in p},
        "koutsu": {t: self.TileManager.get_complete_combination(Koutsu, p, t) for t in p},
        "toitsu": {t: self.TileManager.get_complete_combination(Toitsu, p, t) for t in p},
      }
      completes = {i:{t:completes[i][t] for t in completes[i] if completes[i][t] != []} for i in completes}
      # print(completes)

      print(f'd {discard_tile.UID} f{percent}%')
      print(json.dumps({"user":i, "hand":self.print_hand(p)}))
      print("")
      # self.print_hand(p)
      # break

  def print_hand(self, hand):
    return [t.UID for t in hand]


if __name__ == "__main__":
  from .Strategy import BasicDiscard

  sim = Simulator()
  for i in range(10):
    sim.run_single(BasicDiscard)
    print("---")
    # break

  # tm = _TileManager()

  # hand = [tm.getTile("m8"), tm.getTile("m9")]
  # print(hand, BasicDiscard.discard(tm, hand))

  # name_list = list(map(lambda t:t.name, tm.get_drawable_tiles()))
  # print(hand[0].name)
  # print(name_list)
  # print(name_list.count(hand[0].name))