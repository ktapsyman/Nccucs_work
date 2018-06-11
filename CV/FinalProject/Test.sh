#!/bin/bash
#Usage: ./voronoi <command> <implementation_name> <files>
# * command: [ thin | video | video_bright | video_comparer | benchmark ]
#   If command =  video_comparer or benchmark, no implementation must be specified.
# * implementation_name: [morph, guo_hall, guo_hall_original, guo_hall_fast, zhang_suen, zhang_suen_original, zhang_suen_fast]


#Algos=("morph" "guo_hall" "guo_hall_original" "guo_hall_fast" "zhang_suen" "zhang_suen_original" "zhang_suen_fast")
Algos=("zhang_suen" "zhang_suen_original" "zhang_suen_fast")

for Algo in ${Algos[@]};
do
	./voronoi thin "$Algo" Test.png
done
