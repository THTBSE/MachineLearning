#include "supportvm.h"

int main()
{
	srand(time(0));
	svmClassifier<100, 2> svm;
	svm.loadDataSet();
	svm.svmTrain(200, 0.0001, SVM_RBF);
	svm.testSet();

	
}