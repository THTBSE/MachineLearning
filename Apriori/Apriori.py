
class Apriori():
	def __init__(self,minSupport=0.7,minConf=0.7):
		self.minSupport = minSupport
		self.minConf = minConf
		self.FIS = []
		self.Support = {}
		self.AssoRules = []

	def CreateC1(self,data):
		C1 = [item for itemSet in data for item in itemSet]
		C1 = [[item] for item in set(C1)]
		return map(frozenset,C1)

	def ScanForFIS(self,Ck,data):
		Support = [0.0 for s in Ck]
		for itemSet in data:
			for i,can in enumerate(Ck):
				if can.issubset(itemSet):
					Support[i] = Support[i] + 1
		totolSize = float(len(data))
		Support = [s / totolSize for s in Support]
		FIS = []
		FISSupport = []
		for s,can in zip(Support,Ck):
			if s >= self.minSupport:
				FIS.append(can)
				FISSupport.append(s)
		return FIS,FISSupport

	def UpdateCk(self,Ck):
		CkPlus = []
		SetSize = len(Ck)
		for i in range(SetSize):
			for j in range(i+1,SetSize):
				if len(Ck[i]) == 1:
					CkPlus.append(Ck[i].union(Ck[j]))
				elif list(Ck[i])[:-1] == list(Ck[j])[:-1]:
					CkPlus.append(Ck[i].union(Ck[j]))
		return CkPlus

	def GetFIS(self,data):
		Ck = self.CreateC1(data)
		while True:
			FIS,Support = self.ScanForFIS(Ck,data)
			self.FIS.append(FIS)
			self.Support.update(dict(zip(FIS,Support)))
			Ck = self.UpdateCk(FIS)        #find next Ck from frequent item sets 
			if not Ck:
				break
		return self

	def GenAllSubSets(self,freqSet):
		subSets = []
		Ck = [frozenset([item]) for item in freqSet]
		subSets.extend(Ck)
		while True:
			Ck = self.UpdateCk(Ck)
			if len(Ck) != 1:
				subSets.extend(Ck)
			else:
				break
		return subSets

	def AssociatedRules(self):
		lenFIS = len(self.FIS)
		for i in range(1,lenFIS):
			for freqSet in self.FIS[i]:
				subSets = self.GenAllSubSets(freqSet)
				for lSet in subSets:
					rSet = freqSet - lSet
					conf = self.Support[freqSet] / self.Support[lSet]
					if conf >= self.minConf:
						self.AssoRules.append((lSet,rSet,conf))
						print 'rules {0} --> {1}, conf = {2}'.format(lSet,rSet,conf)
		return None
		
if __name__ == '__main__':
	mushroom = [line.rstrip().split() for line in open('mushroom.dat','rb')]
	mushroom = [item for item in mushroom if item[0] == '2']
	ap = Apriori(0.5,0.5)
	ap = ap.GetFIS(mushroom)
	for item in ap.FIS[3]:
		print item
	
