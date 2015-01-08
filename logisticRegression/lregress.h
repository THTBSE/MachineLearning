#ifndef _LREGRESS_H_
#define _LREGRESS_H_
#include "../Algebra/GteMatrix.h"
#include "../Algebra/GteVector3.h"
#include <cstdio>
#include <fstream>
using namespace std;
using namespace gte;

//batch梯度上升法权值w的更新公式是
//matrixW = matrixW + alpha * matrixX.transpose() * (matrixLabel - matrixh)
//matrixX 是(m, n)矩阵，matrixLabel 与matrixh 都是(m, 1)矩阵
//m是样本个数，n是每个样本特征个数。
//权值matrixW 是(n,1)矩阵

template <unsigned M, unsigned N>
class logisticRegression
{
public:
	//初始化数据集
	void loadDataSet();

	//梯度上升法求权值w
	Matrix<N, 1, double> gradAscend();

	//随机梯度上升法求权值w
	Matrix<N, 1, double> stocGradAscend(int maxCycles);

	//测试分类器的准确性
	void testClassify();

	Matrix<M, N, double> data;
	Matrix<M, 1, double> label;
	Matrix<N, 1, double> weights;
private:
	//sigmoid函数
	double sigmoid(double z);

};


#include "lregress.cpp"

#endif