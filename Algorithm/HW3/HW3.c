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
	int X;
	int Y;
	int DistFromStartNode;
	bool Visited;
	struct Node *Next;
}Node;

Node *CreateNode(int Id, int X, int Y);
Node **GetBridges(int N);
int Pop(Node *Head);
bool IsAbleToJump(Node *A, Node *B);
Node *AppendNode(Node *Head, Node *AdjacentVertex);
int BFS(Node **AdjacencyList, int BridgeCount, int TargetId);
void ShowList(Node *Head);
void CleanList(Node *Head);

int main(int argc, char **atgv)
{
	int N = 0;
	if(1 != scanf("%d", &N))
	{
		printf("Input error : invalid N\n");
		exit(0);
	}
	
	Node **AdjacentList = GetBridges(N);
	if(!AdjacentList)
	{
		printf("Error : malloc failed.\n");
		return 0;
	}
	
	printf("%d\n", BFS(AdjacentList, N, N-1));
	
	int BridgeIndex = 0;
	for(; BridgeIndex < N; ++BridgeIndex)
		CleanList(AdjacentList[BridgeIndex]);
	SAFE_FREE(AdjacentList);
	return 0;
}

Node *CreateNode(int Id, int X, int Y)
{
	Node *NewNode = (Node *)malloc(sizeof(Node));
	if(!NewNode)
	{
		printf("Error : malloc failed.\n");
		return NULL;
	}
	NewNode->Id = Id;
	NewNode->X = X;
	NewNode->Y = Y;
	NewNode->DistFromStartNode = 0;
	NewNode->Visited = false;
	NewNode->Next = NULL;
	
	return NewNode;
}

Node **GetBridges(int N)
{
	Node **Bridges = (Node **)malloc(N * sizeof(Node *));
	if(!Bridges)
	{
		printf("Error : malloc failed.\n");
		return NULL;
	}

	int BridgeIndex = 0;
	for(; BridgeIndex < N; ++BridgeIndex)
	{
		int X = 0;
		int Y = 0;
		if(2 != scanf("%d %d", &X, &Y))
		{
			printf("Error occured : invalid X Y\n");
			exit(1);
		}
		Node *NewBridge = CreateNode(BridgeIndex, X, Y);
		Bridges[BridgeIndex] = NewBridge;

		int PreviousIndex = 0;
		for(; PreviousIndex < BridgeIndex; ++PreviousIndex)
		{
			if(IsAbleToJump(Bridges[PreviousIndex], NewBridge))
			{
				AppendNode(Bridges[PreviousIndex], CreateNode(BridgeIndex, 0, 0));
				AppendNode(Bridges[BridgeIndex], CreateNode(PreviousIndex, 0, 0));
			}
		}	
	}
	return Bridges;
}

Node *AppendNode(Node *Head, Node *AdjacentVertex)
{
	if(!Head)
		return AdjacentVertex;
	
	Node *Current = Head;
	while(Current->Next)
	{
		Current = Current->Next;
	}
	Current->Next = AdjacentVertex;

	return Head;
}

int BFS(Node **AdjacencyList, int BridgeCount, int TargetId)
{
	Node *Queue = CreateNode(0, 0, 0);
	AdjacencyList[0]->Visited = true;

	//printf("Traversed : %d Dist : %d\n", 0, 0);
	while(Queue)
	{
		Node *Head = AdjacencyList[Queue->Id];
		Node *Tmp = Queue;
		Queue = Queue->Next;
		SAFE_FREE(Tmp);
		int CurrentDist = Head->DistFromStartNode;
		while(Head)
		{
			if(!AdjacencyList[Head->Id]->Visited)
			{
				//printf("Traversed : %d Dist : %d\n", Head->Id, CurrentDist+1);
				AdjacencyList[Head->Id]->Visited = true;
				AdjacencyList[Head->Id]->DistFromStartNode = CurrentDist+1;
				Queue = AppendNode(Queue, CreateNode(Head->Id, 0, 0));
			}
			Head = Head->Next;
		}
		
		if(AdjacencyList[TargetId]->Visited)
			return AdjacencyList[TargetId]->DistFromStartNode;
		
		
	}
	return -1;
}

void CleanList(Node *Head)
{
	if(!Head)
		return;
	CleanList(Head->Next);
	SAFE_FREE(Head);
}

void ShowList(Node *Head)
{
	printf("List : ");
	Node *Current = Head;
	while(Current)
	{
		printf("%d ", Current->Id);
		Current = Current->Next;
	}
	printf("\n");
}

bool IsAbleToJump(Node *A, Node *B)
{
	return (A->Y > B->X) && (B->Y > A->X);
}

