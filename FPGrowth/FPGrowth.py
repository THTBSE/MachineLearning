
class TreeNode():
	def __init__(self,item,parent=None,count=1):
		self.item = item
		self.count = count
		self.parent = parent
		self.children = {}
		self.next = None

	def display(self,indent=1):
		print '  '*indent,self.item,' ',self.count
		for child in self.children:
			self.children[child].display(indent+1)

class fpGrowth():
	def __init__(self,minSupport=3):
		self.fpTree = None
		self.headerTable = {}
		self.minSupport = minSupport
		self.sortedItems = []
		self.headerPath = {}

	#fixed the order of items in dataSet
	def __InitializeSet(self,dataSet):
		dataSet = map(frozenset,dataSet)
		return dataSet

	def SortFilterItems(self,dataSet):
		headerTable = {}
		for Set in dataSet:
			for item in Set:
				if item in headerTable:
					headerTable[item] += 1
				else:
					headerTable[item] = 1
		for key in headerTable.keys():
			if headerTable[key] < self.minSupport:
				del headerTable[key]
		for i in range(len(dataSet)):
			items = [(item,headerTable[item]) for item in dataSet[i] if item in headerTable]
			items = sorted(items,key=lambda x:x[1],reverse=True)
			dataSet[i] = [item[0] for item in items]
		sortedItems = sorted(headerTable.items(),key=lambda x:x[1],reverse=True)
		return sortedItems, headerTable

	def LinkNodes(self,root,prevNode=None):
		if root.item == 'root':
			prevNode = {}
		elif not root.item in self.headerPath:
			self.headerPath[root.item] = root 
			prevNode[root.item] = root 
		else:
			prevNode[root.item].next = root 
			prevNode[root.item] = root 
		for ckey in root.children:
			self.LinkNodes(root.children[ckey],prevNode)

	def CreateTree(self,dataSet):
		dataSet = self.__InitializeSet(dataSet)
		self.fpTree = TreeNode('root')
		self.sortedItems, self.headerTable = self.SortFilterItems(dataSet)
		#print dataSet
		for Set in dataSet:
			currTree = self.fpTree
			for item in Set:
				if item in currTree.children:
					currTree.children[item].count += 1
				else:
					currTree.children[item] = TreeNode(item,currTree)
				currTree = currTree.children[item]

		self.LinkNodes(self.fpTree)

	#Set in cpb ---> ['x','y','z',5] 
	def CreateCFPTree(self,cpb):
		cfpTree = TreeNode('root')
		for Set in cpb:
			if len(Set) == 1:
				continue
			currTree = cfpTree
			for item in Set[:-1]:
				if item in currTree.children:
					currTree.children[item].count += Set[-1]
				else:
					currTree.children[item] = TreeNode(item,currTree,Set[-1])
				currTree = currTree.children[item]
		return cfpTree

	#freqSets in dict ,key is frozenset() ,value is support 
	def GetFreqSet(self,cfpTree,freqSets):
		if cfpTree.item != 'root':
			for p in freqSets.keys():
				Set = p | frozenset([cfpTree.item])
				if Set in freqSets:
					freqSets[Set] += cfpTree.count
				else:
					freqSets[Set] = cfpTree.count
		for ckey in cfpTree.children:
			self.GetFreqSet(cfpTree.children[ckey],freqSets)

	def RecallPathForCPB(self):
		path = {}
		cpbs = {}
		for key in self.headerPath:
			node = self.headerPath[key]
			while True:
				p = []
				aNode = node
				while aNode.item != 'root':
					p.append(aNode.item)
					aNode = aNode.parent
				p.reverse()
				p.pop()
				p.append(node.count)
				if key in path:
					path[key].append(p)
				else:
					path[key] = [p]
				node = node.next
				if node == None:
					break
		for k in path.keys():
			#print k,path[k]
			stat = {}
			cpbs[k] = []
			for freqSet in path[k]:
				count = freqSet[-1]
				for item in freqSet[:-1]:
					if item in stat:
						stat[item] += count
					else:
						stat[item] = count
			for freqSet in path[k]:
				count = freqSet[-1]
				if len(freqSet) == 1:
					cpbs[k].append(freqSet)
					continue
				freqSet = [item for item in freqSet[:-1] if stat[item] >= self.minSupport]
				freqSet.append(count)
				cpbs[k].append(freqSet)
		return cpbs

	def Pivot(self,cpbs):
		allSets = []
		for k in cpbs:
		#	print k,cpbs[k]
		#	print '----------'
			cfpT = self.CreateCFPTree(cpbs[k])
			freqSets = {frozenset([k]):reduce(lambda x,y:x+y[-1],cpbs[k],0)}
			self.GetFreqSet(cfpT,freqSets)
			allSets.append(freqSets)
		for fqs in allSets:
			for k in fqs:
				print k

def loadSimpDat():
    simpDat = [['r', 'z', 'h', 'j', 'p'],
               ['z', 'y', 'x', 'w', 'v', 'u', 's', 't'],
               ['z'],
               ['r', 'x', 'n', 'o', 's'],
               ['y', 'r', 'x', 'z', 'q', 't', 'p'],
               ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]
    return simpDat

#dataSet = loadSimpDat()
dataSet = [line.split() for line in open('kosarak.dat','r')]
fpg = fpGrowth(100000)
fpg.CreateTree(dataSet)
#fpg.fpTree.display()
cpbs = fpg.RecallPathForCPB()

fpg.Pivot(cpbs)
#cfpT = fpg.CreateCFPTree(cpb)
#freqSets = {frozenset(['t']):reduce(lambda x,y:x[1]+y[1],cpb)}
#fpg.GetFreqSet(cfpT,freqSets)
#print freqSets