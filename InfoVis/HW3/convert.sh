for file in *.csv
do
	echo $file;
	iconv -f big5 -t unicode $file -o UTF/$file
done
