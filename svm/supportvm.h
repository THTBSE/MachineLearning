#ifndef _SUPPORTVM_H_
#define _SUPPORTVM_H_
#include "../Algebra/GteMatrix.h"
#include "../Algebra/GteVector.h"
#include <algorithm>
#include <vector>
#include <fstream>
#include <cstdio>
using namespace gte;

//--- M : the number of examples ---
//--- N : the number of features --- 
#define SVM_LIN 0
#define SVM_RBF 1


template <unsigned M, unsigned N>
class svmClassifier
{
public:
	void loadDataSet();
	void svmTrain(int c, double tol, int ktype, double sig = 1.3);
	void testSet();

	int svmPredict(const Vector<N, double> &x);
	int svmOutput(int i);
	void smoAlgorithm();
	int examineExample(int i2);
	double calcEk(int i);

	Matrix<M, M, double> Kernel;
	Matrix<M, N, double> dataSetIn;
	Vector<M, double> label;
	Vector<M, double> alpha;
	Vector<M, double> errorsCache;
	int C;
	double tolerance, b;
	int kernelType;
	double sigma;

private:
	void selectI2(int &i1, double &E1, int i2, double E2);
	int takeStep(int i1, int i2, double E1, double E2);
	double kernelTransfer(int i1, int i2);
	double kernerlTrans(const Vector<N, double> &xi, const Vector<N, double> &x);
};


#include "supportvm.cpp"

#endif