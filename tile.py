import random, re

class TileType:
	names = ("test")

	def __eq__(self, t):
		if t in self.names:
			return True
		else:
			return False

	def __str__(self):
		return "<%s type>"%self.names[0]

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


class Tile():
	NumTileTypes, CharTileTypes = [Mantsu(), Pintsu(), Soutsu()], [East(),South(),West(),North(),Haku(),Hatsu(),Chun()]
	tileTypes = [type(i) for i in NumTileTypes]+[type(i) for i in CharTileTypes]
	tileOrder = NumTileTypes+CharTileTypes

	def __init__(self, pType = None, pNumber = 0, pTileOrilNum = 0, pDora = False):
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

		# self.typeNumber = checker.Checker.typeNumber[checker.Checker.type.index(self.tileType)]

	def getInfo(self):
		if self.error:
			return False
		else:
			return self.tileType, self.number, self.dora

	def __str__(self):
		return "%s %s"%(self.name, self.UID)

	def __eq__(self, t):
		types = type(t)

		if types == Tile:
			pass
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
		

class TileManager:
	singleton = None

	@staticmethod
	def getInstance():
		if TileManager.singleton == None:
			TileManager.singleton = TileManager()

		return TileManager.singleton


	def __init__(self):
		self.tiles, self.outTiles = [], []
		self.tileFormats = [re.compile("((?:%s)[1-9])" % "|".join(["|".join(list(i.names)) for i in Tile.NumTileTypes])), re.compile("((?:%s)[1-9])" % " | ".join([str(i) for i in Tile.CharTileTypes]))]
		self.createTiles()
		# print(self.tileFormats[0])

	def createTiles(self):
		for e in Tile.NumTileTypes:
			for i in range(0, 9):
				# print(e)
				self.tiles.append(Tile(e, i+1, 1))
				self.tiles.append(Tile(e, i+1, 2))
				self.tiles.append(Tile(e, i+1, 3))
				self.tiles.append(Tile(e, i+1, 4))

		for e in Tile.CharTileTypes:
			self.tiles.append(Tile(e, pTileOrilNum=1))
			self.tiles.append(Tile(e, pTileOrilNum=2))
			self.tiles.append(Tile(e, pTileOrilNum=3))
			self.tiles.append(Tile(e, pTileOrilNum=4))

	def getRandomTile(self, size=1):
		tiles = random.sample(self.tiles, size)
		for i in tiles:
			self.outTiles.append(i)
			self.tiles.remove(i)

		return tiles

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

	def getTile(self, tile):
		for i in self.tiles:
			if i == tile:
				self.outTiles.append(i)
				self.tiles.remove(i)
				return i
				break
		
		pass


"""
M = Mantz
P = Pintz
S = Soutz

E = East
O = sOuth
W = West
N = North

H = Haku
A = hAtsu
C = Chuu
"""

if __name__ == "__main__":
	tm = TileManager().getInstance()
	hand = tm.getTiles("m2, mantsu2, Mantsu2, soutsu3, s4, Soutsu5, p6, Pintsu7, pintsu8, p5, p5, p5, m4, m4")

	# for i in hand:
	# 	print(i)
	# print(hand)
	hand = tm.getRandomTile(14)
	hand = TileManager.sortTiles(hand)

	for i in hand:
		print(i, i.ID)
	
