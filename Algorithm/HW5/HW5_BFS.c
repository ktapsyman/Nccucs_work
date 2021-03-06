#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <limits.h>

#ifndef SAFE_FREE  
#define SAFE_FREE(Ptr) if(Ptr){\
                                  free(Ptr);\
								  Ptr = NULL;\
							  }
#endif  
/*
(1) 由捷運轉乘公車的時間是5分鐘

(2) 由公車轉乘公車的時間是5分鐘

(3) 由捷運轉乘捷運的時間是10分鐘

(4) 由公車轉乘捷運的時間是10分鐘

(5) 兩車站之間只會有一線公車或一線捷運

(6) 捷運與公車都是單向
*/

enum
{
	BUS = 1,
	MRT = 2
};

typedef struct Stop
{
	int StopId;
	bool Visited;
	struct Route *RouteList;
	struct Stop *Next;
} Stop;

typedef struct Route
{
	int RouteId;
	Stop *Dest;
	int LastTransportType;
	int TravelTime;
	struct Route *Next;
} Route;

typedef struct Query
{
	int FromId;
	int DestId;
	struct Query *Next;
} Query;

typedef struct RouteStackElement
{
	Route *RouteElement;
	struct RouteStackElement *Prev;
} RouteStackElement;

Stop *GetTransportInfo();
Stop *CreateStop(int StopId);
Stop *AppendStop(Stop *Head, Stop *NewStop);
Stop *SearchStopById(Stop *Head, int StopId);
void CleanStops(Stop *Head);
void ResetStopState(Stop *Head);

Route *CreateRoute(int RouteId, Stop *Dest, int LastTransportType, int TravelTime);
Route *AppendRoute(Route *Head, Route *NewRoute);
Route *SearchRouteByDestId(Route *Head, int DestId);
void CleanRoutes(Route *Head);
void DumpRoutes(int StopId, Route *Head);

Query *AppendQuery(Query *Head, Query *NewQuery);
Query *CreateQuery(int FromId, int DestId);
void CleanQueries(Query *Head);

RouteStackElement *CreateStackElement(Route *RouteElement);
RouteStackElement *Push(RouteStackElement *Head, RouteStackElement *NewElement);
RouteStackElement *Pop(RouteStackElement **Head);

void DFS(Stop *From, int DestId, RouteStackElement *RouteStack, int *MinTravelTime);
bool ContainsCycle(Stop *Stops);


int main(int argc, char **argv)
{
	Query *Queries = NULL;
	Stop *Stops = GetTransportInfo(&Queries);
	if(!Stops)
	{
		printf("-1\n");
		return 0;
	}
	
	Query *Current = Queries;
	while(Current)
	{
		RouteStackElement *Stack = NULL;
		int MinTravelTime = INT_MAX;
		if(Current->FromId == Current->DestId)
		{
			printf("0\n");
			Current = Current->Next;
			continue;
		}
		
		Stop *From = SearchStopById(Stops, Current->FromId);
		if(!From)
		{
			printf("-1\n");
			Current = Current->Next;
			continue;
		}
		
		DFS(From, Current->DestId, Stack, &MinTravelTime);
		
		if(MinTravelTime == INT_MAX)
			printf("-1\n");
		else
			printf("%d\n", MinTravelTime);
		
		ResetStopState(Stops);
		
		Current = Current->Next;
	}

	CleanStops(Stops);
	CleanQueries(Queries);
	return 0;
}

