#ifndef _SUPPORTVM_H_
#define _SUPPORTVM_H_
#include "../Algebra/GteMatrix.h"
#include "../Algebra/GteVector.h"
#include <algorithm>
using namespace gte;

//--- M : the number of examples ---
//--- N : the number of features --- 

template <unsigned M, unsigned N>
class svmClassifier
{
public:
	enum {LINEAR, RBF}

	void smoAlgorithm();
	int examineExample(int i2);
	double calcEk(int i);

	Matrix<M, M, double> Kernel;
	Matrix<M, N, double> dataSetIn;
	Vector<M, int> label;
	Vector<M, double> alpha;
	Vector<M, double> errorsCache;
	int C;
	double tolerance, b;
	int kernelType;

private:
	void selectI1(int &i1, double &E1, int i2, double E2);
	int takeStep(int i1, int i2, double E1, double E2);
	double kernelTransfer(int i1, int i2);
};


#include "supportvm.cpp"

#endif