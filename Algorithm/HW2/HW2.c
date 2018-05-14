#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#ifndef SAFE_FREE  
#define SAFE_FREE(Ptr) if(Ptr){\
                                  free(Ptr);\
								  Ptr = NULL;\
							  }
#endif  

int Comparison(const void *a, const void *b);
int **GetHeightFromStdin(int M, int N);
int CalcMaximumGrades(int **School);

int main(int argc, char **atgv)
{
	int M = 0, N = 0;
	if( 2 != scanf("%d %d", &M, &N) )
	{
		printf("Input error : invalid M or N\n");
		exit(0);
	}
	printf("M = %d, N = %d\n", M, N);
	int **Students = GetHeightFromStdin(M, N);
	
	int Grade = 0;
	for(; Grade < M; ++Grade)
	{
		int StudentIndex = 0;
		for(; StudentIndex < N; ++StudentIndex)
		{
			printf("%d ", Students[Grade][StudentIndex]);
		}
		printf("\n");
		SAFE_FREE(Students[Grade]);
	}
	SAFE_FREE(Students);

	return 0;
}

int Comparison(const void *a, const void *b)
{
	return *(int *)a - *(int *)b;
}

int **GetHeightFromStdin(int M, int N)
{
	int **Students = (int **)malloc(M * sizeof(int *));

	int Grade = 0;
	for(; Grade < M; ++Grade)
	{	
		Students[Grade] = (int *)malloc(N * sizeof(int));
		int StudentIndex = 0;
		for(; StudentIndex < N; ++StudentIndex)
		{
			if(1 != scanf("%d", &Students[Grade][StudentIndex]))
				printf("Error occured\n");
			printf("%d ", Students[Grade][StudentIndex]);
		}
		qsort(Students[Grade], N, sizeof(int), Comparison);
		printf("\n");
	}
	printf("==============\n");
	return Students;
}

int CalcMaximumGrades(int **School);
