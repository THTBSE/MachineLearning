#include "lregress.h"



int main()
{
	logisticRegression<299,22> lr;
	lr.loadDataSet();

	lr.weights = lr.stocGradAscend(300);
	lr.testClassify();
	while (true)
	{

	}
}