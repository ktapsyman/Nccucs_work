#!/bin/bash
#for SrcImg in ../../../Dataset/Img/*/143636.gif
for Text in ../../../Dataset/Img/*
do
	DirName=./Dataset/$(basename $Text)
	echo $DirName
	if [ ! -d $DirName ]; then
		mkdir $DirName
	fi

	for SrcImg in $Text/*
	do
		SrcFileName=${SrcImg##*/}
		IntermediateFile=${SrcFileName%.*}.png
		TargetFile=$DirName/${SrcFileName%.*}.jpg
		#echo $SrcImg
		#echo $SrcFileName
		#echo $IntermediateFile
		#echo $TargetFile
		convert -negate $SrcImg $IntermediateFile
		convert -alpha remove $IntermediateFile $TargetFile
		rm $IntermediateFile
	done
done
