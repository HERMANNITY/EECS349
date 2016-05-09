# DOCUMENTATION
# =====================================
# Class node attributes:
# ----------------------------
# children - a list of 2 nodes if numeric, and a dictionary (key=attribute value, value=node) if nominal.  
#            For numeric, the 0 index holds examples < the splitting_value, the 
#            index holds examples >= the splitting value
#
# label - is None if there is a decision attribute, and is the output label (0 or 1 for
#	the homework data set) if there are no other attributes
#       to split on or the data is homogenous
#
# decision_attribute - the index of the decision attribute being split on
#
# is_nominal - is the decision attribute nominal
#
# value - Ignore (not used, output class if any goes in label)
#
# splitting_value - if numeric, where to split
#
# name - name of the attribute being split on

class Node:
    def __init__(self):
        # initialize all attributes
        self.label = None
        self.decision_attribute = None
        self.is_nominal = None
        self.value = None
        self.splitting_value = None
        self.children = {}
        self.name = None

    def classify(self, instance):
        '''
        given a single observation, will return the output of the tree
        '''
        
        if self.label == 1:
            return 1
        if self.label == 0:
            return 0
        if self.label == None:
            if self.is_nominal == True:
                diff = {}
                for div in self.children.keys():
                    if div == instance[self.decision_attribute]:
                        return self.children[div].classify(instance)
                    else:
                        diff[abs(instance[self.decision_attribute] - div)] = div
                return self.children[diff[min(diff.keys())]].classify(instance)
            else:
                if instance[self.decision_attribute] < self.splitting_value:
                    return self.children[0].classify(instance)
                else:
                    return self.children[1].classify(instance)

    def print_tree(self, indent = 0):
        '''
        returns a string of the entire tree in human readable form
        '''
        output = []
        print_text = ''
        self.generateTree(indent, output)
        for entry in output:
            print_text += entry
        return print_text

    def print_dnf_tree(self):
        '''
        returns the disjunct normalized form of the tree.
        '''
        result = ''
        dnf = []
        total_dnf = ''
        self.generateDNF(result, dnf)
        for entry in dnf:
            entry = entry[:-4] + ')'
            total_dnf += entry + ' v '
        print total_dnf[:-3]
        return total_dnf[:-3]

    def generateTree(self, indent, output):
        if self.is_nominal == True:
            for div in self.children.keys():
                if self.children[div].label == None:
                    output.append(' ' * indent * 2 + self.name +\
                     ' = ' + str(div) + '\n')
                    print ' ' * indent * 2 + self.name + ' = ' + str(div)
                    self.children[div].generateTree(indent + 1, output)
                else:
                    output.append(' ' * indent * 2 + self.name +\
                     ' = ' + str(div) + ' : ' + str(self.children[div].label) +\
                      '\n')
                    print ' ' * indent * 2 + self.name + ' = ' + str(div) +\
                     ' : ' + str(self.children[div].label)
        if self.is_nominal == False:
            if self.children[0].label == None:
                output.append(' ' * indent * 2 + self.name + ' < ' +\
                 str(self.splitting_value) + '\n')
                print ' ' * indent * 2 + self.name + ' < ' +\
                 str(self.splitting_value)
                self.children[0].generateTree(indent + 1, output)
            else:
                output.append(' ' * indent * 2 + self.name + ' < ' +\
                 str(self.splitting_value) + ' : ' +\
                  str(self.children[0].label) + '\n')
                print ' ' * indent * 2 + self.name + ' < ' +\
                 str(self.splitting_value) + ' : ' + str(self.children[0].label)
            if self.children[1].label == None:
                output.append(' ' * indent * 2 + self.name + ' >' + '= ' +\
                 str(self.splitting_value) + '\n')
                print ' ' * indent * 2 + self.name + ' >' + '= ' +\
                 str(self.splitting_value)
                self.children[1].generateTree(indent + 1, output)
            else:
                output.append(' ' * indent * 2 + self.name + ' >' + '= ' +\
                 str(self.splitting_value) + ' : ' +\
                  str(self.children[1].label) + '\n')
                print ' ' * indent * 2 + self.name + ' >' + '= ' +\
                 str(self.splitting_value) + ' : ' + str(self.children[1].label)
        
        
    def generateDNF(self, result, dnf):
        if self.label == 1:
            dnf.append('(' + result + ')' )
        if self.is_nominal == True:
            for div in self.children.keys():
                result += self.name + '=' + str(div) + ' ^ '
                self.children[div].generateDNF(result, dnf)
        if self.is_nominal == False:
            temp = result
            result += self.name + '<' + str(self.splitting_value) + ' ^ '
            self.children[0].generateDNF(result, dnf)
            result = temp   
            result += self.name + '>' + '=' + str(self.splitting_value) + ' ^ '
            self.children[1].generateDNF(result, dnf)











