#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <limits.h>

#ifndef SAFE_FREE
#define SAFE_FREE(Ptr) if(Ptr){\
                                  free(Ptr);\
                                  Ptr = NULL;\
                              }
#endif


int *GetSequenceFromStdin();
int CalcMaximumSubSeq(int *Seq);

int main(int argc, char **argv)
{
    int *Seq = GetSequenceFromStdin();
    int MaxSub = CalcMaximumSubSeq(Seq);
    int Index;
    int SeqSum = 0;
    for(Index = 1; Index <= Seq[0]; ++Index)
    {
        SeqSum += Seq[Index];
        Seq[Index] *= -1;
    }
    int WrappedMaxSubSeqSum = SeqSum + CalcMaximumSubSeq(Seq);
    MaxSub = MaxSub > WrappedMaxSubSeqSum ? MaxSub : WrappedMaxSubSeqSum;
    printf("%d\n", MaxSub);
    SAFE_FREE(Seq);
    return 0;
}

int *GetSequenceFromStdin()
{
    int CurrentLen = 1001;
    int InputBuf = 0;
    int *Seq = (int *)malloc(CurrentLen*sizeof(int));

    Seq[0] = 0;//Stores length of the seq
    while(/*fgets(StrBuf, sizeof(StrBuf), stdin)*/1 == scanf("%d", &InputBuf))
    {
        if(0 == Seq[0])
        {
            Seq[0]++;
            Seq[Seq[0]] = InputBuf;
        }
        else
        {
            Seq[0]++;
            if( Seq[0] == CurrentLen )
            {
                CurrentLen += 1000;
                int *ReallocTmp = (int *)realloc(Seq, CurrentLen*sizeof(int));
                if(!ReallocTmp)
                {
                    printf("Memory Error!\n");
                    SAFE_FREE(Seq);
                    exit(0);
                }
                Seq = ReallocTmp;
            }
            Seq[Seq[0]] = InputBuf;
        }
    }

    return Seq;
}

int CalcMaximumSubSeq(int *Seq)
{
    int SeqLen = Seq[0];
    int SuffixMax = 0;
    int GlobalMax = 0;
    int Index;
    for(Index = 1; Index < SeqLen; ++Index)
    {
        if(SuffixMax + Seq[Index ] > GlobalMax)
        {
            SuffixMax += Seq[Index ];
            GlobalMax = SuffixMax;
        }
        else if( SuffixMax + Seq[Index ] > SuffixMax )
        {
            SuffixMax += Seq[Index ];
        }
        else
        {
            SuffixMax = SuffixMax+Seq[Index ] > 0 ? SuffixMax+Seq[Index ] : 0;
        }
    }
    return GlobalMax;
}
