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

typedef struct
{
	int Id;
	int MaxPossibleGrades;
	int *GreaterThan;
	int GreaterThanCount;
	bool IsTraversed;
}GraphNode;

int HeightComparison(const void *a, const void *b);
int GradeComparison(int *GradeA, int *GradeB, int Length);
int **GetHeightFromStdin(int M, int N);
int GetMaxDepthOfNode(GraphNode **Graph, GraphNode *Node);

//For Debug
void ShowStudents(int *Students, int StudentsCount)
{
	int Index = 0;
	for(; Index < StudentsCount; ++Index)
		printf("%d ", *(Students+Index));
	printf("\n");
}

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
	GraphNode **StudentGraph = (GraphNode **)malloc(M*sizeof(GraphNode*));
	for(; Grade < M; ++Grade)
	{
		//ShowStudents(Students[Grade], N);

		GraphNode *Node = (GraphNode *)malloc(sizeof(GraphNode));
		Node -> Id = Grade;
		Node -> MaxPossibleGrades = 0;
		Node -> GreaterThanCount = M;
		Node -> GreaterThan = (int *)malloc(M*sizeof(int));
		int Index = 0;
		for(; Index < M; ++Index)
			Node -> GreaterThan[Index] = M+1;
		Node -> IsTraversed = false;
		StudentGraph[Grade] = Node;
	}

	for(Grade = 0; Grade < M; ++Grade)
	{
		int LocalMaxPhotoGrades = 0;
		int OtherGrades = 0;
		for(; OtherGrades < M; ++OtherGrades)
		{
			if(GradeComparison(Students[Grade], Students[OtherGrades], N) == 1)
			{
				StudentGraph[Grade] -> GreaterThan[LocalMaxPhotoGrades] = OtherGrades;
				LocalMaxPhotoGrades += 1;
			}
		}
	}
	int MaxPhotoGrades = 0;
	for(Grade = 0; Grade < M; ++Grade)
	{
		int MaxDepthOfNode = GetMaxDepthOfNode(StudentGraph, StudentGraph[Grade]);
		if(MaxDepthOfNode > MaxPhotoGrades)
			MaxPhotoGrades = MaxDepthOfNode;
	}
	printf("%d\n", MaxPhotoGrades);
	for(; Grade < M; ++Grade)
	{
		SAFE_FREE(Students[Grade]);
		SAFE_FREE(StudentGraph[Grade]->GreaterThan);
		SAFE_FREE(StudentGraph[Grade]);
	}
	SAFE_FREE(StudentGraph);
	SAFE_FREE(Students);

	return 0;
}

int HeightComparison(const void *a, const void *b)
{
	return *(int *)a - *(int *)b;
}

int GradeComparison(int *GradeA, int *GradeB, int Length)//assume two arrs have the same length
{
	int Index = 0;
	int Diff = 0;
	int AbsDiff = 0;
	for(; Index < Length; ++Index)
	{
		if(GradeA[Index] == GradeB[Index])
			return 0;
		Diff += (GradeA[Index] - GradeB[Index]);
		AbsDiff += abs(GradeA[Index] - GradeB[Index]);
	}
	if(Diff == AbsDiff)
	{
		return 1;
	}
	else if(Diff == -AbsDiff)
	{
		return -1;
	}
	else
	{ 
		return 0;
	}
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
		}
		qsort(Students[Grade], N, sizeof(int), HeightComparison);
	}
	return Students;
}

int GetMaxDepthOfNode(GraphNode **Graph, GraphNode *Node)
{
	if(Node -> IsTraversed)
		return Node -> MaxPossibleGrades;
	Node -> IsTraversed = true;
	int Index = 0;
	int MaxDepthOfSubgraph = 0;
	for(; Index < Node -> GreaterThanCount && Node->GreaterThan[Index] != Node -> GreaterThanCount+1; ++Index)
	{
		int LocalMaxDepth = GetMaxDepthOfNode(Graph, Graph[Node->GreaterThan[Index]]);
		if(LocalMaxDepth > MaxDepthOfSubgraph)
			MaxDepthOfSubgraph = LocalMaxDepth;
	}
	Node -> MaxPossibleGrades = 1 + MaxDepthOfSubgraph;
	
	return Node -> MaxPossibleGrades;
}
