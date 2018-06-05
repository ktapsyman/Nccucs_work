#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>

#ifndef SAFE_FREE  
#define SAFE_FREE(Ptr) if(Ptr){\
                                  free(Ptr);\
								  Ptr = NULL;\
							  }
#endif  

typedef struct Node
{
	int Id;
	int Color;
	bool Visited;
	struct Node *Next;
}Node;

Node **GetNodes(int M, int N);
int CalcConnectedArea(Node **Matrix, int M, int N, int Row, int Col);

int main(int argc, char **atgv)
{
	int M = 0, N = 0;
	if(2 != scanf("%d %d", &M, &N))
	{
		printf("Input error : invalid M or N\n");
		exit(0);
	}
	
	Node **Matrix = GetNodes(M, N);
	if(!Matrix)
		return 0;	
	
	int Row = 0;
	int MaxArea = 0;
	for(Row = 0; Row < M; ++Row)
	{
		int Col = 0;
		for(; Col < N; ++Col)
		{
			if(Matrix[Row][Col].Visited)
				continue;
			
			int Area = CalcConnectedArea(Matrix, M, N, Row, Col);
			if(Area > MaxArea)
				MaxArea = Area;
		}
	}
	printf("%d\n", MaxArea);
	for(Row = 0; Row < M; ++Row)
		SAFE_FREE(Matrix[Row]);
	SAFE_FREE(Matrix);
	return 0;
}

Node **GetNodes(int M, int N)
{
	Node **Matrix = (Node **)malloc(M * sizeof(Node *));
	if(!Matrix)
	{
		printf("Error : malloc failed.\n");
		return 0;
	}

	int Row = 0;
	for(; Row < M; ++Row)
	{
		Matrix[Row] = (Node *)malloc(N * sizeof(Node));
		if(!Matrix[Row])
		{
			int CleanRange = Row;
			for(Row = 0; Row < CleanRange; ++Row)
				SAFE_FREE(Matrix[Row]);
			SAFE_FREE(Matrix);
			printf("Error : malloc failed.\n");
			return NULL;
		}
		int Col = 0;
		for(; Col < N; ++Col)
		{
			int Color = -1;
			if(1 != scanf("%d", &Color))
			{
				int CleanRange = Row;
				for(Row = 0; Row <= CleanRange; ++Row)
					SAFE_FREE(Matrix[Row]);
				SAFE_FREE(Matrix);
				printf("Error occured : invalid Color\n");
				return NULL;
			}
			Matrix[Row][Col].Id = N*Row+Col;
			Matrix[Row][Col].Visited = false;
			Matrix[Row][Col].Color = Color;
		}
	}
	
	return Matrix;
}

int CalcConnectedArea(Node **Matrix, int M, int N, int Row, int Col)
{
	if(Matrix[Row][Col].Visited)
		return 0;
	Matrix[Row][Col].Visited = true;
	int CurrentColor = Matrix[Row][Col].Color;	

	int Area = 1;
	
	if(Row != 0 && (CurrentColor == Matrix[Row-1][Col].Color))
	{
		Area += CalcConnectedArea(Matrix, M, N, Row-1, Col);
	}

	if(Col != 0 && (CurrentColor == Matrix[Row][Col-1].Color))
	{
		Area += CalcConnectedArea(Matrix, M, N, Row, Col-1);
	}

	if(Row != M-1 && (CurrentColor == Matrix[Row+1][Col].Color))
	{
		Area += CalcConnectedArea(Matrix, M, N, Row+1, Col);
	}
	
	if(Col != N-1 && (CurrentColor == Matrix[Row][Col+1].Color))
	{
		Area += CalcConnectedArea(Matrix, M, N, Row, Col+1);
	}

	return Area;
}	

