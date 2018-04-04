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

#ifndef POSITIVE
#define POSITIVE 1
#endif
#ifndef NEGATIVE
#define NEGATIVE !POSITIVE
#endif

int *GetSequenceFromStdin(int *CancerIndex);
int CalcMaximumSubSeq(int *Seq, int CancerIndex);

int main(int argc, char **argv)
{
    int CancerIndex = 0;
    int *Seq = GetSequenceFromStdin(&CancerIndex);
    int MaxSub = CalcMaximumSubSeq(Seq, CancerIndex);
    printf("%d\n", MaxSub);
    SAFE_FREE(Seq);
    return 0;
}

int *GetSequenceFromStdin(int *CancerIndex)
{
    int CurrentLen = 1001;
    int InputBuf = 0;
    int Sign;
    int CurrentMin = INT_MAX;
    int *Seq = (int *)malloc(CurrentLen*sizeof(int));

    Seq[0] = 0;//Stores length of the seq
    while(/*fgets(StrBuf, sizeof(StrBuf), stdin)*/1 == scanf("%d", &InputBuf))
    {   
        if(0 == Seq[0])
        {   
            Sign = InputBuf > 0 ? POSITIVE : NEGATIVE;
            Seq[0]++;
            Seq[Seq[0]] = InputBuf;
			if(Sign == NEGATIVE)
			{
				CurrentMin = InputBuf;
				*CancerIndex = Seq[0];
			}
        }
        else
        {   
            if(Sign == POSITIVE && InputBuf > 0)
            {   
                Seq[Seq[0]] += InputBuf;
            }
            else if(Sign == NEGATIVE && InputBuf <= 0)
            {   
                Seq[Seq[0]] += InputBuf;
                if(Seq[Seq[0]] < CurrentMin)
                {   
                    CurrentMin = Seq[Seq[0]];
                    *CancerIndex = Seq[0];
                }
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
                Sign = InputBuf > 0 ? POSITIVE : NEGATIVE;
                Seq[Seq[0]] = InputBuf;
                if(Sign == NEGATIVE && Seq[Seq[0]] < CurrentMin)
                { 
                    CurrentMin = Seq[Seq[0]];
                    *CancerIndex = Seq[0];
                }
            }
        }
    }
	if( Seq[0] >= 2 )
	{
		if( Seq[1]*Seq[Seq[0]] >= 0 )
		{
			Seq[1] += Seq[Seq[0]];
			--Seq[0];
		}
	}
    return Seq;
}

int CalcMaximumSubSeq(int *Seq, int CancerIndex)
{
    int SeqLen = Seq[0];
    int SuffixMax = 0;
    int GlobalMax = 0;
    int Index;
    for(Index = CancerIndex; Index < SeqLen+CancerIndex; ++Index)
    {
		int IndexPadded = Index % SeqLen + 1;
		printf("Suffix : %d,  Seq : %d, GlobalMax : %d\n", SuffixMax, Seq[IndexPadded], GlobalMax);
        if(SuffixMax + Seq[IndexPadded] > GlobalMax)
        {
            SuffixMax += Seq[IndexPadded];
            GlobalMax = SuffixMax;
        }
        else if( SuffixMax + Seq[IndexPadded] > SuffixMax )
        {
            SuffixMax += Seq[IndexPadded];
        }
        else
        {
            SuffixMax = SuffixMax+Seq[IndexPadded] > 0 ? SuffixMax+Seq[IndexPadded] : 0;
        }
    }
    return GlobalMax;
}

