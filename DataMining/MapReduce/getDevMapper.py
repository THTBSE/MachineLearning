import sys

#'Name\tItem1:rating\tItem2:rating...'
def mapper():
	for line in sys.stdin:
		line = line.rstrip().split(',')
		items = line[1:]
		itemCount = len(items)
		for i in range(itemCount - 1):
			for j in range(i+1, itemCount):
				item1,rating1 = items[i].split(':')
				item2,rating2 = items[j].split(':')
				rating1 = float(rating1)
				rating2 = float(rating2)
				print '{0}:{1}\t{2}'.format(item1,item2,rating1 - rating2)
				print '{0}:{1}\t{2}'.format(item2,item1,rating2 - rating1)

if __name__ == '__main__':
	mapper()

