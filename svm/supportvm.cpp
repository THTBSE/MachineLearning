#include "supportvm.h"

template <unsigned M, unsigned N>
void svmClassifier<M, N>::loadDataSet()
{
	std::ifstream input("testSetRBF.txt");
	for (int i = 0; i < M; i++)
	{
		for (int j = 0; j < N; j++)
		{
			input >> dataSetIn(i, j);
		}
		input >> label[i];
	}
	input.close();
}

template <unsigned M, unsigned N>
void svmClassifier<M, N>::svmTrain(int c, double tol, int ktype, double sig)
{
	C = c;
	tolerance = tol;
	kernelType = ktype;
	sigma = sig;
	alpha.MakeZero();
	b = 0;
	
	for (int i = 0; i < M; i++)
	{
		for (int j = 0; j < M; j++)
		{
			Kernel(i, j) = kernelTransfer(i, j);
		}
		errorsCache[i] = -label[i];
	}

	smoAlgorithm();
}

template <unsigned M, unsigned N>
void svmClassifier<M, N>::testSet()
{
	std::ifstream input("testSetRBF2.txt");
	int errors = 0;
	//for (int i = 0; i < M; i++)
	//{
	//	int ret = svmPredict(dataSetIn.GetRow(i));
	//	if (ret != (int)label[i])
	//		errors++;
	//}
	for (int i = 0; i < M; i++)
	{
		Vector<N, double> x;
		input >> x[0] >> x[1];
		double y;
		input >> y;

		int ret = svmPredict(x);
		if (ret != (int)y)
			errors++;
	}
	input.close();
	double rate = (double)errors / (double)M;

	int see = 1;
}

template <unsigned M, unsigned N>
void svmClassifier<M, N>::smoAlgorithm()
{
	int numChanged = 0;
	bool examineAll = true;
	while (numChanged > 0 || examineAll)
	{
		numChanged = 0;
		if (examineAll)
		{
			for (int i = 0; i < M; i++)
			{
				numChanged += examineExample(i);
			}
		}
		else
		{
			for (int i = 0; i < M; i++)
			{
				if (0 < alpha[i] && alpha[i] < C)
				{
					numChanged += examineExample(i);
				}
			}
		}
		if (examineAll)
			examineAll = false;
		else if (numChanged == 0)
			examineAll = true;
	}
}

template <unsigned M, unsigned N>
int svmClassifier<M, N>::examineExample(int i1)
{
	auto y1 = label[i1];
	auto alpha1 = alpha[i1];
	auto E1 = calcEk(i1);
	auto r1 = E1 * y1;

	//if violate KKT condition 
	if ((r1 < tolerance && alpha1 < C) || (r1 > tolerance && alpha1 > 0))
	{
		int i2; double E2;
		std::vector<int> nonBound;
		for (int i = 0; i < M; i++)
		{
			if (0 < alpha[i] && alpha[i] < C)
				nonBound.push_back(i);
		}
		if (nonBound.size() > 1)
		{
			selectI2(i2, E2, i1, E1);
			if (takeStep(i1, i2, E1, E2))
				return 1;
		}

		//loop over all non-zero and non-C alpha, starting at a random point
		if (!nonBound.empty())
		{
			while (true)
			{
				i2 = nonBound[rand() % nonBound.size()];
				if (i2 != i1)
					break;
			}
			E2 = calcEk(i2);
			if (takeStep(i1, i2, E1, E2))
				return 1;
		}

		for (int i = 0; i < M; i++)
		{
			if (i == i1)
				continue;

			i2 = i;
			E2 = calcEk(i2);
			if (takeStep(i1, i2, E1, E2))
				return 1;
			break;
		}

	}
	return 0;
}

template <unsigned M, unsigned N>
int svmClassifier<M, N>::svmPredict(const Vector<N, double> &x)
{
	double sum = 0.0;
	for (int i = 0; i < M; i++)
	{
		if (alpha[i] > 0)
		{
			sum += alpha[i] * label[i] * kernerlTrans(dataSetIn.GetRow(i), x);
		}
	}
	sum += b;
	if (sum > 0)
		return 1;
	else
		return -1;
}

