#ifndef _NAIVEBAYES_H_
#define _NAIVEBAYES_H_
#include <vector>
#include <set>
#include <map>
#include <string>
#include <algorithm>
#include <fstream>
#include <sstream>
using namespace std;
typedef std::pair<vector<string>, int> DataSet;

#define HAM 0
#define SPAM 1



class naiveBayes
{
public:
	naiveBayes(int numtype);
	int ClassifyVec(const vector<int> &Vec);
	vector<string> parseDocum(const string &doc);
	map<int, vector<double>> pxc;
	vector<double> py;

	//for training
	vector<DataSet> dataList;
	//for testing
	vector<DataSet> testList;

	set<string> vocabulary;
	vector<int> Words2Vec(const vector<string> &doc);

	//Test 
	void SpamTest();
private: 
	int numberOfType;
	void init();
	void LoadDataSet();
	void CreateVocabulary();
	void TrainData();
};




#endif