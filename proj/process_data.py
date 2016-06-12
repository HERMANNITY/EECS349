import csv
import operator
from scipy import stats
import numpy as np
import math
from sklearn import svm

def mode(lst):
	memeda = {}
	for x in lst:
		if x != '?':
			if x in memeda:
				memeda[x] += 1
			else:
				memeda[x] = 1
	return max(memeda.iteritems(), key=operator.itemgetter(1))[0]

def mean(lst):
	memeda = {}
	sumOfLst = 0.0
	lenOfLst = len(lst)
	for x in lst:
		if x != '?':
			sumOfLst += float(x)
	return sumOfLst / lenOfLst
def getCol(matrix, column):
	result = []
	for rowI, row in enumerate(matrix):
		temoRow = []
		result.append(row[column])
	return result
def replaceMat(matrix, toBeZN, toBeRepN):
	for colNum in toBeRepN:
		tempCol1 = replaceMiss(getCol(matrix, colNum))
		for rowNum, row in enumerate(matrix):
			matrix[rowNum][colNum] = tempCol1[rowNum]
	for colNum in toBeZN:
		tempCol2 = zScore(getCol(matrix, colNum))
		for rowNum, row in enumerate(matrix):
			matrix[rowNum][colNum] = tempCol2[rowNum]
	return matrix
def replaceMiss(lst):
	m = str(int(mean(lst)))
	for i, x in enumerate(lst):
		if x == '?':
			lst[i] = m
	return lst
def zScore(lst):
	newLst = replaceMiss(lst)
	for idx, x in enumerate(newLst):
		newLst[idx] = float(x)
	numArray = np.array(newLst)
	numArray = stats.zscore(numArray)
	result = list(numArray)
	minimum = min(result) - 1
	for idx, num in enumerate(result):
		result[idx] = math.log(num - minimum)	
	return result

def replaceNominal(matrix, toBeNu):
	
	for col in toBeNu:
		temp = getCol(matrix, col)
		memeda = {}
		for row in temp:
			if row not in memeda:
				memeda[row] = len(memeda)
		for idx, row in enumerate(matrix):
			matrix[idx][col] = memeda[row[col]]
	return matrix

if __name__ == '__main__':
	allfeature = ["year", "runtimemins", "numlang", "maingenre", "numgenre", "director_award_index", "actors_award_index", "box", "budget"]
	toBeZ = ["year", "runtimemins", "numlang", "numgenre", "director_award_index", "actors_award_index", "box", "budget"]
	toBeRep = ["director_award_index", "actors_award_index", "box", "budget"]
	toBeNu = ["maingenre"]
	movy = open('train_test_data.csv', 'rb')
	movies = csv.reader(movy, delimiter=',',quotechar=' ')
	output_writer = csv.writer(file('zscored_filtered.csv', 'wb'))
	first = movies.next()
	toBeZN = []
	toBeRepN = []
	toBeNuN = []
	featureIdx = []
	for x in toBeZ:
		toBeZN.append(first.index(x))
	for x in toBeRep:
		toBeRepN.append(first.index(x))
	for x in toBeNu:
		toBeNuN.append(first.index(x))
	for x in allfeature:
		featureIdx.append(first.index(x))
	output_writer.writerow(first)
	matrix = []
	for rowI, row in enumerate(movies):
		tempRow = []
		for colI, col in enumerate(row):
			tempRow.append(col)
		matrix.append(tempRow)
	matrix = replaceMat(matrix, toBeZN, toBeRepN)
	matrix = replaceNominal(matrix, toBeNuN)
	X0 = []
	X = []
	XX = []
	y0 = getCol(matrix, first.index("four_class"))
	y = []
	yy = []
	for row in matrix:
		temp = []
		for col in featureIdx:
			temp.append(row[col])
		X0.append(temp)
	for idx, row in enumerate(X0):
		if idx % 10 == 0:
			XX.append(row)
			yy.append(y0[idx])
		else:
			X.append(row)
			y.append(y0[idx])	
	clf = svm.SVC(decision_function_shape='ovo')
	# clf = svm.SVC()
	clf.fit(X, y)
	output = list(clf.predict(XX))
	right = 0
	for idx, x in enumerate(output):
		right += (output[idx] == yy[idx])
	print float(right) / float(len(yy))
	for row in matrix:
		output_writer.writerow(row)



