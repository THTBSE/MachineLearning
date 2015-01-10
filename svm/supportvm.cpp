#include "supportvm.h"

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
	auto E1 = errorsCache[i1];
	auto r1 = E1 * y1;

	//if violate KKT condition 
	if ((r1 < tolerance && alpha1 < C) || (r1 > tolerance && alpha1 > 0))
	{
		int numOfNonbound = 0;
		for (int i = 0; i < M; i++)
		{
			if (0 < alpha[i] && alpha[i] < C)
				numOfNonbound++;
		}
		if (numOfNonbound > 1)
		{
			int i2; double E2;
			selectI1(i2, E2, i1, E1);
			if (takeStep(i1, i2, E1, E2))
				return 1;
		}


	}
	return 0;
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
	return sum - (double)label[i];
}

template <unsigned M, unsigned N>
void svmClassifier<M, N>::selectI1(int &i2, double &E2, int i1, double E1)
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
	auto y2 = laber[i2];
	auto s = y1 * y2;
	double a1, a2;

	double L, H;
	if (y1 != y2)
	{
		L = std::max(0, alpha2 - alpha1);
		H = std::min(C, C + alpha2 - alpha1);
	}
	else
	{
		L = std::max(0, alpha1 + alpha2 - C);
		H = std::min(C, alpha1 + alpha2);
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
	const double sigma = 1.3;
	double K = 0;
	if (kernelType == LINEAR)
	{
		K = Dot(dataSetIn.GetRow(i1), dataSetIn.GetRow(i2));
	}
	else if (kernelType == RBF)
	{
		auto L = Length(dataSetIn.GetRow(i1) - dataSetIn.GetRow(i2));
		K = exp(-(K*K) / (2 * sigma*sigma));
	}
	return K;
}