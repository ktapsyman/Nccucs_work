#include <stdlib.h>

typedef struct Node Node;

struct Node
{
	int Val;
	Node *Next;
};

Node *CreateNode(int Val);
Node *Append(Node *Head, Node *NewNode);
Node *Insert(Node *Head, Node *Previous, Node *NewNode);
Node *DeleteNodeByValue(Node *Head, int Val);
void SearchList(Node *Head, int Val);
void DumpList(Node *Head);
