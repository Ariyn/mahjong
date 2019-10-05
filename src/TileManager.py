import re

from .tile import *

class _TileManager:
  singleton = None

  @staticmethod
  def getInstance():
    if _TileManager.singleton == None:
      _TileManager.singleton = _TileManager()

    return _TileManager.singleton


  def __init__(self):
    self.tiles, self.inTiles, self.outTiles = {}, {}, [[] for i in range(5)]
    self.entire_dumpster, self.dumpster = [], [[] for i in range(4)]
    self.tileFormats = [re.compile("(%s)([1-9])" % "|".join(["|".join(list(i.names)) for i in Tile.NumTileTypes])), re.compile("(%s)()" % "|".join(["|".join(i.names) for i in Tile.CharTileTypes]))]
    self.createTiles()

    # for i in enumerate(self.inTiles):
    #   print(i[1], str(self.inTiles[i[1]]))
    # print(self.tileFormats[0])

  def createTiles(self):
    for e in Tile.NumTileTypes:
      for i in range(0, 9):
        # print(e)
        for z in range(0, 4):
          x = Tile(e, i+1, z+1)
          self.tiles[x.UID] = x
          self.inTiles[x.UID] = x


    for e in Tile.CharTileTypes:
      for z in range(0, 4):
        x = Tile(e, pTileOrilNum=z+1)
        self.tiles[x.UID] = x
        self.inTiles[x.UID] = x

  def getRandomTile(self, player=0, size=1):
    tiles = random.sample(list(self.tiles.values()), size)
    self.entire_dumpster += tiles
    self.outTiles[player] += tiles

    return tiles


  def get_dora_tile(self):
    return self.getRandomTile(4)


  def discard(self, player_num, tile):
    self.dumpster[player_num].append(tile)
    print("discard", player_num, tile, self.outTiles[player_num], "out")
    self.outTiles[player_num].remove(tile)


  def get_drawable_tiles(self, player=0):
    return list(set(self.tiles.values()) - set(self.outTiles[player]) - set(self.entire_dumpster))


  @staticmethod
  def sortTiles(hand):
    # newHand = [(Tile.tileOrder.index(itype)*10 + i.number,i) for i in hand]
    # print(newHand, sorted(newHand, key=itemgetter(0)))
    # print(hand)
    return [v for i,v in enumerate(sorted(hand, key=lambda i:i.UID))]

  def getTiles(self, tile):
    # print(self.tileFormats)
    x = []
    for i in self.tileFormats:
      d = [self.getTile(e) for e in i.findall(tile)]
      x += d

    return x

  def getTile(self, uid, player=0):
    parsed_id = re.search(r"([a-z]+)([0-9]*)", uid)
    if parsed_id:
      type_name, number = parsed_id.groups()
    else:
      raise AttributeError

    if type_name in Mantsu.names:
      id = "m"
    elif type_name in Pintsu.names:
      id = "p"
    elif type_name in Soutsu.names:
      id = "s"
    else:
      id = type_name

    order = ["m", "p", "s", "east", "south", "west", "north", "haku", "hatsu", "chun"].index(id)

    if 3 <= order: index = 1
    else: index = int(uid[1])

    order = (order+1)*100+index*10
    tile = None

    for i in range(1,5):
      # print(order+i, order+i in self.inTiles, len(self.inTiles))

      if order + i in self.inTiles:
        tile = self.inTiles[order + i]
        self.outTiles[player].append(tile)
        self.entire_dumpster.append(tile)
        self.inTiles.pop(order + i, None)
        break

    return tile

  def getTileWithUID(self, uid):
    return self.tiles[uid]


  @staticmethod
  def check_forms(hand):
    pass


  @staticmethod
  def get_complete_combination(form, hand, target):
    return [i[0] for i in form.calculate([1], hand, target) if 1 <= i[1]]


TileManager = _TileManager()