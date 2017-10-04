import numpy as np
import csv

ScoreKeys = ["0~9", "10~19", "20~29", "30~39", "40~49", "50~59", "60~69", "70~79", "80~89", "90~99", "100"]

#Problem 1 ( Cosine Similarity )
def cosine_similarity(A,B):
    ### write your code here ###
	result_value = float()
	VectorA = np.array(A)
	VectorB = np.array(B)
	

	return np.dot(VectorA, VectorB)/(np.linalg.norm(VectorA)*np.linalg.norm(VectorB))

#Problem 2 ( Grades )
def grades(FilePath):
	DictGrades = dict()
	TupleGradeList = []
	
	with open(FilePath) as ScoreFile:
		CsvReader = csv.DictReader(ScoreFile, skipinitialspace=True)
		for Row in CsvReader:
			print(Row)
			TupleGradeList.append((Row["Name"], Row["Age"], Row["Score"]))
			Score = int(Row["Score"])
			if 0 <= Score and Score < 10:
				if ScoreKeys[0] not in DictGrades:
					DictGrades[ScoreKeys[0]] = 1
				else:
					DictGrades[ScoreKeys[0]] += 1
					
			elif 10 <= Score and Score < 20:
				if ScoreKeys[1] not in DictGrades:
					DictGrades[ScoreKeys[1]] = 1
				else:
					DictGrades[ScoreKeys[1]] += 1
					
			elif 20 <= Score and Score < 30:
				if ScoreKeys[2] not in DictGrades:
					DictGrades[ScoreKeys[2]] = 1
				else:
					DictGrades[ScoreKeys[2]] += 1
					
			elif 30 <= Score and Score < 40:
				if ScoreKeys[3] not in DictGrades:
					DictGrades[ScoreKeys[3]] = 1
				else:
					DictGrades[ScoreKeys[3]] += 1
					
			elif 40 <= Score and Score < 50:
				if ScoreKeys[4] not in DictGrades:
					DictGrades[ScoreKeys[4]] = 1
				else:
					DictGrades[ScoreKeys[4]] += 1
					
			elif 50 <= Score and Score < 60:
				if ScoreKeys[5] not in DictGrades:
					DictGrades[ScoreKeys[5]] = 1
				else:
					DictGrades[ScoreKeys[5]] += 1
					
			elif 60 <= Score and Score < 70:
				if ScoreKeys[6] not in DictGrades:
					DictGrades[ScoreKeys[6]] = 1
				else:
					DictGrades[ScoreKeys[6]] += 1
					
			elif 70 <= Score and Score < 80:
				if ScoreKeys[7] not in DictGrades:
					DictGrades[ScoreKeys[7]] = 1
				else:
					DictGrades[ScoreKeys[7]] += 1
					
			elif 80 <= Score and Score < 90:
				if ScoreKeys[8] not in DictGrades:
					DictGrades[ScoreKeys[8]] = 1
				else:
					DictGrades[ScoreKeys[8]] += 1
					
			elif 90 <= Score and Score < 100:
				if ScoreKeys[9] not in DictGrades:
					DictGrades[ScoreKeys[9]] = 1
				else:
					DictGrades[ScoreKeys[9]] += 1

			elif Score == 100:
				if ScoreKeys[10] not in DictGrades:
					DictGrades[ScoreKeys[10]] = 1
				else:
					DictGrades[ScoreKeys[10]] += 1
					
			else:
				print("Score out of range! Score : "+str(Score))

		TupleGradeList.sort(key=lambda Student:(Student[0], Student[1], Student[2]))
		DictGrades = [(key, DictGrades[key]) for key in sorted(DictGrades.keys)]
		print(TupleGradeList)
		print(DictGrades)

	return DictGrades, TupleGradeList

#Problem 3 ( The valid of password )
def valid_password(passwords):
	result_list = list()    

	return result_list

if __name__ == "__main__":
	pro_1_value = cosine_similarity([1,2,3],[4,5,6])
	pro_2_dict, pro_2_tuple = grades('./example.csv')
	pro_3_list = valid_password(['Ab12!','AA1234!?','AbCdEfGh','12345AaBa!', '12Zz!?98Aa#@'])
	print (pro_1_value)
	print (pro_2_dict)
	print (pro_2_tuple)
	print (pro_3_list)
