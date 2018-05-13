#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#ifndef SAFE_FREE  
#define SAFE_FREE(Ptr) if(Ptr){\  
                                  free(Ptr);\  
								  Ptr = NULL;\
							  }  
#endif  

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
	int **Students = GetHeightFromStdin(M, N);
	
	int Grade = 0;
	for(; Grade < M; ++Grade)
		SAFE_FREE(Students[Grade]);
	SAFE_FREE(Students);

	return 0;
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
				print("Error occured\n");
			printf("%d ", Students[Grade][StudentIndex]);
		}
		printf("\n");
	}
	return Students;
}

int CalcMaximumGrades(int **School);
