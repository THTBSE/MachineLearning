from collections import defaultdict
import random,math,sys

def corpus_generator(file_path):
	for line in open(file_path):
		words = line.rstrip().split(' ')
		yield words

class plsa():
	def __init__(self,topic_num):
		self.words = set()
		self.n_d_w = [] # n(d,w)
		self.topic_num = topic_num
		self.p_d_z = []   # p(z|d) probability of each topic z of given document 
		self.p_z_w = [defaultdict(float) for i in range(topic_num)]  # p(w|z) probability of each word w of given topic z

	def init_params(self):
		for z in self.p_z_w:
			for word in self.words:
				z[word] = random.random()

	def load_corpus(self,corpus):
		if isinstance(corpus,str):
			corpus = corpus_generator(corpus)

		for doc in corpus:
			self.n_d_w.append(defaultdict(int)) 
			self.p_d_z.append([random.random() for i in range(self.topic_num)])
			for word in doc:
				self.words.add(word)
				self.n_d_w[-1][word] += 1

		self.init_params()

	def log_likelihood(self):
		doc_num = len(self.n_d_w)
		likelihood = 0
		for i in xrange(doc_num):
			for w in self.n_d_w[i]:
				p_d_w = 0
				for k in xrange(self.topic_num):
					p_d_w += self.p_d_z[i][k] * self.p_z_w[k][w]
				likelihood += self.n_d_w[i][w] * math.log(p_d_w)
		return likelihood

	def train(self,max_iter=70):

		doc_num = len(self.n_d_w)
		for epoch in xrange(max_iter):
			p_dw_z = {}
			# # # e step
			for i in xrange(doc_num):
				for w in self.n_d_w[i]:
					dw = (i,w)
					numerator = [self.p_d_z[i][k]*self.p_z_w[k][w] for k in range(self.topic_num)]
					p_d_w = sum(numerator)
					p_dw_z[dw] = [numerator[k] / p_d_w for k in range(self.topic_num)]

			# # # m step  计算p(w|z)
			for k in range(self.topic_num):
				denom = 0.0
				numerator = defaultdict(float)
				for w in self.words:
					for i in xrange(doc_num):
						dw = (i,w)
						if w in self.n_d_w[i]:
							n_d_w_p_z_dw = self.n_d_w[i][w] * p_dw_z[dw][k]
							denom += n_d_w_p_z_dw
							numerator[w] += n_d_w_p_z_dw

				for w in self.words:
					self.p_z_w[k][w] = numerator[w] / denom

			# # # 计算 p(z|d)
			for i in xrange(doc_num):
				denom = 0.0
				numerator = [0.0 for k in range(self.topic_num)]

				for k in range(self.topic_num):
					for w in self.words:
						dw = (i,w)
						if w in self.n_d_w[i]:
							n_d_w_p_z_dw = self.n_d_w[i][w] * p_dw_z[dw][k]
							denom += n_d_w_p_z_dw
							numerator[k] += n_d_w_p_z_dw


				for k in range(self.topic_num):
					self.p_d_z[i][k] = numerator[k] / denom

			ll = self.log_likelihood()
			print 'epoch {0} done...,log_likelihood:{1}'.format(epoch,ll)
			sys.stdout.flush()

	def print_topic_word(self,num):
		for k in range(self.topic_num):
			words = self.p_z_w[k].items()
			words.sort(key=lambda x:x[1],reverse=True)
			print 'topic:{0}'.format(k)
			if num > len(words):
				num = len(words)
			for i in range(num):
				print words[i][0]


if __name__ == '__main__':
	plsa_test = plsa(5)
	plsa_test.load_corpus('corpus1')
	print 'load corpus done'
	plsa_test.train()
	plsa_test.print_topic_word(10)

