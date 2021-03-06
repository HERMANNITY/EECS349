import math
from node import Node
import sys
import copy
from data_preprocessing import *

def ID3(data_set, attribute_metadata, numerical_splits_count, depth):
    '''
    See Textbook for algorithm.
    Make sure to handle unknown values, some suggested approaches were
    given in lecture.
    ========================================================================================================
    Input:  A data_set, attribute_metadata, maximum number of splits to consider for numerical attributes,
	maximum depth to search to (depth = 0 indicates that this node should output a label)
    ========================================================================================================
    Output: The node representing the decision tree learned over the given data set
    ========================================================================================================

    '''
    preprocessing(data_set, attribute_metadata)
    if check_homogenous(data_set) != None:
        ans = Node()
        ans.label = check_homogenous(data_set)
    elif depth == 0:
            ans = Node()
            ans.label = mode(data_set)
    else:
        best = pick_best_attribute(data_set, attribute_metadata, 
            numerical_splits_count)
        if best[0] == False:
            ans = Node()
            ans.label = mode(data_set)
        else:
            ans = Node()
            ans.decision_attribute = best[0]
            ans.name = attribute_metadata[best[0]]['name']
            depth -= 1
            if str(best[1]) == 'False':
                ans.is_nominal = True
                ans.children = {}
                divide = split_on_nominal(data_set, best[0])
                for x in divide.keys():
                    ans.children[x] = ID3(divide[x], attribute_metadata, 
                        numerical_splits_count, depth)
            else:
                ans.is_nominal = False
                ans.children = []
                ans.splitting_value = best[1]
                divide = split_on_numerical(data_set, best[0], best[1])
                ans.children.append(ID3(divide[0], attribute_metadata, 
                    numerical_splits_count, depth))
                ans.children.append(ID3(divide[1], attribute_metadata, 
                    numerical_splits_count, depth)) 
    return ans

def check_homogenous(data_set):
    '''
    ========================================================================================================
    Input:  A data_set
    ========================================================================================================
    Job:    Checks if the attribute at index 0 is the same for the data_set, if so return output otherwise None.
    ========================================================================================================
    Output: Return either the homogenous attribute or None
    ========================================================================================================
    '''
    for i in xrange(0, len(data_set) - 1):
        if data_set[i][0] != data_set[i + 1][0]:
            return None
    return data_set[0][0]
# ======== Test Cases =============================
# data_set = [[0],[1],[1],[1],[1],[1]]
# check_homogenous(data_set) ==  None
# data_set = [[0],[1],[None],[0]]
# check_homogenous(data_set) ==  None
# data_set = [[1],[1],[1],[1],[1],[1]]
# check_homogenous(data_set) ==  1

def pick_best_attribute(data_set, attribute_metadata, numerical_splits_count):
    '''
    ========================================================================================================
    Input:  A data_set, attribute_metadata, splits counts for numeric
    ========================================================================================================
    Job:    Find the attribute that maximizes the gain ratio. If attribute is numeric return best split value.
            If nominal, then split value is False.
            If gain ratio of all the attributes is 0, then return False, False
            Only consider numeric splits for which numerical_splits_count is greater than zero
    ========================================================================================================
    Output: best attribute, split value if numeric
    ========================================================================================================
    '''
    i = 0
    max_num = 0
    memeda = {}
    for x in attribute_metadata:
        if x['name'] == "winner":
            i += 1
            continue
        if x['is_nominal'] == True:
            gratio = gain_ratio_nominal(data_set, i)
            memeda[gratio] = i
            i += 1
        if x['is_nominal'] == False:
            if numerical_splits_count[i] != 0:
                gratio = gain_ratio_numeric(data_set, i)
                if gratio[0] >= max_num:
                    max_num = gratio[0]
                    splival_atmax = gratio[1]
                memeda[gratio[0]] = i
                i += 1
            else:
                memeda[0] = i
                i += 1
    if memeda == {} or max(memeda.keys()) == 0:
        return (False, False)
    else: 
        ans = memeda[max(memeda.keys())]
        if attribute_metadata[ans]['is_nominal'] == True:
            return (ans, False)
        else:
            numerical_splits_count[ans] -= 1
            return (ans, splival_atmax)

# # ======== Test Cases =============================
# numerical_splits_count = [20,20]
# attribute_metadata = [{'name': "winner",'is_nominal': True},{'name': "opprundifferential",'is_nominal': False}]
# data_set = [[1, 0.27], [0, 0.42], [0, 0.86], [0, 0.68], [0, 0.04], [1, 0.01], [1, 0.33], [1, 0.42], [0, 0.51], [1, 0.4]]
# pick_best_attribute(data_set, attribute_metadata, numerical_splits_count) == (1, 0.51)
# attribute_metadata = [{'name': "winner",'is_nominal': True},{'name': "weather",'is_nominal': True}]
# data_set = [[0, 0], [1, 0], [0, 2], [0, 2], [0, 3], [1, 1], [0, 4], [0, 2], [1, 2], [1, 5]]
# pick_best_attribute(data_set, attribute_metadata, numerical_splits_count) == (1, False)

