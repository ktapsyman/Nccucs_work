import pyspark as ps
conf = ps.SparkConf().setAppName("Test").setMaster("local[4]")
sc = ps.SparkContext(conf=conf)
lines = sc.textFile("file:/Users/psyman/Documents/HW/Nccucs_work/DS/20171023121500.export.CSV").filter(lambda str:str is not None and len(str) > 0)
words = lines.flatMap(lambda str:str.split())
wordsCount = words.map(lambda word:(word, 1)).reduceByKey(lambda x,y:x+y).map(lambda x:(x[1], x[0])).sortByKey(False)
print(wordsCount.take(10))
