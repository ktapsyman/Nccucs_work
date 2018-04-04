#include "HW1.h"

#ifndef POSITIVE
#define POSITIVE 1
#endif
#ifndef NEGATIVE
#define NEGATIVE !POSITIVE
#endif

int main(int argc, char **argv)
{
	int CancerIndex;
	int *Seq = GetSequenceFromStdin(&CancerIndex);
	int Max = CalcMaximumSubsequenceSum(Seq, CancerIndex);
	printf("%d\n", Max);
	SAFE_FREE(Seq);
	return 0;
}

int *GetSequenceFromStdin(int *CancerIndex)
{
	int CurrentLen = 1001;
	int InputBuf = 0;
	int Sign;
	int CurrentMin = 0;
	int *Seq = (int *)malloc(CurrentLen*sizeof(int));
	char StrBuf[4] = {};

	Seq[0] = 0;//For saving length
	while(fgets(StrBuf, sizeof(StrBuf), stdin))
	{
		sscanf(StrBuf, "%d\n", &InputBuf);
		if(0 == Seq[0])
		{
			Sign = InputBuf > 0 ? POSITIVE : NEGATIVE;
			Seq[0]++;
			Seq[Seq[0]] = InputBuf;
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
	return Seq;
}

int CalcMaximumSubsequenceSum(int *Seq, int StartIndex)
{
	int SeqLen = Seq[0];
	int SuffixMax = 0;
	int GlobalMax = 0;
	for(int Index = StartIndex; Index < SeqLen+StartIndex; ++Index)
	{
		if(SuffixMax + Seq[Index % SeqLen + 1] > GlobalMax)
		{
			SuffixMax += Seq[Index % SeqLen + 1];
			GlobalMax = SuffixMax;
		}
		else if( SuffixMax + Seq[Index % SeqLen + 1] > SuffixMax )
		{
			SuffixMax += Seq[Index % SeqLen + 1];
		}
		else
		{
			SuffixMax = SuffixMax > 0 ? SuffixMax+Seq[Index % SeqLen + 1] : 0;
		}
	}
	return GlobalMax;
}