# Uses gain_ratio_nominal or gain_ratio_numeric to calculate gain ratio.

def mode(data_set):
    '''
    ========================================================================================================
    Input:  A data_set
    ========================================================================================================
    Job:    Takes a data_set and finds mode of index 0.
    ========================================================================================================
    Output: mode of index 0.
    ========================================================================================================
    '''
    count0 = 0
    count1 = 0
    for x in data_set:
        if x[0] == 0:
            count0 += 1
        else:
            count1 += 1
    if count0 > count1:
        return 0
    else:
        return 1
# ======== Test case =============================
# data_set = [[0],[1],[1],[1],[1],[1]]
# mode(data_set) == 1
# data_set = [[0],[1],[0],[0]]
# mode(data_set) == 0

def entropy(data_set):
    '''
    ========================================================================================================
    Input:  A data_set
    ========================================================================================================
    Job:    Calculates the entropy of the attribute at the 0th index, the value we want to predict.
    ========================================================================================================
    Output: Returns entropy. See Textbook for formula
    ========================================================================================================
    '''
    numEntries = len(data_set)
    count0 = 0
    count1 = 0
    for x in data_set:
        if x[0] == 0:
            count0 += 1
        else:
            count1 += 1
    p0 = float(count0)/numEntries
    p1 = float(count1)/numEntries
    if p0 == 0 or p1 == 0:
        ans = 0
    else:
        ans = -p0 * math.log(p0, 2) - p1 * math.log(p1, 2)
    return ans

# ======== Test case =============================
# data_set = [[0],[1],[1],[1],[0],[1],[1],[1]]
# entropy(data_set) == 0.811
# data_set = [[0],[0],[1],[1],[0],[1],[1],[0]]
# entropy(data_set) == 1.0
# data_set = [[0],[0],[0],[0],[0],[0],[0],[0]]
# entropy(data_set) == 0


def gain_ratio_nominal(data_set, attribute):
    '''
    ========================================================================================================
    Input:  Subset of data_set, index for a nominal attribute
    ========================================================================================================
    Job:    Finds the gain ratio of a nominal attribute in relation to the variable we are training on.
    ========================================================================================================
    Output: Returns gain_ratio. See https://en.wikipedia.org/wiki/Information_gain_ratio
    ========================================================================================================
    '''
    split = split_on_nominal(data_set, attribute)
    Ex = len(data_set)
    ent = entropy(data_set)
    IV = 0
    subEnt = 0
    for splitval in split.keys():
        p = float(len(split[splitval])) / Ex
        IV += -p * math.log(p, 2)
        subEnt += entropy(split[splitval]) * p
    InfoGain = ent - subEnt
    if InfoGain == 0:
        return 0
    else:
        return InfoGain / IV
# ======== Test case =============================
# data_set, attr = [[1, 2], [1, 0], [1, 0], [0, 2], [0, 2], [0, 0], [1, 3], [0, 4], [0, 3], [1, 1]], 1
# gain_ratio_nominal(data_set,attr) == 0.11470666361703151
# data_set, attr = [[1, 2], [1, 2], [0, 4], [0, 0], [0, 1], [0, 3], [0, 0], [0, 0], [0, 4], [0, 2]], 1
# gain_ratio_nominal(data_set,attr) == 0.2056423328155741
# data_set, attr = [[0, 3], [0, 3], [0, 3 ], [0, 4], [0, 4], [0, 4], [0, 0], [0, 2], [1, 4], [0, 4]], 1
# gain_ratio_nominal(data_set,attr) == 0.06409559743967516

def gain_ratio_numeric(data_set, attribute, steps = 1):
    '''
    ========================================================================================================
    Input:  Subset of data set, the index for a numeric attribute, and a step size for normalizing the data.
    ========================================================================================================
    Job:    Calculate the gain_ratio_numeric and find the best single threshold value
            The threshold will be used to split examples into two sets
                 those with attribute value GREATER THAN OR EQUAL TO threshold
                 those with attribute value LESS THAN threshold
            Use the equation here: https://en.wikipedia.org/wiki/Information_gain_ratio
            And restrict your search for possible thresholds to examples with array index mod(step) == 0
    ========================================================================================================
    Output: This function returns the gain ratio and threshold value
    ========================================================================================================
    '''
    result = {}
    for index in xrange(0, len(data_set)):
        if index % steps == 0:
            splitnum = split_on_numerical(data_set, attribute, 
                data_set[index][attribute])
            if splitnum[0] == [] or splitnum[1] == []:
                infoRatio = 0
            else:
                templeft = copy.deepcopy(splitnum[0])
                tempright = copy.deepcopy(splitnum[1])
                for x in templeft:
                    x[attribute] = 0
                for x in tempright:
                    x[attribute] = 1
                new_data_set = templeft + tempright
                infoRatio = gain_ratio_nominal(new_data_set, attribute)
            result[infoRatio] = data_set[index][attribute]         #may have bug
    return (max(result.keys()), result[max(result.keys())])
