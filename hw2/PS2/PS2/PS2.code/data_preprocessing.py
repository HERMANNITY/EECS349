
def preprocessing(data_set, attribute_metadata):
    memeda = []
    j = 0
    for x in xrange(0, len(data_set)):
        if data_set[x][0] == None:
            memeda.append(x)
    for x in memeda:
        del data_set[x - j]
        j += 1
    for x in data_set:
        for attribute in xrange(1, len(x)):
            if x[attribute] == None:
                x[attribute] = helper(data_set, attribute_metadata
                    , attribute, x[0])
                
def preprocessing_for_testdata(data_set, attribute_metadata):
    for x in data_set:
        for attribute in xrange(1, len(x)):
            if x[attribute] == None:
                x[attribute] = helper(data_set, attribute_metadata
                    , attribute, x[0])
                
def helper(data_set, attribute_metadata, attribute, target_value):
    memeda = {}
    sum = 0
    count = 0
    if attribute_metadata[attribute]['is_nominal'] == True:
        for x in data_set:
            if x[attribute] != None and x[0] == target_value:
                if memeda.has_key(x[attribute]):
                    memeda[x[attribute]] += 1
                else:
                    memeda[x[attribute]] = 1
        for key in memeda.keys():
            if memeda[key] == max(memeda.values()):
                return key
    else:
        for x in data_set:
            if x[attribute] != None and x[0] == target_value:
                sum += x[attribute]
                count += 1
        return sum / count