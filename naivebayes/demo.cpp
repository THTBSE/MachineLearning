#include "naivebayes.h"
#include <cstdio>

naiveBayes NB(2);

int main()
{

	/*printf("py1 = %.3f, py2 = %.3f\n", NB.py[0], NB.py[1]);

	for (auto pword = NB.vocabulary.begin(); pword != NB.vocabulary.end(); ++pword)
	{
		auto index = std::distance(NB.vocabulary.begin(), pword);
		printf("py1 %s:%.3f\n", (*pword).c_str(), NB.pxc[0][index]);
	}

	for (auto pword = NB.vocabulary.begin(); pword != NB.vocabulary.end(); ++pword)
	{
		auto index = std::distance(NB.vocabulary.begin(), pword);
		printf("py2 %s:%.3f\n", (*pword).c_str(), NB.pxc[1][index]);
	}*/

	vector<string> testCase{ "Do you love me? I love you so much!", "Do you want to buy this today? It's only $100!" };

	for (const auto &doc : testCase)
	{
		auto svec = NB.parseDocum(doc);
		auto vec = NB.Words2Vec(svec);
		auto type = NB.ClassifyVec(vec);

		if (type == 0)
		{
			printf("%s : Normal mail\n", doc.c_str());
		}
		else if (type == 1)
		{
			printf("%s : Spam mail\n", doc.c_str());
		}
	}

	printf("\nBegin run test cases!\n");
	NB.SpamTest();

	while (true)
	{

	}
}