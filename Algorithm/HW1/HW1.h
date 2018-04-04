#ifndef HW1_HEADER
#define HW1_HEADER

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifndef SAFE_FREE
#define SAFE_FREE(Ptr) if(Ptr)\
				  {\
				  	   free(Ptr);\
					   Ptr = NULL;\
				  }
#endif

int *GetSequenceFromStdin(int *CancerIndex);
int CalcMaximumSubsequenceSum(int *IntArr, int StartIndex);

#endif
