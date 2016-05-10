import os.path
from operator import xor
from parse import *
import csv, collections
import random
from ID3 import *
from node import *
from data_preprocessing import *
# DOCUMENTATION
# ========================================
# this function outputs predictions for a given data set.
# NOTE this function is provided only for reference.
# You will not be graded on the details of this function, so you can change the interface if 
# you choose, or not complete this function at all if you want to use a different method for
# generating predictions.

def create_predictions(tree, testfile_name, newfile_name):
    '''
    Given a tree and a url to a data_set. Create a csv with a prediction for
    each result
    using the classify method in node class.
    '''
    testdata = parse(testfile_name, 'winner')
    test_data_set = testdata[0]
    preprocessing_for_testdata(test_data_set, testdata[1])
    testfile = csv.reader(open(testfile_name, 'rb'))
    newfile = csv.writer(file(newfile_name, 'wb'))
    i = 0
    error = 0
    for row in testfile:
        if row[len(row) - 1] == ' winner':
            newfile.writerow(row)
        else:
            if tree.classify(test_data_set[i]) != None:
                row[len(row) - 1] = tree.classify(test_data_set[i])
                newfile.writerow(row)
            else:
                print test_data_set[i]
                newfile.writerow(['t', 't', 't', 't'])
                error += 1    
            i += 1