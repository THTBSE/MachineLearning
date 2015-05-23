import numpy as np 
import matplotlib.pyplot as plt

def randomSampling(num):
	vectors = [] 
	for i in range(num):
		x = [np.random.randint(0,11) for i in range(5000)]
		y = [np.random.randint(0,11) for i in range(5000)]
		vectors.append((x,y))
	return vectors

def compare(vectors):
	rate = []
	for v in vectors:
		intersection = map(lambda x,y:min(x,y),v[0],v[1])
		s0 = sum(v[0])
		s1 = sum(v[1])
		si = sum(intersection)
		repeat = float(si) / max(s0,s1)

		v0 = np.array(v[0])
		v1 = np.array(v[1])
		v0 = v0 / np.linalg.norm(v0,2)
		v1 = v1 / np.linalg.norm(v1,2)

		cosine = np.dot(v0,v1)
		rate.append((repeat,cosine))

	rate.sort(key=lambda x:x[0])
	return rate

if __name__ == '__main__':
	vectors = randomSampling(1000)
	rate = compare(vectors)
	rate = np.array(rate)

	plt.plot(rate[:,0],rate[:,1])
	plt.show()





