#include "naivebayes.h"

naiveBayes::naiveBayes(int numtype) :numberOfType(numtype)
{
	init();
}

void
naiveBayes::init()
{
	LoadDataSet();
	CreateVocabulary();
	TrainData();
}

void
naiveBayes::LoadDataSet()
{
	vector<vector<string>> data{
			{ "my", "dog", "has", "flea", "problems", "help", "please", "you", "a"},
			{ "maybe", "not", "take", "him", "to", "dog", "park", "stupid" },
			{ "my", "dalmation", "is", "so", "cute", "I", "love", "him", "are" },
			{ "stop", "posting", "stupid", "worthless", "garbage", "fuck" , "fucking" },
			{ "mr", "licks", "ate", "my", "steak", "how", "to", "stop", "him" },
			{ "quiet", "buying", "worthless", "dog", "food", "stupid" , "bitch" }
	};

	vector<int> classVec{ 0, 1, 0, 1, 0, 1 };
	for (size_t i = 0; i<data.size(); i++)
	{
		dataList.push_back(std::make_pair(data[i], classVec[i]));
	}
	
	srand(time_t(0));
	set<int> testNumber0, testNumber1;
	while (testNumber0.size() < 5 || testNumber1.size() < 5)
	{
		auto x = rand() % 26;
		if (x == 0)
			x = 1;
		if (testNumber0.size() < 5)
			testNumber0.insert(x);
		if (testNumber1.size() < 5)
			testNumber1.insert(x);
	}

	//load normal email data
	for (int i = 1; i < 26; i++)
	{
		vector<string> tempfile;
		stringstream ss;
		ss << "F:\\ML\\TestCase\\email\\ham\\" << i << ".txt";
		ifstream input(ss.str());
		string tempstring;
		while (getline(input,tempstring))
		{
			std::transform(tempstring.begin(), tempstring.end(), tempstring.begin(), tolower);
			auto vstring = parseDocum(tempstring);
			if (!vstring.empty())
				tempfile.insert(tempfile.end(), vstring.begin(), vstring.end());
		}
		input.close();
		if (testNumber0.count(i))
			testList.push_back(std::make_pair(tempfile, HAM));
		else
			dataList.push_back(std::make_pair(tempfile, HAM));
	}

	//load spam data
	for (int i = 1; i < 26; i++)
	{
		vector<string> tempfile;
		stringstream ss;
		ss << "F:\\ML\\TestCase\\email\\spam\\" << i << ".txt";
		ifstream input(ss.str());
		string tempstring;
		while (getline(input, tempstring))
		{
			std::transform(tempstring.begin(), tempstring.end(), tempstring.begin(), tolower);
			auto vstring = parseDocum(tempstring);
			if (!vstring.empty())
				tempfile.insert(tempfile.end(), vstring.begin(), vstring.end());
		}
		input.close();
		if (testNumber1.count(i))
			testList.push_back(std::make_pair(tempfile, SPAM));
		else
			dataList.push_back(std::make_pair(tempfile, SPAM));
	}
}

void
naiveBayes::CreateVocabulary()
{
	if (dataList.empty())
		return;

	for (const auto &doc : dataList)
	{
		for (const auto &word : doc.first)
		{
			vocabulary.insert(word);
		}
	}
}

vector<int>
naiveBayes::Words2Vec(const vector<string>& doc)
{
	vector<int> ret(vocabulary.size());
	for (const auto &word : doc)
	{
		auto iter = vocabulary.find(word);
		if (iter != vocabulary.end())
		{
			auto index = std::distance(vocabulary.begin(), iter);
			ret[index] = 1;
		}
	}
	return std::move(ret);
}

void
naiveBayes::TrainData()
{
	py.resize(numberOfType);
	//get py by Laplace smoothing
	int lambda = 1;
	vector<int> pyf(numberOfType);
	double ptotal;
	ptotal = (double)(dataList.size() + numberOfType * lambda);
	for (const auto &doc : dataList)
	{
		if (doc.second == 0)
			pyf[0]++;
		else if (doc.second == 1)
			pyf[1]++;
	}
	
	for (size_t i = 0; i < pyf.size(); ++i)
	{
		py[i] = (double)(pyf[i] + lambda) / ptotal;
	}

	//get pxc by Laplace smoothing
	for (int i = 0; i < numberOfType; i++)
	{
		pxc.insert(std::make_pair(i, vector<double>(vocabulary.size(), (double)lambda)));
	}

	for (auto pword = vocabulary.begin(); pword != vocabulary.end(); ++pword)
	{
		for (const auto &doc : dataList)
		{
			auto iter = std::find(doc.first.begin(), doc.first.end(), *pword);
			if (iter == doc.first.end())
				continue;
			auto index = std::distance(vocabulary.begin(), pword);
			if (doc.second == 0)
			{
				pxc[0][index] += 1.0;
			}
			else if (doc.second == 1)
			{
				pxc[1][index] += 1.0;
			}
		}
	}

	double Sj = (double)vocabulary.size();
	for (auto ps = pxc.begin(); ps != pxc.end(); ++ps)
	{
		double denom = (double)pyf[ps->first] + Sj * lambda;
		for (auto &p : ps->second)
		{
			p /= denom;
		}
	}
}

int
naiveBayes::ClassifyVec(const vector<int> &Vec)
{
	vector<double> pEachType(numberOfType,1.0);
	for (int i = 0; i < numberOfType; i++)
	{
		for (int j = 0; j < Vec.size(); ++j)
		{
			if (Vec[j] == 0)
			{
				pEachType[i] *= (1 - pxc[i][j]);
			}
			else if (Vec[j] == 1)
			{
				pEachType[i] *= pxc[i][j];
			}
		}
	}

	auto max = std::max_element(pEachType.begin(), pEachType.end());
	return (int)std::distance(pEachType.begin(), max);
}

vector<string>
naiveBayes::parseDocum(const string &doc)
{
	vector<string> ret;
	size_t delimiter; 
	auto the_end = doc.size();
	for (size_t pos = 0; pos < the_end;)
	{
		if (pos != the_end && !(doc[pos] == ' '))
		{
			delimiter = pos;
			do
			{
				++pos;
			} while (pos != the_end && !(doc[pos] == ' '));
			auto token = doc.substr(delimiter, pos - delimiter);
			do
			{
				char c = token.back();
				if (c == ',' || c == '.' || c == '!' || c == '?')
				{
					token.pop_back();
				}
				else
					break;
			} while (true);

			if (!token.empty())
				ret.push_back(token);
		}
		else
		{
			++pos;
		}
	}
	return std::move(ret);
}

void
naiveBayes::SpamTest()
{
	std::random_shuffle(testList.begin(), testList.end());
	int miss = 0, total = 0;
	for (const auto &testDoc : testList)
	{
		total++;
		auto vec = Words2Vec(testDoc.first);
		auto type = ClassifyVec(vec);

		if (type != testDoc.second)
		{
			miss++;
		}
		double rate = (double)miss / (double)total;
		printf("the error rate is %.5f\n", rate);
	}
}