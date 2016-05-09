from node import Node
from ID3 import *
from operator import xor
import copy
from modules.parse import *

# Note, these functions are provided for your reference.  You will not be graded
# on their behavior,
# so you can implement them as you choose or not implement them at all if you 
# want to use a different
# architecture for pruning.

def reduced_error_pruning(temp_root, temp_originroot, root, originroot, 
    training_set, validation_set, attribute_metadata):
    if temp_root.is_nominal == True:
        subset = split_on_nominal(training_set, temp_root.decision_attribute)

        for div in temp_root.children.keys():
            if temp_root.children[div].label == None:
                new_Node = Node()
                new_Node.label = mode(subset[div])
                new_Node.children = {}
                temp = copy.deepcopy(temp_root.children[div])
                temp_root.children[div] = new_Node
                prune_acc = validation_accuracy(temp_originroot, validation_set,
                 attribute_metadata)
                acc = validation_accuracy(originroot, validation_set,
                 attribute_metadata)
                if prune_acc >= acc:
                    print prune_acc
                    root.children[div] = new_Node
                else:
                    temp_root.children[div] = temp
                    reduced_error_pruning(temp_root.children[div],
                     temp_originroot, root.children[div], originroot,
                     subset[div], validation_set, attribute_metadata)
    if temp_root.is_nominal == False:
        subset = split_on_numerical(training_set, root.decision_attribute,
         root.splitting_value)
        for i in xrange(0, 2):
            if temp_root.children[i].label == None:
                new_Node = Node()
                new_Node.label = mode(subset[i])
                new_Node.children = {}
                temp = copy.deepcopy(temp_root.children[i])
                temp_root.children[i] = new_Node
                prune_acc = validation_accuracy(temp_originroot, validation_set,
                 attribute_metadata)
                acc = validation_accuracy(originroot, validation_set,
                 attribute_metadata)
                if prune_acc >= acc:
                    print prune_acc
                    root.children[i] = new_Node
                else:
                    temp_root.children[i] = temp
                    reduced_error_pruning(temp_root.children[i], temp_originroot,
                     root.children[i], originroot, subset[i], validation_set, 
                     attribute_metadata) 
       

def validation_accuracy(tree, validate_set, attribute_metadata):
    '''
    takes a tree and a validation set and returns the accuracy of the set on 
    the given tree
    '''
    accuracy = 0
    i = 0
    j = 0
    preprocessing_for_testdata(validate_set, attribute_metadata)
    for entry in validate_set:
        if entry[0] != None:
            if entry[0] == tree.classify(entry):
                accuracy += 1.0
            i += 1
    return accuracy / i * 100