# ======== Test case =============================
# data_set,attr,step = [[0,0.05], [1,0.17], [1,0.64], [0,0.38], [0,0.19], [1,0.68], [1,0.69], [1,0.17], [1,0.4], [0,0.53]], 1, 2
# gain_ratio_numeric(data_set,attr,step) == (0.31918053332474033, 0.64)
# data_set,attr,step = [[1, 0.35], [1, 0.24], [0, 0.67], [0, 0.36], [1, 0.94], [1, 0.4], [1, 0.15], [0, 0.1], [1, 0.61], [1, 0.17]], 1, 4
# gain_ratio_numeric(data_set,attr,step) == (0.11689800358692547, 0.94)
# data_set,attr,step = [[1, 0.1], [0, 0.29], [1, 0.03], [0, 0.47], [1, 0.25], [1, 0.12], [1, 0.67], [1, 0.73], [1, 0.85], [1, 0.25]], 1, 1
# gain_ratio_numeric(data_set,attr,step) == (0.23645279766002802, 0.29)

def split_on_nominal(data_set, attribute):
    '''
    ========================================================================================================
    Input:  subset of data set, the index for a nominal attribute.
    ========================================================================================================
    Job:    Creates a dictionary of all values of the attribute.
    ========================================================================================================
    Output: Dictionary of all values pointing to a list of all the data with that attribute
    ========================================================================================================
    '''
    ans = {}
    for x in data_set:
        if ans.has_key(x[attribute]):
            ans[x[attribute]].append(x)
        else:
            ans[x[attribute]] = [x]
    return ans
# ======== Test case =============================
# data_set, attr = [[0, 4], [1, 3], [1, 2], [0, 0], [0, 0], [0, 4], [1, 4], [0, 2], [1, 2], [0, 1]], 1
# split_on_nominal(data_set, attr) == {0: [[0, 0], [0, 0]], 1: [[0, 1]], 2: [[1, 2], [0, 2], [1, 2]], 3: [[1, 3]], 4: [[0, 4], [0, 4], [1, 4]]}
# data_set, attr = [[1, 2], [1, 0], [0, 0], [1, 3], [0, 2], [0, 3], [0, 4], [0, 4], [1, 2], [0, 1]], 1
# split on_nominal(data_set, attr) == {0: [[1, 0], [0, 0]], 1: [[0, 1]], 2: [[1, 2], [0, 2], [1, 2]], 3: [[1, 3], [0, 3]], 4: [[0, 4], [0, 4]]}

def split_on_numerical(data_set, attribute, splitting_value):
    '''
    ========================================================================================================
    Input:  Subset of data set, the index for a numeric attribute, threshold (splitting) value
    ========================================================================================================
    Job:    Splits data_set into a tuple of two lists, the first list contains the examples where the given
	attribute has value less than the splitting value, the second list contains the other examples
    ========================================================================================================
    Output: Tuple of two lists as described above
    ========================================================================================================
    '''
    less = []
    greater = []
    for x in data_set:
        if x[attribute] < splitting_value:
            less.append(x)
        else:
            greater.append(x)
    return (less, greater)
# ======== Test case =============================
# d_set,a,sval = [[1, 0.25], [1, 0.89], [0, 0.93], [0, 0.48], [1, 0.19], [1, 0.49], [0, 0.6], [0, 0.6], [1, 0.34], [1, 0.19]],1,0.48
# split_on_numerical(d_set,a,sval) == ([[1, 0.25], [1, 0.19], [1, 0.34], [1, 0.19]],[[1, 0.89], [0, 0.93], [0, 0.48], [1, 0.49], [0, 0.6], [0, 0.6]])
# d_set,a,sval = [[0, 0.91], [0, 0.84], [1, 0.82], [1, 0.07], [0, 0.82],[0, 0.59], [0, 0.87], [0, 0.17], [1, 0.05], [1, 0.76]],1,0.17
# split_on_numerical(d_set,a,sval) == ([[1, 0.07], [1, 0.05]],[[0, 0.91],[0, 0.84], [1, 0.82], [0, 0.82], [0, 0.59], [0, 0.87], [0, 0.17], [1, 0.76]])
