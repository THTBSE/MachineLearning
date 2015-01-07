#ifndef _LREGRESS_H_
#define _LREGRESS_H_
#include "../Algebra/GteMatrix.h"
#include "../Algebra/GteVector3.h"
#include <cstdio>
#include <fstream>
using namespace gte;

class logisticRegression
{
public:
	//初始化数据集
	void loadDataSet();

	//梯度上升法求权值w
	Matrix<3, 1, double> gradAscend();

	Matrix<100, 3, double> data;
	Matrix<100, 1, double> label;
private:
	//sigmoid函数
	double sigmoid(double z);

};




#endif