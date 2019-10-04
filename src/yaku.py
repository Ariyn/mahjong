#!python3

from collections import Counter
from operator import mul
from itertools import combinations, permutations, product, chain
from tile import Tile, TileManager, pic

# 만수, 통수, 삭수, 동, 남, 서, 북, 백, 발, 중
Mantsu, Pintsu, Souzu, East, South, West, North, Haku, Hatsu, Chun = "Manzu", "Pinzu", "Souzu", "East", "South", "West", "North", "Haku", "Hatsu", "Chun"

# tileType
# 수패, 자패, 준장패, 노두패
shuhai, tsupai, chunchanpai, loutouhai = "shuhai", "tsupai", "chunchanpai", "loutouhai"

# formType
koutsu, shuntsu, kantsu, ddoitsu = "koutsu", "shuntsu", "kantsu", "ddoitsu"
mentsu, atama = "mentsu", "atama"

class YakuForm:
	def __init__(self, tType, range=None, menzen=True):
		# type means Mantsu, Pintsu, Tongtsu, East, South, West, North, Haku, Hatsu, 
		# also can be shuhai, tsupai, loutouhai, chunchanpai
		self.tileType = tType

		# koutsu, shuntsu, kantsu, ddoitsu
		# mentsu, atama
		# self.completeType = cType
		self.size = 3 if self.tileType in [koutsu, shuntsu, mentsu] else 2 if self.tileType in [ddoitsu, atama] else 4

		# range canbe 1-9 or 0.
		# 0 means doesn't care
		self.range = range
		self.menzen = menzen

	def __str__(self):
		return "%s tiles %s %s %s"%(
			self.size,
			"%s~%s"%(self.range.start, self.range.stop) if self.range else "",
			"menzen" if self.menzen else "",
			self.tileType
		)

	def search(self, hand):
		keys, values = list(hand.keys()), list(hand.values())
		retVal = []
		
		x = {item//100-1:[] for item in hand}
		for item in hand:
			for i in range(0, hand[item]):
				x[item//100-1].append((item//10%10, item))
		
		for i in x:
			if self.tileType == atama or self.tileType == ddoitsu:
				diffs = [(e[0][0] == e[1][0], e) for e in combinations(x[i], 2)]
			elif self.tileType == kantsu:
				diffs = [(sum((e[0][0]-e[1][0], e[1][0]-e[2][0], e[2][0]-e[3][0])), e) for e in combinations(x[i], 4)]
			else:
				diffs = [(sum((e[0][0]-e[1][0], e[0][0]-e[2][0])), (e[0][0]+e[1][0]+e[2][0])/e[0][0] == 3, e) for e in combinations(x[i], 3)]
				
			for e in diffs:
				if self.tileType == koutsu:
					# print(e, sum((e[-1][0][0]-e[-1][1][0], e[-1][1][0]-e[-1][2][0])), e[-1][0][0], e[-1][1][0], e[-1][1][0]-e[-1][2][0])
					pass
				if (self.tileType == mentsu and abs(e[0])%3 == 0) or \
					(self.tileType == shuntsu and abs(e[0]) == 3) or \
					(self.tileType == koutsu and e[1]) or \
					(self.tileType == kantsu and e[0] == 0) or \
					((self.tileType == atama or self.tileType == ddoitsu) and e[0]):
					e = [str(ee[1]) for ee in e[-1]]
					e.sort()
					retVal.append(".".join(e))
			
		retVal = list(set(retVal))
		retVal.sort()
		
		for i, v in enumerate(retVal):
			v = [TileManager.getTileWithUID(int(e)) for e in v.split(".")]
			retVal[i] = v
				
		return retVal


class Yaku:
	def __init__(self, name, point, mPoint = None):
		self.name = name
		self.point, self.mPoint = point, point
		
		if mPoint:
			self.mPoint = mPoint

		self.terms = []

	def addTerm(self, tileType, range=None, menzen=True):
		form = YakuForm(tileType, range, menzen)
		self.terms.append(form)

	def __str__(self):
		return "%s points, %s" %(self.point, self.name)

	def term(self):
		return self.__str__()+"".join(["\n\t"+str(i) for i in self.terms])

	def match(self, hand):
		combs = [i.search(hand) for i in self.terms]
		# print(self.terms)
		print(combs)
		
		sequences = list(product(*combs, repeat=1))
		# print(len(sequences))
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
		tanyao.addTerm(shuhai, range(2,8))
		tanyao.addTerm(shuhai, range(2,8))
		tanyao.addTerm(shuhai, range(2,8))
		tanyao.addTerm(shuhai, range(2,8))
		tanyao.addTerm(ddoitsu, range(2,8))

		self.yakus.append(tanyao)

	def checkYaku(self, hand):
		newHand = Counter([i.UID for i in hand])
		correct = [i.match(newHand) for i in self.yakus]
		
		print(correct)
		# for i in correct[0]:
		# 	print(i)

def printHand(hand):
	for i in hand:
		print(i)

if __name__ == "__main__":
	ym = YakuManager()

	tm = TileManager.getInstance()
	hand = tm.getTiles("m2 m2 m2 m2 m3 m3 m4 m4 m3 s4 s5 p6 p7 p6")
	# hand = tm.getRandomTile(14)
	# for i in hand:
	# 	print(i)
	hand = TileManager.sortTiles(hand)
	ym.checkYaku(hand)
	# d = YakuForm(koutsu, range(1,9), True)
	# d = YakuForm(koutsu, range(1,9), True)
	
	# newHand = Counter([i.UID for i in hand])
	# x = d.search(newHand)
	# # x.sort()
	# 
	# print(len(x))
	# for i in x:
	# 	print([str(e) for e in i])
	# 
	# print(262-271, 271-261, sum([262-271, 271-261]))