template <unsigned M, unsigned N>
int svmClassifier<M, N>::svmOutput(int i)
{
	double sum = 0.0;
	for (int j = 0; j < M; j++)
	{
		if (alpha[j] > 0)
		{
			sum += alpha[j] * label[j] * Kernel(j, i);
		}
	}
	sum += b;

	if (sum > 0)
		return 1;
	else
		return -1;
}
template <unsigned M, unsigned N>
double svmClassifier<M, N>::calcEk(int i)
{
	double sum = 0.0;
	for (int j = 0; j < M; j++)
	{
		if (alpha[j] > 0)
		{
			sum += alpha[j] * label[j] * Kernel(j, i);
		}
	}
	sum += b;
	return sum - label[i];
}

template <unsigned M, unsigned N>
void svmClassifier<M, N>::selectI2(int &i2, double &E2, int i1, double E1)
{
	if (E1 > 0)
	{
		E2 = std::numeric_limits<double>::max();
		for (int i = 0; i < M; i++)
		{
			if (i == i1)
				continue;
			if (errorsCache[i] < E2)
			{
				E2= errorsCache[i];
				i2 = i;
			}
		}
	}
	else
	{
		E2 = std::numeric_limits<double>::min();
		for (int i = 0; i < M; i++)
		{
			if (i == i1)
				continue;
			if (errorsCache[i] > E2)
			{
				E2 = errorsCache[i];
				i2 = i;
			}
		}
	}
}

template <unsigned M, unsigned N>
int svmClassifier<M, N>::takeStep(int i1, int i2, double E1, double E2)
{
	auto alpha1 = alpha[i1];
	auto alpha2 = alpha[i2];
	auto y1 = label[i1];
	auto y2 = label[i2];
	auto s = y1 * y2;
	double a1, a2;

	double L, H;
	if (y1 != y2)
	{
		L = std::max(0.0, alpha2 - alpha1);
		H = std::min((double)C, (double)(C + alpha2 - alpha1));
	}
	else
	{
		L = std::max(0.0, (double)(alpha1 + alpha2 - C));
		H = std::min((double)C, (double)(alpha1 + alpha2));
	}

	if (L == H)
		return 0;
	auto K11 = Kernel(i1, i1);
	auto K22 = Kernel(i2, i2);
	auto K12 = Kernel(i1, i2);

	auto eta = K11 + K22 - 2 * K12;
	if (eta > 0)
	{
		a2 = alpha2 + y2 * (E1 - E2) / eta;
		if (a2 < L)
			a2 = L;
		else if (a2 > H)
			a2 = H;
	}
	else
	{
		return 0;
	}

	if (fabs(a2 - alpha2) < tolerance * (a2 + alpha2 + tolerance))
		return 0;

	a1 = alpha1 + s * (alpha2 - a2);
	alpha[i1] = a1;
	alpha[i2] = a2;

	auto b1 = -E1 - y1*K11*(a1 - alpha1) - y2*K12*(a2 - alpha2) + b;
	auto b2 = -E2 - y1*K12*(a1 - alpha1) - y2*K22*(a2 - alpha2) + b;

	if (0 < a1 && a1 < C)
		b = b1;
	else if (0 < a2 && a2 < C)
		b = b2;
	else
		b = 0.5 * (b1 + b2);

	errorsCache[i1] = calcEk(i1);
	errorsCache[i2] = calcEk(i2);
	return 1;
}

template <unsigned M, unsigned N>
double svmClassifier<M, N>::kernelTransfer(int i1, int i2)
{
	double K = 0;
	if (kernelType == SVM_LIN)
	{
		K = Dot(dataSetIn.GetRow(i1), dataSetIn.GetRow(i2));
	}
	else if (kernelType == SVM_RBF)
	{
		auto L = Length(dataSetIn.GetRow(i1) - dataSetIn.GetRow(i2));
		K = exp(-(L*L) / (2 * sigma*sigma));
	}
	return K;
}

template <unsigned M, unsigned N>
double svmClassifier<M, N>::kernerlTrans(const Vector<N, double> &xi, const Vector<N, double> &x)
{
	double K = 0;
	switch (kernelType)
	{
	case (int)SVM_LIN:
	{
		K = Dot(xi, x);
	}
		break;
	case (int)SVM_RBF:
	{
		auto L = Length(xi - x);
		K = exp(-(L*L) / (2 * sigma*sigma));
	}
		break;
	default:
		break;
	}
	return K;
}