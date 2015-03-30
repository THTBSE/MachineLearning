
class recommender():
	def __init__(self,data):
		self.data = data
		self.cardS = {}
		self.dev = {}
		self.getDeviation(self.data)

	def getDeviation(self,data):
		for user in data:
			rating = data[user]
			items = data[user].keys()
			itemsCount = len(items)
			for i in range(itemsCount - 1):
				self.dev.setdefault(items[i],{})
				for j in range(i+1,itemsCount):
					self.dev.setdefault(items[j],{})
					pair = frozenset([items[i],items[j]])
					self.cardS.setdefault(pair,0)
					self.cardS[pair] += 1
					self.dev[items[i]].setdefault(items[j],0.0)
					self.dev[items[i]][items[j]] += rating[items[i]] - rating[items[j]]
					self.dev[items[j]].setdefault(items[i],0.0)
					self.dev[items[j]][items[i]] += rating[items[j]] - rating[items[i]]
		for Si in self.dev.keys():
			for Sj in self.dev[Si].keys():
				pair = frozenset([Si,Sj])
				self.dev[Si][Sj] /= self.cardS[pair]

	def updateDeviation(self,ratings):
		items = ratings.keys()
		itemsCount = len(items)
		for i in range(itemsCount - 1):
			self.dev.setdefault(items[i],{})
			for j in range(i+1,itemsCount):
				self.dev.setdefault(items[j],{})
				pair = frozenset([items[i],items[j]])
				origCardS = self.cardS.setdefault(pair,0)
				currCardS = origCardS + 1
				#update cardS
				self.cardS[pair] = currCardS
				#update dev[i][j]
				origDevIJ = self.dev[items[i]].setdefault(items[j],0.0)
				currDevIJ = ratings[items[i]] - ratings[items[j]]
				self.dev[items[i]][items[j]] = (origDevIJ * origCardS + currDevIJ) / currCardS
				#update dev[j][i]
				self.dev[items[j]][items[i]] = (-self.dev[items[i]][items[j]])

	def recommendation(self,user):
		name = user.keys()[0]
		userRating = user[name]
		if name not in self.data:
			self.data[name] = userRating
			self.updateDeviation(userRating)

		recommend = {}
		for item in self.dev.keys():
			if item not in userRating:
				numerator = 0.0
				denominator = 0.0
				for u in userRating:
					count = self.cardS[frozenset([item,u])]
					numerator += (self.dev[item][u] + userRating[u]) * count
					denominator += count
				recommend[item] = numerator / denominator

		recommend = recommend.items()
		recommend.sort(key=lambda x:x[1],reverse=True)
		return recommend

#demo 
if __name__ == '__main__':
	users = {"Amy": {"Taylor Swift": 4, "PSY": 3, "Whitney Houston": 4},
         	 "Clara": {"PSY": 3.5, "Whitney Houston": 4},
          	"Daisy": {"Taylor Swift": 5, "Whitney Houston": 3}}

	r = recommender(users)
	user = {'Ben':{'Taylor Swift':5,'PSY':2}}
	rec = r.recommendation(user)
	print rec

	for item in r.dev:
		print item,r.dev[item]