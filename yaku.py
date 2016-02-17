from collections import Counter
from operator import mul
from itertools import combinations, permutations, product, chain
from tile import Tile, TileManager

Mantsu, Pintsu, Tongtsu, East, South, West, North, Haku, Hatsu = "Mantsu", "Pintsu", "Tongtsu", "East", "South", "West", "North", "Haku", "Hatsu"
shuhai, tsupai, chunchanpai, loutouhai = "shuhai", "tsupai", "chunchanpai", "loutouhai"

koutsu, shuntsu, kantsu, ddoitsu = "koutsu", "shuntsu", "kantsu", "ddoitsu"
mentsu, atama = "mentsu", "atama"

class YakuForm:
	def __init__(self, tType, cType, range=None, menzen=True):
		# type means Mantsu, Pintsu, Tongtsu, East, South, West, North, Haku, Hatsu, 
		# also shuhai, tsupai, loutouhai, chunchanpai
		self.tileType = tType

		# koutsu, shuntsu, kantsu, ddoitsu
		# mentsu, atama
		self.completeType = cType
		self.size = 3 if self.completeType in [koutsu, shuntsu, mentsu] else 2 if self.completeType in [ddoitsu, atama] else 4

		# 1-9 or 0 means doesn't care
		self.range = range
		self.menzen = menzen

	def __str__(self):
		return "%s%s %s%s"%(
			self.size,
			" %s~%s"%(self.range.start, self.range.stop) if self.range else "",
			"menzen " if self.menzen else "",
			self.tileType
		)

	def search(self, hand):
		keys, values = list(hand.keys()), list(hand.values())
		retVal = []

		if self.completeType in [mentsu, shuntsu]:
			x = {item//10:[] for item in hand}
			for item in hand:
				x[item//10].append(item%10)

			for i in x:
				diffs = [(sum((e[0]-e[1], e[0]-e[2])), e) for e in combinations(x[i], 3)]
				retVal += [[Tile.getTileFromID(ee+i*10) for ee in e[1]] for e in diffs if e[0] in (0, -3, 3)]

		if self.completeType in [koutsu, kantsu, ddoitsu, mentsu, atama]:
			retVal += [[Tile.getTileFromID(item)] for item, count in hand.items() if self.size <= count]

			# for item, count in hand.items():
			# 	if self.size <= count:
			# 		d = Tile.getTileFromID(item)
			# 		retVal.append(d)

		return retVal


class Yaku:
	def __init__(self, name, point, mPoint = None):
		self.name = name
		self.point, self.mPoint = point, point
		
		if mPoint:
			self.mPoint = mPoint

		self.terms = []

	def addTerm(self, tileType, cType, range=None, menzen=True):
		form = YakuForm(tileType, cType, range, menzen)
		self.terms.append(form)

	def __str__(self):
		return "%s points, %s" %(self.point, self.name)

	def term(self):
		return self.__str__()+"".join(["\n\t"+str(i) for i in self.terms])

	def match(self, hand):
		combs = [i.search(hand) for i in self.terms]

		sequences = list(product(*combs, repeat=1))
		print(len(sequences))
		removeLambda = (lambda x, i, d: (x.remove(d), True) if len(i) != len(set(i)) else False)
		
		i=0
		while i < len(sequences):
			var, i = sequences[i], i+1

			# need to check amount of tile in hand
			# if ther is 4 tiles, i can use both koutsu and shuntsu
			if removeLambda(sequences, [str(e) for e in var], var):
				i-=1
			elif removeLambda(sequences, list(chain.from_iterable(var)), var):
					i-=1

		return sequences
	
class YakuManager:
	def __init__(self):
		self.yakus = []

		tanyao = Yaku("tanyao", 1)
		tanyao.addTerm(shuhai, mentsu, range(2,8))
		tanyao.addTerm(shuhai, mentsu, range(2,8))
		tanyao.addTerm(shuhai, mentsu, range(2,8))
		tanyao.addTerm(shuhai, mentsu, range(2,8))
		tanyao.addTerm(shuhai, ddoitsu, range(2,8))

		self.yakus.append(tanyao)

	def checkYaku(self, hand):
		newHand = Counter([i.ID for i in hand])
		correct = [i.match(newHand) for i in self.yakus]

		for i in correct[0]:
			print(i)

def printHand(hand):
	for i in hand:
		print(i)

if __name__ == "__main__":
	ym = YakuManager()

	tm = TileManager().getInstance()
	hand = tm.getTiles("m2 m2 m2 m4 m4 s3 s4 s5 p5 p5 p5 p8 p7 p6")
	# hand = tm.getRandomTile(14)
	# hand = TileManager.sortTiles(hand)
 
	ym.checkYaku(hand)



