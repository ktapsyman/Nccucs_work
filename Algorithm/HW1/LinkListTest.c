#include "HW1.h"
#include "LinkedList.h"

int main(int argc, char **argv)
{
	Node *Head = CreateNode(3);
	int ValueArr[] = {-2, -3, 3, 2, -3, 2, -1};
	for(int Index = 0; Index < 7; ++Index)
		Append(Head, CreateNode(ValueArr[Index]));
	
	DumpList(Head);
	
	Head = DeleteNodeByValue(Head, 3);
	DumpList(Head);
	Head = DeleteNodeByValue(Head, -2);
	DumpList(Head);
	Head = DeleteNodeByValue(Head, -1);
	DumpList(Head);

	while(Head)
	{
		Node *Next = Head->Next;
		SAFE_FREE(Head);
		Head = Next;
	}
	return 0;
}

