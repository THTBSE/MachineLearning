#include "lregress.h"

int main()
{
	logisticRegression lr;
	lr.loadDataSet();

	auto w = lr.gradAscend();
	while (true)
	{

	}
}