Stop *GetTransportInfo(Query **Queries)
{
	char Code = '\0';
	Stop *Stops = NULL;
	int RouteId = 0;
	while(1 == scanf("%c", &Code) && Code != 'E')
	{
		if(Code == '\n')
			continue;
		else if(Code == 'Q')
		{
			int FromId = -1;
			int DestId = -1;
			if( 2 != scanf("%d %d", &FromId, &DestId) )
			{
				printf("Query error\n");
				CleanQueries(*Queries);
				CleanStops(Stops);
			}
			*Queries = AppendQuery(*Queries, CreateQuery(FromId, DestId));
			continue;
		}
		char MRTId = '\0';
		int BusId = -1;
		int NumStops = 0;
		int Type = -1;
		if(1 == scanf("%d", &BusId))
		{
			//printf("BusId = %d\n", BusId);
			Type = BUS;
		}
		else if(1 == scanf("%c", &MRTId))
		{
			//printf("MRTId = %c\n", MRTId);
			Type = MRT;
		}
		else
		{
			printf("Code error\n");
			CleanStops(Stops);
			return NULL;
		}
		if( 1 == scanf("%d", &NumStops) )
		{
			int StopIndex = 0;
			for(; StopIndex < NumStops; ++StopIndex)
			{
				int FromId = -1;
				int DestId = -1;
				int TravelTime = -1;
				if( 3 != scanf("%d %d %d", &FromId, &DestId, &TravelTime) )
				{	
					printf("Stop error\n");
					CleanStops(Stops);
					return NULL;
				}

				Stop *From = SearchStopById(Stops, FromId);
				if(!From)
				{
					Stop *NewStop = CreateStop(FromId);
					Stops = AppendStop(Stops, NewStop);
					From = NewStop;
				}

				Stop *Dest = SearchStopById(Stops, DestId);
				if(!Dest)
				{
					Stop *NewStop = CreateStop(DestId);
					Stops = AppendStop(Stops, NewStop);
					Dest = NewStop;
				}
				Route *NewRoute = CreateRoute(RouteId, Dest, Type, TravelTime);
				From->RouteList = AppendRoute(From->RouteList, NewRoute);
			}
			RouteId++;
			
		}
		else
		{
			printf("2Stop error\n");
		}
	}
	return Stops;
}

Stop *CreateStop(int StopId)
{
	Stop *NewStop = (Stop *)malloc(sizeof(Stop));
	if(!NewStop)
	{
		printf("Failed to malloc\n");
		return NULL;
	}

	NewStop->Next = NULL;
	NewStop->StopId = StopId;
	NewStop->Visited = false;
	NewStop->RouteList = NULL;

	return NewStop;
}

Stop *AppendStop(Stop *Head, Stop *NewStop)
{
	if(!NewStop)
	{
		printf("Warning : append NULL stop\n");
		return Head;
	}
	if(!Head)
		return NewStop;
	
	Stop *Current = Head;
	while(Current)
	{
		if(!Current->Next)
		{
			Current->Next = NewStop;
			break;
		}
		Current = Current->Next;
	}

	return Head;
}

Stop *SearchStopById(Stop *Head, int StopId)
{
	if(!Head)
		return NULL;
	Stop *Current = Head;
	while(Current)
	{
		if(Current->StopId == StopId)
			return Current;
		Current = Current->Next;
	}
	return NULL;
}

void ResetStopState(Stop *Head)
{
	if(!Head)
		return;
	Stop *Current = Head;
	while(Current)
	{
		Current->Visited = false;
		Current = Current->Next;
	}
}

void CleanStops(Stop *Head)
{
	if(!Head)
		return;
	CleanStops(Head->Next);
	CleanRoutes(Head->RouteList);
	SAFE_FREE(Head);
}

Route *CreateRoute(int RouteId, Stop *Dest, int LastTransportType, int TravelTime)
{
	Route *NewRoute = (Route *)malloc(sizeof(Route));
	if(!NewRoute)
	{
		printf("Failed to malloc new route\n");
		return NULL;
	}

	NewRoute->RouteId = RouteId;
	NewRoute->Dest = Dest;
	NewRoute->LastTransportType = LastTransportType;
	NewRoute->TravelTime = TravelTime;
	NewRoute->Next = NULL;

	return NewRoute;
}

Route *AppendRoute(Route *Head, Route *NewRoute)
{
	if(!NewRoute)
	{
		printf("Warning : appending NULL Route\n");
		return Head;
	}
	if(!Head)
		return NewRoute;

	Route *Current = Head;
	while(Current->Next)
	{
		Current = Current->Next;
	}
	Current->Next = NewRoute;

	return Head;
}

Route *SearchRouteByDestId(Route *Head, int DestId)
{
	if(!Head)
		return NULL;
	Route *Current = Head;
	while(Current)
	{
		if(Current->Dest->StopId == DestId)
			return Current;
		Current = Current->Next;
	}
	return NULL;
}

