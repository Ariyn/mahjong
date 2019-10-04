#!python3
import random, re
from collections import defaultdict

def pic(tile):
	return tile.__pic__()

class TileType:
	names = ("test")

	def __eq__(self, t):
		if t in self.names:
			return True
		else:
			return False

	def __str__(self):
		return "<%s type>"%self.names[0]


	def get_short_name(self):
		return min(self.names, key=lambda n: len(n))

class Mantsu(TileType):
	names = ("Mantsu", "mantsu", "m")

class Pintsu(TileType):
	names = ("Pintsu", "pintsu", "p")

class Soutsu(TileType):
	names = ("Soutsu", "soutsu", "s")

class East(TileType):
	names = ("East", "east")

class South(TileType):
	names = ("South", "south")

class West(TileType):
	names = ("West", "west")

class North(TileType):
	names = ("North", "north")

class Haku(TileType):
	names = ("Haku", "haku")

class Hatsu(TileType):
	names = ("Hatsu", "hatsu")

class Chun(TileType):
	names = ("Chun", "chun")


class Tile:
	NumTileTypes, CharTileTypes = [Mantsu(), Pintsu(), Soutsu()], [East(), South(), West(), North(), Haku(), Hatsu(), Chun()]
	tileTypes = [type(i) for i in NumTileTypes] + [type(i) for i in CharTileTypes]
	tileOrder = NumTileTypes + CharTileTypes
	tileFontCharacter = [list("🀇🀈🀉🀊🀋🀌🀍🀎🀏"),list("🀙🀚🀛🀜🀝🀞🀟🀠🀡"), list("🀐🀑🀒🀓🀔🀕🀖🀗🀘"),"🀀","🀁","🀂","🀃","🀆","🀅","🀄"]

	def __init__(self, pType = None, pNumber = 1, pTileOrilNum = 0, pDora = False):
		if pNumber == None and pType == None:
			raise Exception

		if type(pType) == type and pType in self.tileTypes:
			pType = pType()
		elif type(pType) not in self.tileTypes:
			raise Exception

		self.name = pType.names[0]
		if pType in self.NumTileTypes:
			self.name += " "+str(pNumber)

		self.number = pNumber
		self.type = pType

		self.dora = pDora

		self.originNum = pTileOrilNum

		self.UID = (self.NumTileTypes.index(self.type)+1)*100 if self.type in self.NumTileTypes else (self.CharTileTypes.index(self.type)+4)*100
		self.UID += self.number*10+self.originNum

		self.ID = (self.tileOrder.index(self.type))*10 + self.number

		self.is_koutsu_possible = False
		self.is_shuntsu_possible = True
		self.possible_combinations = defaultdict(list)
		self.init_possible_combinations()


	def init_possible_combinations(self):
		if self.type in Tile.NumTileTypes:
			self.is_koutsu_possible = True

			if 2 < self.number:
				self.possible_combinations["koutsu"].append(self.number - 2)

			if 1 < self.number:
				self.possible_combinations["koutsu"].append(self.number - 1)

			if self.number < 9:
				self.possible_combinations["koutsu"].append(self.number + 1)

			if self.number < 8:
				self.possible_combinations["koutsu"].append(self.number + 2)

		self.possible_combinations["shuntsu"].append(self.number)

	def get_info(self):
		return (self.type.get_short_name(), self.number, self.originNum, self.dora)


	def distance(self, other):
		if type(other) == str:
			if other[0] in self.type.names:
				number = int(other[1])
		elif type(other) == int:
			number = other
		return abs(number - self.number)


	def __str__(self):
		return "%s %s"%(self.name, self.UID)


	def __repr__(self):
		return self.__str__()


	def __pic__(self):
		tile = Tile.tileFontCharacter[self.UID//100-1][self.UID%100//10-1]
		return tile

	def __eq__(self, t):
		types = type(t)

		if types == Tile:
			return t.type == self.type and t.number == self.number
		elif types == str:
			d1, d2 = re.match("(%s|%s|%s)([1-9])?"%tuple(["|".join(i.names) for i in self.NumTileTypes]), t), re.match("(%s)"%"|".join(["|".join(i.names) for i in self.CharTileTypes]), t)

			if d1:
				tileType, tileNumber = d1.group(1), int(d1.group(2))

				if tileType == self.type and tileNumber == self.number:
					return True
				else:
					return False
			elif d2:
				if self.tileType == d2.group(1):
					return True
				else:
					return False

		elif types in self.tileOrder:
			pass

	@staticmethod
	def getTileFromID(id):
		types, number = Tile.tileOrder[id//10], id%10
		# types, num
		name = types.names[0]
		if types in Tile.NumTileTypes:
			name += " "+str(number)

		return name
