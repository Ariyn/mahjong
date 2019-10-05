from collections import defaultdict

from ..Yaku import Kantsu, Koutsu, Shuntsu, Toitsu


def discard(tileManager, hand, player_num):
  hand.sort()

  percents = []
  total_percent = defaultdict(int)
  drawable_tiles = tileManager.get_drawable_tiles(player=player_num)

  for form in [Kantsu, Koutsu, Shuntsu, Toitsu]:
    for tile in hand:
      percent = form.calculate(drawable_tiles, hand, tile)
      sum_percent = sum(p[1] for p in percent)

      percents.append((form, tile, sum_percent))

      if form != Toitsu:
        total_percent[tile] = total_percent[tile] + sum_percent

  return sorted(total_percent.items(), key=lambda iv: iv[1])[0]
