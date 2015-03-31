import sys

#item1:item2\tdeviation
def reducer():
	itemDev = {}
	count = {}
	for line in sys.stdin:
		line = line.split('\t')
		itemDev.setdefault(line[0],0.0)
		count.setdefault(line[0],0)
		itemDev[line[0]] += float(line[1])
		count[line[0]] += 1
	for pair in itemDev:
		deviation = itemDev[pair] / count[pair]
		item1,item2 = pair.split(':')
		print '{0}->{1}\t{2}'.format(item1,item2,deviation)

if __name__ == '__main__':
	reducer()

