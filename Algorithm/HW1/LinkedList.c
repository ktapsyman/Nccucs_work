#include "LinkedList.h"
#include "HW1.h"

Node *CreateNode(int Val)
{
	Node *NewNode = (Node *)malloc(sizeof(Node));
	if(!NewNode)
	{
		printf("Memory error, failed to alloc\n");
		return NULL;
	}
	
	NewNode->Val = Val;
	NewNode->Next = NULL;
	return NewNode;
}

Node *Append(Node *Head, Node *NewNode)
{
	if(!Head)
	{
		Head = NewNode;
	}
	else
	{
		Node *CurrentNode = Head;
		while(CurrentNode->Next)
		{
			CurrentNode = CurrentNode->Next;
		}
		CurrentNode->Next = NewNode;
	}
	return Head;
}

Node *Insert(Node *Head, Node *Previous, Node *NewNode)
{
	if(!Head)
	{
		Head = NewNode;
	}
	if(!Previous)
	{
		Head->Next = NewNode;
	}
	else
	{
		NewNode->Next = Previous->Next;
		Previous->Next = NewNode;
	}
	return Head;
}

Node *DeleteNodeByValue(Node *Head, int Val)
{
	if(!Head)
	{
		printf("List is empty, no target to delete\n");
		return Head;
	}
	if(Val == Head->Val)
	{
		Node *Target = Head;
		Head = Head->Next;
		SAFE_FREE(Target);
	}
	else
	{
		Node *CurrentNode = Head;
		while(CurrentNode->Next && CurrentNode->Next->Val != Val)
		{
			CurrentNode = CurrentNode->Next;
		}
		if(CurrentNode->Next)
		{
			Node *Target = CurrentNode->Next;
			CurrentNode->Next = Target->Next;
			SAFE_FREE(Target);
		}
	}

	return Head;
}

void SearchList(Node *Head, int Val)
{
	Node *CurrentNode = Head;
	while(CurrentNode)
	{
		if(Val == CurrentNode->Val)
		{
			printf("Value %d exists in list\n", Val);
		}
		CurrentNode = CurrentNode->Next;
	}
}

void DumpList(Node *Head)
{
	Node *CurrentNode = Head;
	while(CurrentNode)
	{
		printf("%d  ", CurrentNode->Val);
		CurrentNode = CurrentNode->Next;
	}
	printf("\n");
}

