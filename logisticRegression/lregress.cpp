#include "lregress.h"

double 
logisticRegression::sigmoid(double z)
{
	return 1 / (1 + exp(-z));
}

void
logisticRegression::loadDataSet()
{
	FILE *fp;
	fopen_s(&fp, "logisticRegression\\testSet.txt", "r");
	float x0, x1, y0;
	int rowNumber = 0;
	while (fscanf_s(fp, "%f %f %f", &x0,&x1,&y0) != EOF)
	{
		Vector3<double> x(1.0, x0, x1);
		Vector<1, double> y;
		y[0] = y0;
		data.SetRow(rowNumber, x);
		label.SetRow(rowNumber,y);
		rowNumber++;
	}
	fclose(fp);
}

Matrix<3, 1, double> 
logisticRegression::gradAscend()
{
	Matrix<3, 1, double> weights;
	weights.SetCol(0, Vector3<double>(1.0, 1.0, 1.0));

	double alpha = 0.001;
	int maxCycles = 500;

	for (int i = 0; i < 500; i++)
	{
		Matrix<100, 1, double> h;
		for (int j = 0; j < 100; j++)
		{
			h[j] = sigmoid((data.GetRow(j) * weights)[0]);
		}
		Matrix<100, 1, double> error;
		error = label - h;
		weights = weights + alpha * Transpose(data) * error;
	}
	return weights;
}

void
logisticRegression::testClassify()
{
	int miss = 0; 
	float total = 100;
	for (int i = 0; i < 100; i++)
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