void CleanRoutes(Route *Head)
{
	if(!Head)
		return;
	CleanRoutes(Head->Next);
	SAFE_FREE(Head);
}

void DumpRoutes(int StopId, Route *Head)
{
	Route *Current = Head;
	while(Current)
	{
		printf("From : %d to %d will cost %d on %s and RouteId is %d\n", StopId, Current->Dest->StopId, Current->TravelTime, Current->LastTransportType == BUS? "BUS":"MRT", Current->RouteId);
		Current = Current->Next;
	}
}

Query *CreateQuery(int FromId, int DestId)
{
	Query *NewQuery = (Query *)malloc(sizeof(Query));
	if(!NewQuery)
	{
		printf("Failed to malloc new Query\n");
		return NULL;
	}
	
	NewQuery->FromId = FromId;
	NewQuery->DestId = DestId;

	return NewQuery;
}

Query *AppendQuery(Query *Head, Query *NewQuery)
{
	if(!NewQuery)
	{
		printf("Warning : appending NULL Query\n");
		return Head;
	}
	if(!Head)
		return NewQuery;

	Query *Current = Head;
	while(Current->Next)
	{
		Current = Current->Next;
	}
	Current->Next = NewQuery;

	return Head;
}

void CleanQueries(Query *Head)
{
	if(!Head)
		return;
	CleanQueries(Head->Next);
	SAFE_FREE(Head);
}

void DFS(Stop *From, int DestId, RouteStackElement *RouteStack, int *MinTravelTime)
{
	if(!From || From->Visited)
	{
		return;
	}
	From->Visited = true;
	Route *CurrentRoute = From->RouteList;
	while(CurrentRoute && !CurrentRoute->Dest->Visited)
	{
		RouteStack = Push(RouteStack, CreateStackElement(CurrentRoute));
		if( CurrentRoute->Dest->StopId == DestId )
		{
			RouteStackElement *CurrentStackElement = RouteStack;
			int CurrentTransportType = CurrentStackElement->RouteElement->LastTransportType;
			int CurrentRouteId = CurrentStackElement->RouteElement->RouteId;
			int TotalTravelTime = 0;//CurrentStackElement->RouteElement->TravelTime;
			while(CurrentStackElement)
			{
				TotalTravelTime += CurrentStackElement->RouteElement->TravelTime;

				if(CurrentStackElement->RouteElement->RouteId != CurrentRouteId)
				{
					if(CurrentTransportType == BUS)
					{
						TotalTravelTime += 5;
					}
					else
					{
						TotalTravelTime += 10;
					}
					
					CurrentTransportType = CurrentStackElement->RouteElement->LastTransportType;
					CurrentRouteId = CurrentStackElement->RouteElement->RouteId;
				}
				CurrentStackElement = CurrentStackElement->Prev;
			}
			if(TotalTravelTime < *MinTravelTime)
			{
				*MinTravelTime = TotalTravelTime;
			}
		}
		else
		{
			DFS(CurrentRoute->Dest, DestId, RouteStack, MinTravelTime);
		}
		
		CurrentRoute = CurrentRoute->Next;
		RouteStackElement *Top = Pop(&RouteStack);
		SAFE_FREE(Top);
	}
	From->Visited = false;
	return;
}

RouteStackElement *CreateStackElement(Route *RouteElement)
{
	RouteStackElement *NewElement = (RouteStackElement *)malloc(sizeof(RouteStackElement));
	if(!NewElement)
	{
		printf("Failed to malloc new stack element\n");
		return NULL;
	}
	NewElement->RouteElement = RouteElement;
	NewElement->Prev = NULL;

	return NewElement;
}

RouteStackElement *Push(RouteStackElement *Head, RouteStackElement *NewElement)
{
	if(!NewElement)
		return Head;
	if(!Head)
		return NewElement;

	NewElement->Prev = Head;

	return NewElement;
}

RouteStackElement *Pop(RouteStackElement **Head)
{
	if(!Head || !*Head)
		return NULL;

	RouteStackElement *Top = *Head;
	*Head = (*Head)->Prev;

	return Top;
}

