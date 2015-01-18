#include "supportvm.h"

int main()
{
	srand(time(0));
	svmClassifier<100, 2> svm;
	svm.loadDataSet();
	svm.svmTrain(200, 0.0001, SVM_RBF, 1.0);
	svm.testSet();
}