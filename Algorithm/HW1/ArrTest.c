#include <stdio.h>

void WriteDataIntoArr(int Arr[])
{
    for(int Index =0; Index < 100; ++Index)
        Arr[Index] = Index;
}

int main()
{
    int Arr[100] = {};

    WriteDataIntoArr(Arr);
    for(int Index = 0; Index < 100; ++Index)
        printf("%d ", Arr[Index]);
    printf("\n");

	return 0;
}

