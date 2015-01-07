#include "lregress.h"

int main()
{
	logisticRegression lr;
	lr.loadDataSet();

	lr.weights = lr.gradAscend();
	lr.testClassify();
	while (true)
	{

	}
}