#include "lregress.h"

template <unsigned M, unsigned N>
double logisticRegression<M,N>::sigmoid(double z)
{
	return 1 / (1 + exp(-z));
}

template <unsigned M, unsigned N>
void logisticRegression<M, N>::loadDataSet()
{
	ifstream input("logisticRegression\\horseColicTraining.txt");
	for (int i = 0; i < M; i++)
	{
		data(i, 0) = 1.0;
		for (int j = 1; j < N ; j++)
		{
			input >> data(i,j);
		}
		input >> label(i, 0);

	}
	input.close();
	//FILE *fp;
	//fopen_s(&fp, "logisticRegression\\testSet.txt", "r");
	//float x0, x1, y0;
	//int rowNumber = 0;
	//while (fscanf_s(fp, "%f %f %f", &x0,&x1,&y0) != EOF && rowNumber < M)
	//{
	//	Vector3<double> x(1.0, x0, x1);
	//	Vector<1, double> y;
	//	y[0] = y0;
	//	data.SetRow(rowNumber, x);
	//	label.SetRow(rowNumber,y);
	//	rowNumber++;
	//}
	//fclose(fp);
}

template <unsigned M, unsigned N>
Matrix<N, 1, double> logisticRegression<M, N>::gradAscend()
{
	Matrix<N, 1, double> weight;
	Vector<N, double> initial;
	initial.MakeOne();
	weight.SetCol(0, initial);

	double alpha = 0.001;
	int maxCycles = 500;

	for (int i = 0; i < 500; i++)
	{
		Matrix<M, 1, double> h;
		for (int j = 0; j < M; j++)
		{
			h[j] = sigmoid((data.GetRow(j) * weight)[0]);
		}
		Matrix<M, 1, double> error;
		error = label - h;
		weight = weight + alpha * Transpose(data) * error;
	}
	return weight;
}

template <unsigned M, unsigned N>
Matrix<N, 1, double> logisticRegression<M, N>::stocGradAscend(int maxCycles)
{
	Matrix<N, 1, double> weight;
	Vector<N, double> initial;
	initial.MakeOne();
	weight.SetCol(0, initial);
	Matrix<N, 1, double> xi;
	double alpha = 0.001;

	for (int t = 0; t < maxCycles; t++)
		for (int i = 0; i < M; i++)
		{
			xi.SetCol(0, data.GetRow(i));
			auto h = sigmoid((data.GetRow(i)*weight)[0]);
			weight = weight + alpha * (label[i] - h) * xi;
		}
	return weight;
}

template <unsigned M, unsigned N>
void logisticRegression<M, N>::testClassify()
{
	int miss = 0; 
	float total = M;
	for (int i = 0; i < M; i++)
	{
		auto h = sigmoid((data.GetRow(i) * weights)[0]);
		if (fabs(label[i] - h) > 0.5)
		{
			miss++;
		}
	}
	float rate = (float)miss / total;
	printf("The error rate is : %f", rate);
}