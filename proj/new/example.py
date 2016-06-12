from imdb import IMDb
# from parse import *
import wikipedia
import csv
def toMillion(txt):
    li = txt.split(' ')
    if li[1] == 'million':
        return float(li[0][1:])
    elif li[1] == 'billion':
        return float(li[0][1:])*1000
    else:
        print li[0]
        print ('neither million or billion')
        
def countAwards(nameList):
    if len(nameList) == 0:
        return 0
    if not isinstance(nameList, list):
        nameList = [nameList]
    oscars = 0
    golden_globes = 0
    for name in nameList:
        try:
            text = wikipedia.page(name).html()
        except:
            print name + ' does not have wiki page'
        else:
            oscars += text.count('oscar') + text.count('Oscar')\
            + text.count("prize") + text.count("Prize") + text.count("awards")
            golden_globes += text.count('golden globe')
    return oscars + golden_globes

def genF() :
    filename = "filtered.csv"
    newfile = "data7500-7999.csv"
    testfile = csv.reader(open(filename, 'rb'))
    newfile = csv.writer(file(newfile, 'wb'))
    a = []
    for row in testfile:
        if row[0] == "imdbid":
            newfile.writerow(row)
            continue
        tmp = row[0]
        tmp = tmp[2:]
        
        a.append(tmp)
        
        newrow = []
        newrow.append(tmp)
        newrow += (row[1:])
        newfile.writerow(newrow)

    '''
    #parse (filename)
    a = loadPickle("filteredId")
    a = a[:100]
    d = {}
    cnt = 0
    for i in a:
        ia = IMDb()
        m = ia.get_movie(str(i))
        d[i] = m

    makePickle (d, "lang")
    '''
#genF()

# def genD(left, right) :
#     filename = "filtered.csv"
#     newfile = "data.csv"
#     testfile = csv.reader(open(filename, 'rb'))
#     newfile = csv.writer(file(newfile, 'wb'))
#     #parse (filename)
#     a = loadPickle("filteredId")
#     a = a[left:right]
#     d = {}
#     cnt = 0
#     for i in a:
#         ia = IMDb()
#         m = ia.get_movie(str(i))
#         print cnt
#         cnt += 1
#         d[i] = m

#     makePickle (d, "movies" + str(left) + "to" + str(right))
#genD(0, 10)
'''
def genData(s, l, r):
    filename = "filtered.csv"
    newfile = "data.csv"
    testfile = csv.reader(open(filename, 'rb'))
    newfile = csv.writer(file(newfile, 'wb'))
    #parse (filename)
    a = loadPickle("filteredId")

    #d = loadPickle (s)
    row = ["Id", "casts", "language", "num lang", "director awards", "actor awards"]
    newfile.writerow(row)
    for i in range (l, r):
        print i
        row = []
        mId = a[i]
        row.append(mId)
        ia = IMDb()
        mv = ia.get_movie(str(mId))
        #mv = d[mId]

        s = ""
        try:
            casts = mv['cast']
            if len(casts) >= 3:
                tmp = casts[:3]
                s = tmp[0]['name'] + ',' + tmp[1]['name'] + ',' + tmp[2]['name']
        except:
            print i, " error"
        row.append(s)
        #language
        s = ""
        lang = []
        try:
            lang = mv['lang']
            for j in lang:
                s += str(j) + ','
            s = s[:-1]

        except:
            s = ""
            lang = []
            
        row.append(s)
        row.append(len(lang))
        try:
            newfile.writerow(row)
        except:
            newfile.writerow([])
#genData("", 0, 8943)
'''
            
def genData(l, r):
    filename = "filtered.csv"
    newfile = "data7500-7999.csv"
    testfile = csv.reader(open(filename, 'rb'))
    newfile = csv.writer(file(newfile, 'wb'))

    #d = loadPickle (s)
    cnt = 0
    for row in testfile:
        if row[0] == "imdbid":
 #           row += ["main Genres", "number of genres", "casts", "language", "director awards", "actor awards"]
            newfile.writerow(row)
            continue
        print cnt
        if cnt < l:
            cnt += 1
            newfile.writerow(row)
            continue
        if cnt == r:
            break
        
        cnt += 1
        s = row[3]
        #director awards
        row.append(countAwards(s))
        print s
        #actor awards
        s = row[9].split(',')
        row.append(countAwards(s))
        print s
        
        
        try:
            newfile.writerow(row)
        except:
            newfile.writerow([])
       
       
genData(7500,7999)
                







        







'''
m = ia.get_movie('0110912')
print m['director']
'''

'''
m = ia.search_movie('The Untouchables')
a = m[0]
ia.update(a)
print a['runtime']



for person in ia.search_person('Mel Gibson'):
        print person.personID, person['name']
'''
